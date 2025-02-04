import datetime
import json
import os
from django.core.mail import EmailMessage
from io import BytesIO

import django
import xlwt
from django.template.loader import render_to_string

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bizz_proj.settings")
django.setup()
from django.core.mail import  send_mail
from django.conf import settings
from bizz.models import List
from dateutil.relativedelta import relativedelta
from bizz.views import get_rows


def send_email(list):
    """rows = get_rows(list.filters)
    print(rows)
    excelfile = BytesIO()
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('records')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    print("here")
    columns = ['Title', 'Address', 'Asking Price', 'Gross Revenue', 'Ebitda', 'State', 'County',
               'Inventory', 'Real Estate', 'Established', 'Building Area(sf)', 'Employees',
               'Reason for selling', 'Age of Business', 'Description'
               ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(excelfile)

    email = EmailMessage(
        'Search Results for list saved at BizbuySell.com',
        'Hey, Attached file contains records for filters you saved at bizBuysell. Please contact us at customerservice@bizbuysell.com',
        settings.EMAIL_HOST_USER,
        ['hiraaltaf086@gmail.com'],
    )
    email.attach('file.xlsx', excelfile.getvalue(), 'application/vnd.ms-excel')
    print("email send")"""

    message = render_to_string('bizz/pages/scheduled_email.html', {
        'customer': f"{list.user.first_name} {list.user.last_name}",
        'filters': json.loads(list.user_filters),
        'list_id': list.id,
    })
    email = list.user.email
    print(email)
    send_mail('Reminder: Search Results for drupsinvesting', message='', html_message=message,
              recipient_list=[email], from_email='noreply@admin.drupsinvesting.com')


active_lists = List.objects.filter(email_active=True, next_email_date__date=datetime.datetime.now().date())
try:
    for list in active_lists:
        print(list.name)
        today = datetime.datetime.now()
        if list.last_email_sent:
            last_email_sent = list.last_email_sent
        else:
            last_email_sent = today
        print(f"lastsentdate: {last_email_sent}")

        if list.email_frequency == 'daily':
            next_date = last_email_sent + datetime.timedelta(days=1)
            list.last_email_sent = today
            list.next_email_date = next_date

        elif list.email_frequency == 'weekly':
            next_date = last_email_sent + datetime.timedelta(days=7)
            list.last_email_sent = today
            list.next_email_date = next_date

        elif list.email_frequency == 'monthly':
            next_date = last_email_sent + relativedelta(months=1)
            list.last_email_sent = today
            list.next_email_date = next_date
        send_email(list)
        list.save()
except Exception as e:
    send_mail('Email Sending failed at drupsinvesting', message='', html_message=f'Email failed. Error Description: {e}',
              recipient_list=['hiraaltaf086@gmail.com','customerservice@admin.drupsinvesting.com'], from_email='noreply@admin.drupsinvesting.com')
