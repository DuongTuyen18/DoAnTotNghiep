from django.shortcuts import render
from .utils import List_Infor_Email_Eml,Content_Email_Eml,inforEmail,convert_eml_to_csv,clear_folder_in_media,read_csv_file
import os
import csv
import email
from email.utils import parseaddr
from django.http import HttpResponse
from email.parser import Parser
from dateutil.parser import parse
from email.header import decode_header
from django.http import JsonResponse
from django.shortcuts import redirect
from pathlib import Path
from django.core.files.uploadhandler import FileUploadHandler
from django.conf import settings
import shutil
folder_name = ''
filecsv_name = ''
path_file_export = ''
def choosefolder(request):
    global folder_name
    if request.method == 'POST':
        # Lấy thư mục được chọn từ thẻ input
        folder = request.FILES.getlist('folder')
        folder_name = request.POST.get('folder_name')
        # Lấy đường dẫn tuyệt đối đến thư mục upload
        upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads')

        # Dọn file trong folder uoloads
        clear_folder_in_media('uploads')
        
        # Tạo đối tượng FileUploadHandler để xử lý các file được upload từ thư mục
        handler = FileUploadHandler()
        
        for file in folder:
            # Lấy tên của file
            file_name = os.path.basename(file.name)
            # Lưu file vào thư mục upload
            with open(os.path.join(upload_path, file_name), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        return redirect("emaildatafile")
    
def export_csv(request):
    global folder_name
    global path_file_export
    upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
    export_path = os.path.join(settings.MEDIA_ROOT, 'export')
    clear_folder_in_media('export')
    data=List_Infor_Email_Eml(upload_path)
    if not data:
        return redirect("base")
    else:
        path_file_export = convert_eml_to_csv(upload_path,export_path,folder_name)
        csv_infor = read_csv_file(path_file_export)
        context = {'list_email':data,'folder_name':folder_name,'csv_infor':csv_infor}
        return render(request,'app/export/csv_file.html',context)

def save_export(request):
    global folder_name
    global path_file_export
    folder_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
    data=List_Infor_Email_Eml(folder_path)
    if not data:
        return redirect("base")
    else:   
        if os.path.exists(path_file_export):
            with open(path_file_export, 'rb') as file:
                response = HttpResponse(file.read(), content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="'+folder_name+'.csv"'
                return response
        return HttpResponse('File not found.', status=404)
    
def emaildatafile(request):
    global folder_name
    #folder_path = Path(folder_path)
    folder_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
    data=List_Infor_Email_Eml(folder_path)
    if not data:
        return redirect("base") 
    else:   
        context = {'list_email':data,'folder_name':folder_name}
        return render(request,'app/emaildatafile.html',context)
    
def choosefile_csv(request):
    global filecsv_name
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file_input')  # Lấy file CSV từ request.FILES
        # Lấy đường dẫn tuyệt đối đến thư mục upload
        upload_path = os.path.join(settings.MEDIA_ROOT, 'csv_file')
        # Dọn file trong folder uoloads
        clear_folder_in_media('csv_file')
        filecsv_name = os.path.basename(csv_file.name)
        # Lưu file vào thư mục upload
        with open(os.path.join(upload_path, filecsv_name), 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)
        return redirect('csvdatafile')

def csvdatafile(request):
    global filecsv_name
    #folder_path = Path(folder_path)
    csv_file_path = os.path.join(settings.MEDIA_ROOT, 'csv_file')
    path_file_csv = os.path.join(csv_file_path, filecsv_name) 
    csv_infor = read_csv_file(path_file_csv)
    context = {'filecsv_name':filecsv_name,'csv_infor':csv_infor}
    return render(request,'app/Email_CsvFile/csvdatafile.html',context)

def base(request):
    clear_folder_in_media('uploads')
    clear_folder_in_media('export')
    clear_folder_in_media('csv_file')
    return render(request,'app/base.html')

def home(request):
    return render(request,'app/home.html')



def inforemail_content(request, filename):
    global folder_name
    folder_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
    data=List_Infor_Email_Eml(folder_path)
    if not data:
        return redirect("base")
    else:   
        eml_file_path = folder_path+"\\"+filename
        infor_email = inforEmail(eml_file_path)
        context = {'list_email':data,'infor_email': infor_email,'file_name':filename,'folder_name':folder_name}
        return render(request, 'app/inforEmaildatafile_content.html', context)

    
def inforemail_massageheader(request, filename):
    global folder_name
    folder_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
    data=List_Infor_Email_Eml(folder_path)
    if not data:
        return redirect("base")
    else: 
        eml_file_path =folder_path+"\\"+filename
        infor_email = inforEmail(eml_file_path)
        context = {'list_email':data,'infor_email': infor_email,'file_name':filename,'folder_name':folder_name}
        return render(request, 'app/inforEmaildatafile_massageheader.html', context)

def inforemail_hexview(request, filename):
    global folder_name
    folder_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
    data=List_Infor_Email_Eml(folder_path)
    if not data:
        return redirect("base")
    else: 
        eml_file_path = folder_path+"\\"+filename
        infor_email = inforEmail(eml_file_path)
        context = {'list_email':data,'infor_email': infor_email,'file_name':filename,'folder_name':folder_name}
        return render(request, 'app/inforEmaildatafile_hexview.html', context)

def read_files_in_folder(request):
    folder_path = "D:\\hoc tap\\DoAn\\ProjectDoAn\\EmailForensicTool\\media\\uploads\\"
    eml_files = [f for f in os.listdir(folder_path) if f.endswith('.eml')]
    name_files=str(eml_files[0])
    eml_path = "D:\\hoc tap\\DoAn\\ProjectDoAn\\EmailForensicTool\\media\\uploads\\"+"\\"+name_files
    if not os.path.exists(eml_path):
        return HttpResponse("File not found")
    
    with open(eml_path, "rb") as f:
        msg = email.message_from_bytes(f.read())
        
        headers = msg.items()
        header_string = "<br>".join([f"{k}: {v}" for k, v in headers])
        
        return HttpResponse(header_string)


def view_content(request):
    if request.method == 'POST':
        folder = request.FILES.get('folder', None)
        if folder is not None:
            # folder_path = folder.temporary_file_path()
            # Xử lý đường dẫn của thư mục ở đây
            return HttpResponse(f'Đã chọn thư mục: {folder}')
    return render(request, 'app/home.html')
    # return HttpResponse(email_content)
def clearfilefolders(request):
    clear_folder_in_media('uploads')
    clear_folder_in_media('export')
    clear_folder_in_media('csv_file')
    return redirect("base")