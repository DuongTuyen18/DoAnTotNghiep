from django.shortcuts import render
from .utils import count_spam_emails, list_from_extract_phone_number, list_bcc_extract_email_address, list_cc_extract_email_address, list_to_extract_email_address, list_from_extract_email_address, convert_eml_to_html, list_to_by_from, check_email_availability,find_links_by_emails,get_list_from_and_to,convert_graph_to_json,create_link_analysis,wordcloud_view,List_Infor_Email_Eml,get_list_from,inforEmail,convert_eml_to_csv,clear_folder_in_media,read_csv_file,convert_csv_to_dataframe,get_data_day_statistical,get_data_month_statistical,get_data_year_statistical,get_list_to
import os
import zipfile
import email
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.files.uploadhandler import FileUploadHandler
from django.conf import settings
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
import pandas as pd
import networkx as nx
folder_name = ''
filecsv_name = ''
path_file_export = ''
def check_email(request):
    email = request.GET.get('sender_email')
    print(email)
    if email:
        is_available = check_email_availability(email)
        response = {'available': is_available}
        return JsonResponse(response)
    else:
        response = {'error': 'Invalid email'}
        return JsonResponse(response, status=400)
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
    export_path = os.path.join(settings.MEDIA_ROOT, 'export/csv')
    clear_folder_in_media('export/csv')
    data=List_Infor_Email_Eml(upload_path)
    if not data:
        return redirect("base")
    else:
        path_file_export = convert_eml_to_csv(upload_path,export_path,folder_name)
        csv_infor = read_csv_file(path_file_export)
        context = {'list_email':data,'folder_name':folder_name,'csv_infor':csv_infor}
        return render(request,'app/export/csv_file.html',context)
    
def export_html(request):
    global folder_name
    global path_file_export
    upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
    export_path = os.path.join(settings.MEDIA_ROOT, 'export/html')

    clear_folder_in_media('export/html')

    # tạo folder lưu chữ các file html
    html_folder_path = os.path.join(export_path , folder_name)
    # Kiểm tra nếu thư mục chưa tồn tại
    if not os.path.exists(html_folder_path):
        # Tạo thư mục mới
        os.makedirs(html_folder_path)

    data=List_Infor_Email_Eml(upload_path)
    if not data:
        return redirect("base")
    else:
        path_file_export = convert_eml_to_html(upload_path, html_folder_path)
        html_files = os.listdir(html_folder_path)
        context = {'list_email':data,'folder_name':folder_name,'html_files':html_files}
        return render(request,'app/export/html_file.html',context)
    

def preview_html(request, filename):
    global folder_name
    html_folder_path = os.path.join(settings.MEDIA_ROOT, 'export\\html\\', folder_name)
    html_file_path = os.path.join(html_folder_path, filename)

    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    return render(request, 'app/export/html_preview.html', {'html_content': html_content})

def save_export_csv(request):
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

def save_export_html(request):
    global folder_name
    global path_file_export
    export_path = path_file_export  # Đường dẫn đến thư mục chứa các file .html
    zip_filename = folder_name + '.zip'  # Tên file ZIP đính kèm

    # Kiểm tra xem thư mục nguồn có tồn tại không
    if os.path.exists(export_path):
        # Tạo file ZIP để lưu trữ thư mục
        zip_filepath = os.path.join(settings.MEDIA_ROOT, zip_filename)
        with zipfile.ZipFile(zip_filepath, 'w') as zip_file:
            # Lặp qua từng file trong thư mục nguồn và thêm vào file ZIP
            for root, _, files in os.walk(export_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, export_path))

        # Đọc file ZIP và trả về response để người dùng tải về
        with open(zip_filepath, 'rb') as zip_file:
            response = HttpResponse(zip_file, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="' + zip_filename + '"'
        
        # Xóa file ZIP sau khi đã trả về response
        os.remove(zip_filepath)
        
        return response
    else:
        return HttpResponse('Source folder not found.', status=404)

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
    

def link_analysis(request):
    global filecsv_name
    #folder_path = Path(folder_path)
    csv_file_path = os.path.join(settings.MEDIA_ROOT, 'csv_file')
    path_file_csv = os.path.join(csv_file_path, filecsv_name) 
    data_detail = convert_csv_to_dataframe(path_file_csv)
    list_form_and_to = get_list_from_and_to(data_detail)
    context = {'filecsv_name':filecsv_name,'list_form_and_to':list_form_and_to}
    return render(request,'app/emailcsvfile/link_analysis.html',context)

def link_analysis_choose_email(request):
    global filecsv_name
    #folder_path = Path(folder_path)
    csv_file_path = os.path.join(settings.MEDIA_ROOT, 'csv_file')
    path_file_csv = os.path.join(csv_file_path, filecsv_name) 
    data_detail = convert_csv_to_dataframe(path_file_csv)
    list_email = request.GET.getlist('list_email[]')
    link_analysis_data, link_counts = find_links_by_emails(data_detail,list_email)
    link_analysis_data_int = nx.Graph()
    for u, v, attr in link_analysis_data.edges(data=True):
        attr['count'] = int(attr['count'])
        link_analysis_data_int.add_edge(u, v, **attr)
    link_analysis_json = convert_graph_to_json(link_analysis_data)
    return JsonResponse(link_analysis_json, safe=False)



def get_list_to_by_from(request):
    global filecsv_name
    #folder_path = Path(folder_path)
    csv_file_path = os.path.join(settings.MEDIA_ROOT, 'csv_file')
    path_file_csv = os.path.join(csv_file_path, filecsv_name) 
    data_detail = convert_csv_to_dataframe(path_file_csv)
    sender_email = request.GET.get('sender_email')
    print("email: "+sender_email)
    list_to = list_to_by_from(data_detail,sender_email)
    print(list_to)
    return JsonResponse({'list_to_by_from': list_to})

def dashboard_csv(request):
    global filecsv_name
    #folder_path = Path(folder_path)
    csv_file_path = os.path.join(settings.MEDIA_ROOT, 'csv_file')
    path_file_csv = os.path.join(csv_file_path, filecsv_name) 
    data_detail = convert_csv_to_dataframe(path_file_csv)
    data_day_statistical = get_data_day_statistical(data_detail)
    data_month_dtatistical = get_data_month_statistical(data_detail)
    data_year_dtatistical = get_data_year_statistical(data_detail)
    data_list_from = get_list_from(data_detail)
    data_list_to = get_list_to(data_detail)
    data_day_statistical_json = json.dumps(data_day_statistical.to_dict('records'))
    data_month_statistical_json = json.dumps(data_month_dtatistical.to_dict('records'))
    data_year_statistical_json = json.dumps(data_year_dtatistical.to_dict('records'))
    data_list_from_json = json.dumps(data_list_from.to_dict('records'))
    data_list_to_json = json.dumps(data_list_to.to_dict('records'))
    image_data = wordcloud_view(data_detail)
    # image_data_link_analysis = create_link_analysis(data_detail)
    link_analysis_data, link_counts = create_link_analysis(data_detail)
    link_analysis_json = convert_graph_to_json(link_analysis_data)
    context = {'filecsv_name':filecsv_name,'data_day_statistical_json':data_day_statistical_json,'data_month_statistical_json':data_month_statistical_json,'data_year_statistical_json':data_year_statistical_json,'data_list_from_json':data_list_from_json,'data_list_to_json':data_list_to_json,'image_data':image_data,'link_analysis_json':link_analysis_json }
    return render(request,'app/emailcsvfile/home.html',context)

def dataframe_table(request):
    global filecsv_name
    #folder_path = Path(folder_path)
    csv_file_path = os.path.join(settings.MEDIA_ROOT, 'csv_file')
    path_file_csv = os.path.join(csv_file_path, filecsv_name) 
    keyword_search = request.GET.get('keyword_search')
    # Lấy giá trị từ ô nhập liệu "from-date"
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    data_detail = convert_csv_to_dataframe(path_file_csv)
    if keyword_search:
        # Tạo điều kiện lọc cho các cột "From", "To", "Subject", và "Content"
        condition = (
            data_detail['file'].str.contains(keyword_search, case=False, na=False) |
            data_detail['From'].str.contains(keyword_search, case=False, na=False) |
            data_detail['To'].str.contains(keyword_search, case=False, na=False) |
            data_detail['Subject'].str.contains(keyword_search, case=False, na=False) |
            data_detail['Content'].str.contains(keyword_search, case=False, na=False)
        )
        # Lọc dữ liệu theo điều kiện
        data_detail = data_detail[condition]
    if from_date and to_date:
        # Chuyển giá trị từ ô nhập liệu "from-date" và "to-date" thành kiểu datetime
        from_date = pd.to_datetime(from_date)
        to_date = pd.to_datetime(to_date)
        # Lọc các dòng có cột "Date" nằm trong khoảng từ "from-date" đến "to-date"
        data_detail = data_detail[(data_detail['Date'] >= from_date) & (data_detail['Date'] <= to_date)]


    # Chuyển đổi DataFrame thành danh sách dict
    data_list = data_detail.to_dict('records')
    
    paginator = Paginator(data_list, 12)  # mỗi trang có tối đa 12 phần tử
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'filecsv_name':filecsv_name,'page_obj': page_obj}
    return render(request, 'app/emailcsvfile/dataframe_table.html', context)


def csvdatafile(request):
    global filecsv_name
    #folder_path = Path(folder_path)
    csv_file_path = os.path.join(settings.MEDIA_ROOT, 'csv_file')
    path_file_csv = os.path.join(csv_file_path, filecsv_name) 
    csv_infor = read_csv_file(path_file_csv)
    data_detail = convert_csv_to_dataframe(path_file_csv)
    # Lấy ra tổng số email trong DataFrame
    total_emails = data_detail.shape[0]
     # Đếm số lượng email thư rác
    spam_count = count_spam_emails(data_detail)

    # Lấy tất cả các email gửi thư có số lần gửi nhiều nhất
    from_max_count = data_detail['From'].value_counts().max()
    from_emails_max = data_detail['From'].value_counts().index[data_detail['From'].value_counts() == from_max_count].tolist()
    # Lấy tất cả các email nhận thư có số lần nhận nhiều nhất
    to_max_count = data_detail['To'].value_counts().max()
    to_emails_max = data_detail['To'].value_counts().index[data_detail['To'].value_counts() == to_max_count].tolist()
    
    # Lấy danh sách email gửi thư cách nhau bằng dấu ", "
    list_sender_email = ", ".join(data_detail['Sender_email'].unique())
    # Lấy danh sách email nhận thư cách nhau bằng dấu ", "
    list_to_email = ", ".join(data_detail['To'].unique())
    context = {
        'filecsv_name':filecsv_name,
        'csv_infor':csv_infor,
        'spam_count':spam_count,
        'total_emails':total_emails,
        'from_emails_max':from_emails_max,
        'from_max_count':from_max_count,
        'to_emails_max':to_emails_max,
        'to_max_count': to_max_count,
        'list_sender_email': list_sender_email,
        'list_to_email': list_to_email
        }
    return render(request,'app/emailcsvfile/csv_file.html',context)


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
    
def extract_email_address(request):
    global folder_name
    global path_file_export
    upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
    data=List_Infor_Email_Eml(upload_path)
    if not data:
        return redirect("base")
    else:
        context = {'list_email':data,'folder_name':folder_name}
        return render(request,'app/extract/email_address.html',context)
    
def extract_phone_number(request):
    global folder_name
    global path_file_export
    upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
    data=List_Infor_Email_Eml(upload_path)
    if not data:
        return redirect("base")
    else:
        context = {'list_email':data,'folder_name':folder_name}
        return render(request,'app/extract/phone_number.html',context)

def save_extract_email_address(request):
    global folder_name
    folder_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
    path_file_extract = os.path.join(settings.MEDIA_ROOT, 'extract/emailaddress.txt')
    data=List_Infor_Email_Eml(folder_path)
    if not data:
        return redirect("base")
    else:   
        if os.path.exists(path_file_extract):
            with open(path_file_extract, 'rb') as file:
                response = HttpResponse(file.read(), content_type='text')
                response['Content-Disposition'] = 'attachment; filename="'+folder_name+'_email_address.txt"'
                return response
        return HttpResponse('File not found.', status=404)
    
def save_extract_phone_number(request):
    global folder_name
    folder_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
    path_file_extract = os.path.join(settings.MEDIA_ROOT, 'extract/phonenumber.txt')
    data=List_Infor_Email_Eml(folder_path)
    if not data:
        return redirect("base")
    else:   
        if os.path.exists(path_file_extract):
            with open(path_file_extract, 'rb') as file:
                response = HttpResponse(file.read(), content_type='text')
                response['Content-Disposition'] = 'attachment; filename="'+folder_name+'_phone_number.txt"'
                return response
        return HttpResponse('File not found.', status=404)
    
def action_extract_email_address(request):
    select_from = request.GET.get('select_from')
    select_to = request.GET.get('select_to')
    select_cc = request.GET.get('select_cc')
    select_bcc = request.GET.get('select_bcc')
    
    global folder_name
    global path_file_export
    upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
    data = List_Infor_Email_Eml(upload_path)
    
    email_addresses_from = []  # Danh sách chứa địa chỉ email "From"
    email_addresses_to = []
    email_addresses_cc = []  
    email_addresses_bcc = []
    email_addresses = []
    if data:
        if(select_from == "true"):
            email_addresses_from = list_from_extract_email_address(upload_path)
        if(select_to == "true"):
            email_addresses_to = list_to_extract_email_address(upload_path)
        if(select_cc == "true"):
            email_addresses_cc = list_cc_extract_email_address(upload_path)
        if(select_bcc == "true"):
            email_addresses_bcc = list_bcc_extract_email_address(upload_path)
    # Tạo một set để lưu trữ các địa chỉ email duy nhất
    unique_email_addresses = set(email_addresses_from + email_addresses_to + email_addresses_cc + email_addresses_bcc)

    # Chuyển đổi set thành danh sách
    email_addresses = list(unique_email_addresses)

    extract_path = os.path.join(settings.MEDIA_ROOT, 'extract')
    extract_file_path = os.path.join(extract_path, 'emailaddress.txt')
    # Kiểm tra nếu thư mục chưa tồn tại
    if not os.path.exists(extract_path):
        # Tạo thư mục mới
        os.makedirs(extract_path)
    # Ghi danh sách email vào file
    with open(extract_file_path, 'w') as file:
        for email in email_addresses:
            file.write(email + '\n')

    # Chuyển đổi danh sách thành chuỗi JSON
    json_data = json.dumps(email_addresses)
    # Trả về JsonResponse
    return JsonResponse(json_data, safe=False)

def action_extract_phone_number(request):
    global folder_name
    global path_file_export
    upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
    data = List_Infor_Email_Eml(upload_path)
    phone_number =[]

    if data:
        phone_number = list_from_extract_phone_number(upload_path)
    # Tạo một set để lưu trữ các địa chỉ email duy nhất
    unique_phone_number = set(phone_number)

    # Chuyển đổi set thành danh sách
    list_phone_number = list(unique_phone_number)

    extract_path = os.path.join(settings.MEDIA_ROOT, 'extract')
    extract_file_path = os.path.join(extract_path, 'phonenumber.txt')
    # Kiểm tra nếu thư mục chưa tồn tại
    if not os.path.exists(extract_path):
        # Tạo thư mục mới
        os.makedirs(extract_path)
    # Ghi danh sách email vào file
    with open(extract_file_path, 'w') as file:
        for phone in list_phone_number:
            file.write(phone + '\n')

    # Chuyển đổi danh sách thành chuỗi JSON
    json_data = json.dumps(list_phone_number)
    # Trả về JsonResponse
    return JsonResponse(json_data, safe=False)

def view_content(request):
    if request.method == 'POST':
        folder = request.FILES.get('folder', None)
        if folder is not None:
            # folder_path = folder.temporary_file_path()
            # Xử lý đường dẫn của thư mục ở đây
            return HttpResponse(f'Đã chọn thư mục: {folder}')
    return render(request, 'app/home.html')

def clearfilefolders(request):
    clear_folder_in_media('uploads')
    clear_folder_in_media('export/csv')
    clear_folder_in_media('csv_file')
    clear_folder_in_media('export/html')
    clear_folder_in_media('extract')

    return redirect("base")

def base(request):
    clear_folder_in_media('uploads')
    clear_folder_in_media('export/csv')
    clear_folder_in_media('csv_file')
    clear_folder_in_media('export/html')
    clear_folder_in_media('extract')
    return render(request,'app/base.html')
