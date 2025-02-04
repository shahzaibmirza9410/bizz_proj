from email.message import EmailMessage

from django.contrib.auth import logout
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import login, logout

from accounts.forms import SignUpForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from accounts.tokens import account_activation_token

from bizz.models import User
from_email = 'noreply@admin.drupsinvesting.com'
from bizz_proj import settings


def signup(request):
    if request.method == 'POST':
        print("post req")
        form = SignUpForm(request.POST)
        if form.is_valid():
            print("valid")
            user = form.save(commit=False)
            user.is_active = False
            #user.is_active = True
            user.save()
            print("user saved")
            subject = 'Activate Your DrupsInvesting Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': request.get_host(),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = user.email
            send_mail(subject, message='', html_message=message,
                      recipient_list=[email], from_email=from_email)
            #user.email_user(subject, message, html_message=message)
            #login(request, user)
            return redirect('account_activation_sent')
        else:
            form = SignUpForm()
            print("in else")
            for err in form.errors:
                print(err)
            messages.warning(request, "Signup Failed. Please Try Again.")
            return render(request, 'accounts/page-register.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'accounts/page-register.html', {'form': form})


def custom_logout(request):
    if request.user.is_authenticated:
        try:
            if request.user.auth_token:
                request.user.auth_token.delete()
        except Exception as e:
            pass
    logout(request)
    return redirect('login')



def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.emailverified = True
        user.save()
        login(request, user)
        return redirect('dashboard')
    else:
        return render(request, 'accounts/account_activation_invalid.html')

class PasswordRestConfirm(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'

    def get(self, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(self.kwargs['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None:
            user.emailverified = True
            user.save()
            """try:
                if user.phone is None:
                    phone = ''
                else:
                    phone = user.phone
                    data = {
                        "email_address": user.email,
                        "status": "subscribed",
                        'status_if_new': 'subscribed',
                        'merge_fields': {'FNAME': user.first_name, 'LNAME': user.last_name, 'PHONE': phone,
                                         'MMERGE8': user.id},
                    }

                    response = client.lists.members.create_or_update(list_id=list_id, subscriber_hash=user.email,
                                                                     data=data)
                    print(response)

            except Exception as e:
                print(e)"""
        resp = super().get(*args, **kwargs)
        return resp
