from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from accounts import views
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('login/', LoginView.as_view(template_name='accounts/page-login.html', success_url='dashboard'), name='login'),
    path('signup/', views.signup, name='signup'),
        path('logout/', views.custom_logout, name='logout'),

    path('change-password/', login_required(PasswordChangeView.as_view(template_name='accounts/change_password.html',
                                                                          success_url='/')), name="change_pass"),
    path(r'account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path(r'activate/<uidb64>/<token>/',
         views.activate, name='activate'),

    path('password_reset/',


         auth_views.PasswordResetView.as_view(html_email_template_name='accounts/password_reset_email.html',
                                              template_name='accounts/password_reset.html'),
         name='password_reset_page'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordRestConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    ]