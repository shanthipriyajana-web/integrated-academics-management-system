from django.urls import path
from . import views

urlpatterns = [
    path('setup/',                        views.first_run_setup,     name='first_run_setup'),
    path('login/',                        views.login_view,          name='login'),
    path('logout/',                       views.logout_view,         name='logout'),
    path('signout/',                      views.signout_page,        name='signout'),
    path('forgot-password/',              views.forgot_password_view, name='forgot_password'),
    path('reset-password/<uuid:token>/',  views.reset_password_view,  name='reset_password'),
    path('check-role/',                   views.check_role_view,      name='check_role'),
]
