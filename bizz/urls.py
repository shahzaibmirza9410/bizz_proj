from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from bizz import views
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView

urlpatterns = [
    path('',login_required(views.dashboard),
         name='dashboard'),
    path('records/',login_required(views.record_view),name='records'),
    path('ajax/list/save/',login_required(views.save_search),name='save-search'),
    path('ajax/get/records/',login_required(views.get_records),name='get-records'),
    path('settings/',login_required(views.settings),name='settings'),
    path('create_download_file/', login_required(views.create_download_file), name='create_download_file'),
    path('scripts/<str:tab>/',login_required(views.scripts),name='scripts'),
    path('scripts/update/<int:pk>',login_required(views.ScriptUpdate.as_view()),name='update-script'),
    path('saved-searches/',login_required(views.get_lists),name='lists'),
    path('ajax/list/update/',login_required(views.update_list),name='update-list'),
    path('list/view/<int:pk>',login_required(views.view_list),name='view-list'),
    path('script/delete/<int:pk>',login_required(views.delete_script),name='script-delete'),
    path('ajax/script/update/',login_required(views.update_script),name='script-updates'),

]
