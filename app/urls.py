from django.contrib import admin
from django.urls import path
from . import views 
urlpatterns = [
    path('emaildatafile/', views.emaildatafile, name="emaildatafile"),
    path('csvdatafile/', views.csvdatafile, name="csvdatafile"),
    path('choosefile_csv/', views.choosefile_csv, name="choosefile_csv"),
    path('emaildatafile/choosefolder', views.choosefolder, name="choosefolder"),
    path('emaildatafile/export/csv', views.export_csv, name="export_csv"),
    path('emaildatafile/export/save', views.save_export, name="save_export"),
    path('emaildatafile/inforemail/content/<path:filename>', views.inforemail_content, name="inforemail_content"),
    path('emaildatafile/inforemail/massageheader/<path:filename>', views.inforemail_massageheader, name="inforemail_massageheader"),
    path('emaildatafile/inforemail/hexview/<path:filename>', views.inforemail_hexview, name="inforemail_hexview"),

    path('clearfilefolders/', views.clearfilefolders, name="clearfilefolders"),
    path('', views.base, name="base"),
    path('home/', views.view_content, name="home"),
]
