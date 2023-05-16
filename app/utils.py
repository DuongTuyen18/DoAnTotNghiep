import os
import csv
from django.core.files.storage import default_storage
from email.utils import parseaddr
from django.http import HttpResponse,FileResponse
from email.parser import Parser
from dateutil.parser import parse
from email.header import decode_header
import html2text
import tkinter as tk
from tkinter import filedialog
from django.conf import settings
import shutil
import re
import pandas as pd
import numpy as np
from pandas import DataFrame

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    return folder_path
def List_Infor_Email_Eml(folder_path):
    eml_files = [f for f in os.listdir(folder_path) if f.endswith('.eml')]
    data=[]
    for file_name in eml_files:
        eml_file_path = folder_path+'\\'+file_name
        with open(eml_file_path, 'rb') as eml_file:
            eml_data = eml_file.read()
        eml_message = Parser().parsestr(eml_data.decode('utf-8', errors='ignore'))
        from_email = eml_message['From']
        sender_name, sender_email = parseaddr(from_email)
        date_email = parse(eml_message['date']).strftime("%d/%m/%Y")
        subject_header = decode_header(eml_message['subject'])
        subject_decoded = ''
        for part in subject_header:
            if isinstance(part[0], bytes):
                subject_decoded += part[0].decode(part[1] or 'utf-8')
            else:
                subject_decoded += part[0]
        data.append({'file_name':file_name,'subject_email': subject_decoded, 'from_email' : sender_name, 'date_email' : date_email})
    return data

def Content_Email_Eml(file_path):
    with open(file_path, 'rb') as eml_file:
        eml_data = eml_file.read()
    eml_message = Parser().parsestr(eml_data.decode('utf-8', errors='ignore'))
    # Lấy phần nội dung của email và chuyển đổi nó thành HTML
    email_content = ''
    for part in eml_message.walk():
        content_type = part.get_content_type()
        charset = part.get_charset()
        # if content_type == 'text/plain' or content_type == 'text/html':
        # HIỆN TẠI CHỈ DÙNG TEXT/HTML
        if content_type == 'text/html':
            if charset:
                email_content += part.get_payload(decode=True).decode(charset)
            else:
                email_content += part.get_payload(decode=True).decode('utf-8', errors='ignore')
    return email_content

def read_csv_file(csv_file_path):
    if os.path.exists(csv_file_path):
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = ''
            for row in reader:
                data += ','.join(row) + '\n'
        return data
    # data = pd.read_csv(csv_file_path)
    # # Chuẩn hóa dữ liệu, dùng biến data_detail để lưu dữ liệu cần thiết
    # arr_message_detail = []
    # for item in data.message:
    #     x=re.split(r'Message-ID: |\nDate: |\nFrom: |\nTo: |\nSubject: |\nMime-Version: |\nContent-Type: |\nContent-Transfer-Encoding: |\nCc: |\nBcc: |\n\n', item,maxsplit=11)
    #     del x[0]
    #     del x[10]
    #     arr_message_detail.append(x)
    # data_detail = DataFrame(arr_message_detail, columns=['MassageID','Date','From','To','Subject','MimeVersion','ContentType','ContentTransferEncoding','Xcc','Xbcc'])
    # data_detail.insert(loc=0, column="file",value=np.array(data.file))
    # tmt=[]
    # for item in data_detail['Date']:
    #     tmt.append(item[:-12])
    # data_detail['Date']=tmt
    # data_detail['Date']= pd.to_datetime(data_detail.Date)   
    # return data_detail
def convert_csv_to_datafarm(csv_file_path):
    data = pd.read_csv(csv_file_path)
    # Chuẩn hóa dữ liệu, dùng biến data_detail để lưu dữ liệu cần thiết
    arr_message_detail = []
    for item in data.message:
        x=re.split(r'Message-ID: |\nDate: |\nFrom: |\nTo: |\nSubject: |\nMime-Version: |\nContent-Type: |\nContent-Transfer-Encoding: |\nCc: |\nBcc: |\n\n', item,maxsplit=11)
        del x[0]
        del x[10]
        arr_message_detail.append(x)
    data_detail = DataFrame(arr_message_detail, columns=['MassageID','Date','From','To','Subject','MimeVersion','ContentType','ContentTransferEncoding','Xcc','Xbcc'])
    data_detail.insert(loc=0, column="file",value=np.array(data.file))
    tmt=[]
    for item in data_detail['Date']:
        tmt.append(item[:-12])
    data_detail['Date']=tmt
    data_detail['Date']= pd.to_datetime(data_detail.Date)   
    return data_detail

def inforEmail(file_path):
    with open(file_path, 'rb') as eml_file:
        eml_data = eml_file.read()
    eml_message = Parser().parsestr(eml_data.decode('utf-8', errors='ignore'))
    hex_data = ''.join(['{:02x}'.format(byte) for byte in eml_data])

    # Hiển thị hex view theo yêu cầu
    hex_view = '<table  id="table_hexview">'
    hex_view += '<thead><tr><th></th><th>00</th><th>01</th><th>02</th><th>03</th><th>04</th><th>05</th><th>06</th><th>07</th><th>08</th><th>09</th><th>0a</th><th>0b</th><th>0c</th><th>0d</th><th>0e</th><th>0f</th></tr></thead>'
    for i in range(0, len(hex_data), 32):
        k = i//2
        row = hex_data[i:i+32]
        row_spaces = ' '.join([row[j:j+2] for j in range(0, len(row), 2)])
        row_cells = [f'<td style="padding-right:20px">{c}</td>' for c in ['{:08x}'.format(k)] + row_spaces.split()]
        hex_view += '<tr>' + ''.join(row_cells) + '</tr>'
    hex_view += '</table>'
    message_header = eml_message.items()
    to = eml_message['To']
    if to is None:
        to = ''
    cc = eml_message['CC']
    if cc is None:
        cc = ''
    from_email = eml_message['From']
    sender_name, sender_email = parseaddr(from_email)
    date_email = parse(eml_message['date']).strftime("%d/%m/%Y")
    subject_header = decode_header(eml_message['subject'])
    subject_decoded = ''
    for part in subject_header:
        if isinstance(part[0], bytes):
            subject_decoded += part[0].decode(part[1] or 'utf-8')
        else:
            subject_decoded += part[0]
    email_content = ''
    for part in eml_message.walk():
        content_type = part.get_content_type()
        charset = part.get_charset()
        # if content_type == 'text/plain' or content_type == 'text/html':
        # HIỆN TẠI CHỈ DÙNG TEXT/HTML
        if content_type == 'text/html':

            if charset:
                email_content += part.get_payload(decode=True).decode(charset)
            else:
                email_content += part.get_payload(decode=True).decode('utf-8', errors='ignore')
    data = {'file_name': file_path,'message_header':message_header,'hex_data':hex_view,'subject_email': subject_decoded, 'from_email' : from_email, 'sender_name' : sender_name, 'date_email' : date_email,'to':to,'cc':cc, 'email_content' : email_content}
    return data

def clear_folder_in_media(folder_name):
    # Lấy đường dẫn tuyệt đối đến thư mục folder_name
    folder_path = os.path.join(settings.MEDIA_ROOT, folder_name)
    # Xóa toàn bộ các file trong thư mục folder_name 
    shutil.rmtree(folder_path)
    # Tạo lại thư mục folder_name trống
    os.mkdir(folder_path)

def convert_eml_to_csv(upload_path,export_path, folder_name):
    list_eml_files = [f for f in os.listdir(upload_path) if f.endswith('.eml')]
    data=[]
    # Tạo đường dẫn và tên file CSV
    csv_file_name =folder_name+'.csv'
    csv_file_path = os.path.join(export_path, csv_file_name)
    columns = ['file', 'message']
    # Ghi dữ liệu vào file CSV
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(columns)
        for file_name in list_eml_files:
            eml_file_path = upload_path+ "\\"+ file_name
            with open(eml_file_path, 'rb') as eml_file:
                eml_data = eml_file.read()
            eml_message = Parser().parsestr(eml_data.decode('utf-8', errors='ignore'))
            # Lấy thông tin từ EML
            message_id = eml_message['Message-ID']
            date = eml_message['Date']
            from_email = eml_message['From']
            to_email = eml_message['To']
            subject = decode_header(eml_message['subject'])
            subject_decoded = ''
            for part in subject:
                if isinstance(part[0], bytes):
                    subject_decoded += part[0].decode(part[1] or 'utf-8')
                else:
                    subject_decoded += part[0]
            mime_version = eml_message['Mime-Version']
            content_type = eml_message['Content-Type']
            content_encoding = eml_message['Content-Transfer-Encoding']
            x_cc = eml_message.get('Cc', '')
            x_bcc = eml_message.get('Bcc', '')
            email_content = ''
            for part in eml_message.walk():
                if part.get_content_type() in ["text/plain", "text/html"]:
                    # Lấy nội dung của phần tử
                    part_content = part.get_payload(decode=True).decode('utf-8')
                    # Chuyển đổi nội dung HTML thành văn bản thuần túy
                    text_content = html2text.html2text(part_content)
                    # Thêm nội dung vào biến lưu trữ
                    email_content += text_content
            csv_row = f'{"Message-ID"}: {message_id}\n{"Date"}: {date}\n{"From"}: {from_email}\n{"To"}: {to_email}\n{"Subject"}: {subject_decoded}\n{"Mime-Version"}: {mime_version}\n{"Content-Type"}: {content_type}\n{"Content-Transfer-Encoding"}: {content_encoding}\n{"Cc"}: {x_cc}\n{"Bcc"}: {x_bcc}\n\n{email_content}'
            # Định dạng thành chuỗi tương ứng
            writer.writerow([file_name, csv_row])   
    return  csv_file_path
    # Lưu file CSV vào thư mục đã chọn trên máy tính

    # with open(csv_file_path, 'rb') as file:
    #     shutil.copy(csv_file_path, "D:\\hoc tap\\")
