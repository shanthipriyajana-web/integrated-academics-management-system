from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header  = "VSU Timetable – Admin"
admin.site.site_title   = "VSU Admin"
admin.site.index_title  = "Management Panel"

urlpatterns = [
    path('admin/',    admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('',          include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
