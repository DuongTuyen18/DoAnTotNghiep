from django.contrib import admin
from django.urls import path
from . import views 
urlpatterns = [
    path('emaildatafile/', views.emaildatafile, name="emaildatafile"),
    path('csvdatafile/', views.csvdatafile, name="csvdatafile"),
    path('csvdatafile/dashboard', views.dashboard_csv, name="dashboard_csv"),
    path('csvdatafile/check_email', views.check_email, name="check_email"),
    path('csvdatafile/get_list_to_by_from', views.get_list_to_by_from, name="get_list_to_by_from"),
    path('csvdatafile/link_analysis', views.link_analysis, name="link_analysis"),
    path('csvdatafile/link_analysis/link_analysis_choose_email', views.link_analysis_choose_email, name="link_analysis_choose_email"),
    path('csvdatafile/dataframetable', views.dataframe_table, name="dataframe_table"),
    path('choosefile_csv/', views.choosefile_csv, name="choosefile_csv"),
    path('emaildatafile/choosefolder', views.choosefolder, name="choosefolder"),
    path('emaildatafile/export/csv', views.export_csv, name="export_csv"),
    path('emaildatafile/export/save', views.save_export, name="save_export"),
    path('emaildatafile/inforemail/content/<str:filename>', views.inforemail_content, name="inforemail_content"),
    path('emaildatafile/inforemail/massageheader/<path:filename>', views.inforemail_massageheader, name="inforemail_massageheader"),
    path('emaildatafile/inforemail/hexview/<path:filename>', views.inforemail_hexview, name="inforemail_hexview"),

    path('clearfilefolders/', views.clearfilefolders, name="clearfilefolders"),
    path('', views.base, name="base"),
    path('home/', views.view_content, name="home"),
]
