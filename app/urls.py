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
    path('csvdatafile/persons', views.persons_csv, name="persons_csv"),
    path('csvdatafile/persons/person_detail/<str:email>', views.person_detail, name="person_detail"),
    path('csvdatafile/persons/person_sent/<str:email>', views.person_sent, name="person_sent"),
    path('csvdatafile/link_analysis/link_analysis_choose_email', views.link_analysis_choose_email, name="link_analysis_choose_email"),
    path('csvdatafile/dataframetable', views.dataframe_table, name="dataframe_table"),
    path('choosefile_csv/', views.choosefile_csv, name="choosefile_csv"),

    path('emaildatafile/choosefolder', views.choosefolder, name="choosefolder"),
    path('emaildatafile/export/html', views.export_html, name="export_html"),
    path('emaildatafile/export/csv', views.export_csv, name="export_csv"),
    path('emaildatafile/export/save_csv', views.save_export_csv, name="save_export_csv"),
    path('emaildatafile/export/save_html', views.save_export_html, name="save_export_html"),
    
    path('emaildatafile/export/save_extract_email_address', views.save_extract_email_address, name="save_extract_email_address"),
    path('emaildatafile/extract/email_address', views.extract_email_address, name="extract_email_address"),
    path('emaildatafile/extract/action_extract_email_address', views.action_extract_email_address, name="action_extract_email_address"),

    path('emaildatafile/export/save_extract_phone_number', views.save_extract_phone_number, name="save_extract_phone_number"),
    path('emaildatafile/extract/phone_number', views.extract_phone_number, name="extract_phone_number"),
    path('emaildatafile/extract/action_extract_phone_number', views.action_extract_phone_number, name="action_extract_phone_number"),

    path('emaildatafile/extract/links', views.extract_links, name="extract_links"),
    path('emaildatafile/extract/action_extract_links', views.action_extract_links, name="action_extract_links"),
    path('emaildatafile/export/save_extract_links', views.save_extract_links, name="save_extract_links"),


    path('emaildatafile/inforemail/content/<str:filename>/<str:mesageid>', views.inforemail_content, name="inforemail_content"),
    path('emaildatafile/inforemail/wordcloud/<str:filename>/<str:mesageid>', views.inforemail_wordcloud, name="inforemail_wordcloud"),
    path('emaildatafile/inforemail/massageheader/<path:filename>/<str:mesageid>', views.inforemail_massageheader, name="inforemail_massageheader"),
    path('emaildatafile/inforemail/hexview/<path:filename>/<str:mesageid>', views.inforemail_hexview, name="inforemail_hexview"),

    path('emaildatafile/analysis/home', views.analysis, name="analysis"),
    path('emaildatafile/analysis/dashboard', views.dashboard, name="dashboard"),
    path('emaildatafile/tabledataframe', views.tabledataframe, name="tabledataframe"),
    path('emaildatafile/linkanalysis', views.linkanalysis, name="linkanalysis"),
    path('emaildatafile/linkanalysisjson', views.linkanalysisjson, name="linkanalysisjson"),
    path('emaildatafile/linkanalysisjson_single_email', views.linkanalysisjson_single_email, name="linkanalysisjson_single_email"),
    path('emaildatafile/analysis/persons', views.persons, name="persons"),
    path('emaildatafile/analysis/personinfor/<str:email>', views.personinfor, name="personinfor"),
    path('emaildatafile/analysis/personsent/<str:email>', views.personsent, name="personsent"),
    path('emaildatafile/analysis/personreceive/<str:email>', views.personreceive, name="personreceive"),
    path('emaildatafile/analysis/personsent/<str:email>/<str:mesageid>', views.personsentemail, name="personsentemail"),


    path('clearfilefolders/', views.clearfilefolders, name="clearfilefolders"),
    path('', views.base, name="base"),
    path('preview_html/<str:filename>', views.preview_html, name="preview_html"),
]
