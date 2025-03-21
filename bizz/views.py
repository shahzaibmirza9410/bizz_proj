import datetime
import json
import re
import urllib
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from bizz.models import ScrapedData
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from bizz.models import ScrapedData, Scraped_data, Archives, Archive
import xlwt
from django.utils.encoding import force_bytes, force_str
from django.db.models import Q

from bizz.models import List, User, Script, Config

from bizz.forms import ConfigForm, ScriptsForm
from django.views.generic import UpdateView

data_filters = {"gross_min": "gross_revenue__gte", "gross_max": "gross_revenue__lte", "cash_min": "cash_flow__gte",
                "cash_max": "cash_flow__lte", "ebita_min": "ebitda__gte", "ebita_max": "ebitda__lte",
                "No_Emp_min": "employees__gte", "No_Emp_max": "employees__lte", "askingprice_min": "asking_price__gte"
    , "askingprice_max": "asking_price__lte", "building_area_min": "building_sf__gte",
                "building_area_max": "building_sf__lte",
                "retire_reason": "reason_for_selling__icontains", 'state': 'state__in', 'county': 'county__in',
                'age_of_business': 'age_years__lte',
                'RSIncluded': 'real_estate', 'InventoryIncluded': 'inventory', 'date-from': 'first_scraped_time__gte',
                'date-to': 'first_scraped_time__lte',
                'buz_category': 'category', 'query': 'address__icontains',
                'inventory_price_gte': 'inventory_price__gte','inventory_price_lte':'inventory_price__lte',
                'rent_min': 'rent__gte','rent_max':'rent__lte',
                'lease-date-to':'lease_expiration_date__lte','lease-date-from':'lease_expiration_date__gte',
                'listings':'listing_type'
                }

states_dic = {'ak': 'Alaska', 'al': 'Alabama', 'ar': 'Arkansas', 'as': 'American Samoa', 'az': 'Arizona',
              'ca': 'California', 'co': 'Colorado', 'ct': 'Connecticut', 'dc': 'District of Columbia',
              'de': 'Delaware', 'fl': 'Florida', 'fm': 'Federated States of Micronesia', 'ga': 'Georgia', 'gu': 'Guam',
              'hi': 'Hawaii', 'ia': 'Iowa', 'id': 'Idaho', 'il': 'Illinois', 'in': 'Indiana', 'ks': 'Kansas',
              'ky': 'Kentucky', 'la': 'Louisiana', 'ma': 'Massachusetts', 'md': 'Maryland', 'me': 'Maine',
              'mh': 'Marshall Islands', 'mi': 'Michigan', 'mn': 'Minnesota', 'mo': 'Missouri',
              'mp': 'Northern Mariana Islands', 'ms': 'Mississippi', 'mt': 'Montana', 'nc': 'North Carolina',
              'nd': 'North Dakota', 'ne': 'Nebraska', 'nh': 'New Hampshire', 'nj': 'New Jersey', 'nm': 'New Mexico',
              'nv': 'Nevada', 'ny': 'New York', 'oh': 'Ohio', 'ok': 'Oklahoma', 'or': 'Oregon', 'pa': 'Pennsylvania',
              'pr': 'Puerto Rico', 'ri': 'Rhode Island', 'pw': 'Palau', 'sc': 'South Carolina', 'sd': 'South Dakota',
              'tx': 'Texas', 'tn': 'Tennessee', 'ut': 'Utah', 'va': 'Virginia', 'vi': 'Virgin Islands',
              'vt': 'Vermont', 'wa': 'Washington', 'wi': 'Wisconsin', 'wv': 'West Virginia', 'wy': 'Wyoming',
              'aa': 'Armed Forces Americas', 'ae': 'Armed Forces Africa', 'ap': 'Armed Forces Pacific'
              }
from_email = 'noreply@admin.drupsinvesting.com'


def view_list(request, pk):
    my_list = List.objects.get(id=pk)
    filters = my_list.filters
    if request.method == 'GET':
        context = {}
        if filters:
            res = get_rows(filters,False)
            paginator = Paginator(res, 10)
            page = request.GET.get('page')
            try:

                records = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                records = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                records = paginator.page(paginator.num_pages)
            response = render_to_string('bizz/pages/filtered_records2.html',
                                        context={'records': records, 'num_pages': paginator.num_pages, 'list':my_list})

            context['response'] = response
            context['list'] = my_list
            states = Scraped_data.objects.order_by().values_list('state', flat=True).distinct()
            counties = Scraped_data.objects.order_by().values_list('county', flat=True).distinct()
            categories = Scraped_data.objects.order_by().values('category').distinct()

            listing_type = Scraped_data.objects.order_by().values('listing_type').distinct()
            s = list(states)
            c = list(counties)
            for idx, state in enumerate(s):
                if state != '':
                    s[idx] = states_dic[state.lower()]
            context['locations'] = s + c
            context['categories'] = categories
            context['listing_type'] = listing_type
            context['filters'] = filters
            print(f"sending list: {my_list}")
            request.session['filters'] = filters
        return render(request, template_name='bizz/pages/tables2.html', context=context)


def record_view(request):
    context = {}
    states = Scraped_data.objects.order_by().values_list('state', flat=True).distinct()
    counties = Scraped_data.objects.order_by().values_list('county', flat=True).distinct()
    categories = Scraped_data.objects.order_by().values('category').distinct()
    listing_type = Scraped_data.objects.order_by().values('listing_type').distinct()
    s = list(states)
    c = list(counties)
    for idx, state in enumerate(s):
        if state != '':
            s[idx] = states_dic[state.lower()]
    context['locations'] = s + c
    context['categories'] = categories
    context['listing_type'] = listing_type
    res = Scraped_data.objects.all()
    res = res.values('title', 'address',
                     'asking_price',
                     'gross_revenue', 'ebitda', 'cash_flow',
                     'established', 'state', 'county', 'inventory', 'real_estate', 'established', 'description',
                     'building_sf', 'employees',
                     'reason_for_selling', 'real_estate_from_detail', 'furniture_fixture_equipment', 'facilities',
                     'competition',
                     'franchise', 'business_website', 'scraped_time', 'detail_url')
    paginator = Paginator(res, 10)
    page = request.GET.get('page')
    try:

        records = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        records = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        records = paginator.page(paginator.num_pages)
    response = render_to_string('bizz/pages/filtered_records.html',
                                context={'records': records, 'num_pages': paginator.num_pages, })
    context['response'] = response
    if request.method == 'GET':
        return render(request, template_name='bizz/pages/tables.html', context=context)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@csrf_exempt
def get_lists(request):
    if request.user.is_staff:
        lists = List.objects.all()
    else:
        lists = List.objects.filter(user=request.user)
    for list in lists:
        if list.user_filters:
            list.user_filters = json.loads(list.user_filters)
    return render(request, template_name='bizz/pages/saved-lists.html', context={'lists': lists})


@csrf_exempt
def save_search(request):
    data = {}
    email_preference = request.GET.get('email_preference', '')
    list_name = request.GET.get('list_name', '')
    filters = request.GET.get('filters', '')
    user_filters = request.GET.get('user_filters', '')
    user = User.objects.get(id=request.user.id)
    new_list = List()
    new_list.name = list_name
    new_list.user_filters = user_filters
    new_list.filters = filters
    new_list.user = user
    new_list.email_preference = email_preference
    new_list.save()
    subject = 'New Search Saved on DrupsInvesting'
    message = render_to_string('bizz/pages/email_template.html', {
        'filters': json.loads(user_filters),
        'customer': f"{user.first_name} {user.last_name}",
        'list_id':new_list.id
    })
    email = user.email
    send_mail(subject, message='', html_message=message,
              recipient_list=[email], from_email=from_email)

    data['status_code'] = 1
    return JsonResponse(data)


def delete_script(request, pk):
    if request.method == 'GET':
        scripts = Script.objects.get(id=pk)
        scripts.delete()
        messages.success(request, "Script Deleted")
        return redirect('scripts', tab='active-scripts-tab')


def update_script(request, pk):
    if request.method == 'GET':
        scripts = Script.objects.get(id=pk)
        scripts.delete()
        messages.success(request, "Script Deleted")
        return redirect('scripts')


def statistics(script):
    script.total_listing_scrapped = Scraped_data.objects.count()
    seven_days_before = datetime.datetime.now() - datetime.timedelta(days=7)
    script.new_listing_scrapped = Scraped_data.objects.filter(
        scraped_time__range=[seven_days_before, datetime.datetime.now()]).count()
    script.old_listing_deleted = Archive.objects.all().count()
    script.last_run_date = Scraped_data.objects.values_list('scraped_time', flat=True).first()
    print(script.last_run_date)
    return script


def scripts(request, tab):
    active_tab = "active-scripts-tab"
    active_tab = tab
    config = {}
    try:
        config = Config.objects.all()
        config = config[0]
        print(config.id)
    except Exception as e:
        print(e)
    config_form = ConfigForm(instance=config)
    if request.method == 'GET':
        scripts = []
        if tab == 'active-scripts-tab':
            scripts = Script.objects.filter(schedule_active=True)
        elif tab == 'history-tab':
            scripts = Script.objects.filter(schedule_active=False)
        for script in scripts:
            if script.title == 'BizBuySell':
                script = statistics(script)
                script.save()
        form = ScriptsForm()
        context = {'scripts': scripts, 'form': form, 'active_tab': active_tab,'setting': config, 'config_form': config_form}
        return render(request, template_name='bizz/pages/scripts.html', context=context)
    if request.method == 'POST':
        form = ScriptsForm(request.POST)
        if form.is_valid():
            messages.success(request, "Script Added")
            form.save()
        else:
            messages.warning(request, "Action Failed. Please Try Again.")
        return redirect('scripts', tab='active-scripts-tab')


def settings(request):
    config = {}
    try:
        config = Config.objects.all()
        config = config[0]
        print(config.id)
    except Exception as e:
        print(e)
    form = ConfigForm(instance=config)
    if request.method == 'GET':
        context = {'setting': config, 'config_form': form}
        return render(request, template_name='bizz/pages/settings.html', context=context)
    if request.method == 'POST':
        form = ConfigForm(request.POST, instance=config)
        if form.is_valid():
            messages.success(request, "Settings Updated")
            form.save()
            
        else:
            messages.warning(request, "Action Failed. Please Try Again.")
        return redirect('settings')


def dashboard(request):
    try:
        script = Script.objects.get(title='BizBuySell')
        if script:
            script = statistics(script)
            script.save()
        return render(request, template_name='bizz/pages/dashboard.html', context={'script': script})
    except Exception as e:
        return render(request, template_name='bizz/pages/dashboard.html', context={'script': ''})


def update_list(request):
    data = {'status_code': 0}
    if is_ajax(request):
        email_freq = request.GET.get('email_freq', None)
        list_id = request.GET.get('list_id', None)
        ActiveEmail = request.GET.get('ActiveEmail', None)
        email_preference = request.GET.get('email_preference', '')
        list_name = request.GET.get('list_name', '')
        filters = request.GET.get('filters', '')
        user_filters = request.GET.get('user_filters', '')

        if list_id and email_freq:
            list = List.objects.get(id=list_id)
            list.email_frequency = email_freq
            if ActiveEmail == "true":
                list.email_active = True
            else:
                list.email_active = False

            today = datetime.datetime.now()
            if list.last_email_sent:
                last_email_sent = list.last_email_sent
            else:
                last_email_sent = ''
            if list.email_frequency == 'daily':
                if last_email_sent:
                    list.next_email_date = last_email_sent + datetime.timedelta(days=1)
                else:
                    list.next_email_date = today
            elif list.email_frequency == 'weekly':
                if last_email_sent:
                    list.next_email_date = last_email_sent + datetime.timedelta(days=7)
                else:
                    list.next_email_date = today
            elif list.email_frequency == 'monthly':
                if last_email_sent:
                    list.next_email_date = last_email_sent + relativedelta(months=1)
                else:
                    list.next_email_date = today

            list.save()
            data['status_code'] = 1
        elif list_id and list_name:
            my_list = List.objects.get(id=list_id)
            user = User.objects.get(id=request.user.id)
            my_list.name = list_name
            my_list.user_filters = user_filters
            my_list.filters = filters
            my_list.user = user
            my_list.email_preference = email_preference
            my_list.save()
            data['status_code'] = 1
    else:
        data['status_code'] = 0
    return JsonResponse(data)


def get_records(request):
    data = {'status_code': 0}
    if is_ajax(request):
        filters = request.GET.get('filters', None)
        my_filters = {}
        if filters:
            res = get_rows(filters,False)

            paginator = Paginator(res, 10)
            page = request.GET.get('page')
            try:

                records = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                records = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                records = paginator.page(paginator.num_pages)
            response = render_to_string('bizz/pages/filtered_records.html',
                                        context={'records': records, 'num_pages': paginator.num_pages, })

            request.session['filters'] = filters
            data['status_code'] = 1
            data['response'] = response
        else:
            data['status_code'] = 0
        return JsonResponse(data)


def get_rows(filters, sorted):
    my_filters = {}
    filters_applied = {}
    if filters:
        filters_applied = json.loads(filters)

    for key, val in filters_applied.items():
        if key in ['query', 'gross_min', 'gross_max', 'cash_min', 'cash_max', "ebita_min",
                   "ebita_max", "No_Emp_min", "No_Emp_max", "age_of_business",
                   "askingprice_min", 'askingprice_max', 'building_area_min', 'building_area_max',
                   'retire_reason', 'InventoryIncluded', 'RSIncluded', 'date-from', 'date-to', 'buz_category',
                   'inventory_price_gte','inventory_price_lte','lease-date-to','lease-date-from','rent_min','rent_max','listings']:
            if val:
                print(key)
                if key == 'age_of_business':
                    val = int(val)
                    my_filters[f'{data_filters[key]}'] = val

                elif key in ['gross_min', 'gross_max', 'cash_min', 'cash_max', "ebita_min",
                             "ebita_max", "No_Emp_min", "No_Emp_max",
                             "askingprice_min", 'askingprice_max', 'building_area_min', 'building_area_max'
                    ,'inventory_price_gte','inventory_price_lte','rent_min','rent_max']:

                    for char in [',', '$']:
                        val = val.replace(char, '')
                    val = int(val)
                    my_filters[f'{data_filters[key]}'] = val

                elif key in ['query']:
                    if val in states_dic.values():
                        for k, v in states_dic.items():
                            if v == val:
                                val = k
                        my_filters['state__icontains'] = val
                    else:
                        my_filters['address__icontains'] = val
                else:
                    my_filters[f'{data_filters[key]}'] = val
    print(f"myflters: {my_filters}")
    keywords = filters_applied.get('keywords', '')
    if my_filters:
        res = Scraped_data.objects.filter(**my_filters)
        if keywords:
            for keyword in keywords:
                res = res.filter(
                    Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(
                        facilities__icontains=keyword)
                    | Q(competition__icontains=keyword)
                )
    else:
        if keywords:
            res = ''
            for keyword in keywords:
                if res:
                    res = res.filter(
                        Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(
                            facilities__icontains=keyword)
                        | Q(competition__icontains=keyword)
                    )
                else:
                    res = Scraped_data.objects.filter(
                        Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(
                            facilities__icontains=keyword)
                        | Q(competition__icontains=keyword)
                    )
        else:
            print("in else getting all")
            res = Scraped_data.objects.all()[:2000]
    if sorted:
        res = res.values_list('title', 'address',
                              'asking_price',
                              'gross_revenue', 'ebitda', 'state', 'county', 'inventory', 'real_estate', 'established',
                              'building_sf', 'employees',
                              'reason_for_selling', 'age_years', 'description', 'cash_flow', 'facilities',
                              'competition',
                              'real_estate_from_detail', 'furniture_fixture_equipment', 'franchise', 'business_website',
                              'detail_url', 'category', 'cash_flow_multiple','rent','inventory_price','listing_type')
    else:
        res = res.values('title', 'address',
                         'asking_price',
                         'gross_revenue', 'ebitda', 'cash_flow',
                         'established', 'state','age_years', 'county', 'inventory', 'real_estate', 'established', 'description',
                         'building_sf', 'employees',
                         'reason_for_selling', 'real_estate_from_detail', 'furniture_fixture_equipment',
                         'facilities', 'competition',
                         'franchise', 'business_website', 'scraped_time', 'detail_url', 'category',
                         'cash_flow_multiple','scraped_time','rent','lease_expiration_date','inventory_price','listing_type')
    return res


def create_download_file(request):
    filters = request.session.get('filters')
    rows = get_rows(filters,True)
    response = HttpResponse(content_type='application/ms-excel')
    filename = 'DrupsInvesting File.xlsx'
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('report')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Title', 'Address', 'Asking Price', 'Gross Revenue', 'Ebitda', 'State', 'County',
               'Inventory', 'Real Estate', 'Established', 'Building Area(sf)', 'Employees',
               'Reason for selling', 'Age of Business', 'Description','Cash flow','Category','Competition',
               'Real Estate From Detail', 'Furniture Fixture Equipment', 'Franchise', 'Business Website',
               'Detail Url', 'Category', 'Cash Flow Multiple','Rent','Inventory Price','Listing Type'
               ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


class ScriptUpdate(UpdateView):
    model = Script
    template_name = 'bizz/pages/update_script.html'
    form_class = ScriptsForm
    success_url = reverse_lazy('scripts', kwargs={'tab': 'active-scripts-tab'})
