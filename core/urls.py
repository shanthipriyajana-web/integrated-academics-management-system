from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('',                    lambda request: redirect('dashboard') if request.user.is_authenticated else redirect('login'), name='home'),
    path('dashboard/',          views.dashboard,         name='dashboard'),
    path('timetable/',          views.timetable_view,    name='timetable'),
    path('resources/',          views.resources_view,    name='resources'),
    path('manage/subjects/',    views.manage_subjects,   name='manage_subjects'),
    path('manage/faculty/',     views.manage_faculty,    name='manage_faculty'),
    path('manage/users/',       views.manage_users,      name='manage_users'),
    path('manage/resources/',   views.manage_resources,  name='manage_resources'),
]
