import os
import csv
from django.core.files.storage import default_storage
from email.utils import parseaddr
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
<<<<<<< HEAD
from urllib.parse import unquote
import html
import email
import pdfkit 
import tempfile
import PyPDF2
from pdfminer.high_level import extract_text
from email import message_from_file
import fitz
from email.policy import default
from email import message_from_bytes 
from email import message_from_string
from pdfdocument.document import PDFDocument
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from io import BytesIO
from fpdf import FPDF
from email.message import EmailMessage
from email.header import decode_header
from html import escape
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from bs4 import BeautifulSoup
import eml_parser
from eml_parser import EMLParser

=======
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import networkx as nx
from django.shortcuts import render
import json
import requests
import email
from bs4 import BeautifulSoup
def check_email_availability(email):
    api_key = 'live_bfb97de3d118e4b8ac6010a039896ce86006f099602baebf48bf0604edbba589'
    url = f'https://api.kickbox.com/v2/verify?email={email}&apikey={api_key}'

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        if data['result'] == 'deliverable':
            return True
        else:
            return False
    else:
        return False
    
>>>>>>> 53a6da94dd4f15560221dcbf58e6e04500558761
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
        if(sender_name == ""):
            sender_name = sender_email
        decoded_name = decode_header(sender_name)[0][0]
        if isinstance(decoded_name, bytes):
            sender_name = decoded_name.decode()
        else:
            sender_name = decoded_name
        date_email = parse(eml_message['date']).strftime("%d/%m/%Y")
        subject_header = decode_header(eml_message['subject'])
        subject_decoded = ''
        for part in subject_header:
            if isinstance(part[0], bytes):
                subject_decoded += part[0].decode(part[1] or 'utf-8')
            else:
                subject_decoded += part[0]
        data.append({'file_name':file_name,'subject_email': subject_decoded, 'sender_name' : sender_name, 'date_email' : date_email})
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
<<<<<<< HEAD
    
def read_pdf(file_path):
    text = extract_text(file_path)
    print(text)
    
=======

def list_to_by_from(data_detail,sender_email):
    filtered_data = data_detail[data_detail['Sender_email'] == sender_email]
    grouped_data = filtered_data.groupby(['Sender_email', 'To']).size().reset_index(name='Count')

    result_list = []
    for index, row in grouped_data.iterrows():
        sender = row['Sender_email']
        to = row['To']
        count = row['Count']
        result_list.append({'sender_email': sender, 'to': to, 'counts': count})
    return result_list


>>>>>>> 53a6da94dd4f15560221dcbf58e6e04500558761
def get_list_from(data_detail):
    list_from = data_detail.groupby(['Sender_name', 'Sender_email']).size().reset_index()
    list_from.columns = ['sender_name', 'sender_email', 'counts']
    return list_from

def get_list_to(data_detail):
    list_from = data_detail.To.value_counts().reset_index()
    list_from.columns = ['to', 'counts']
    return list_from

def get_list_from_and_to(data_detail):
    sender_emails = data_detail['Sender_email'].unique()
    to_emails = data_detail['To'].unique()
    # Kết hợp và loại bỏ giá trị trùng nhau
    unique_emails = set(sender_emails).union(set(to_emails))
    return unique_emails

def get_data_day_statistical(data_detail):
    data_day_statistical=pd.DataFrame()
    day_statistical = pd.DataFrame()
    data_day_statistical["Day"]=data_detail['Date'].apply(lambda x: x.day)
    day_statistical["Day"]=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
    day_statistical["counts"] = day_statistical["Day"].map(data_day_statistical["Day"].value_counts())
    day_statistical["counts"] = day_statistical["counts"].fillna(0)
    return day_statistical

def get_data_month_statistical(data_detail):
    data_month_statistical=pd.DataFrame()
    month_statistical = pd.DataFrame()
    data_month_statistical["Month"]=data_detail['Date'].apply(lambda x: x.month)
    month_statistical["Month"]=[1,2,3,4,5,6,7,8,9,10,11,12]
    month_statistical["counts"] = month_statistical["Month"].map(data_month_statistical["Month"].value_counts())
    month_statistical["counts"] = month_statistical["counts"].fillna(0)
    return month_statistical

def get_data_year_statistical(data_detail):
    data_year_statistical=pd.DataFrame()
    year_statistical = pd.DataFrame()
    data_year_statistical["Year"]=data_detail['Date'].apply(lambda x: x.year)
    year_statistical["Year"]=pd.Series(range(min(data_year_statistical["Year"]), max(data_year_statistical["Year"]) + 1))
    year_statistical["counts"] = year_statistical["Year"].map(data_year_statistical["Year"].value_counts())
    year_statistical["counts"] = year_statistical["counts"].fillna(0)
    return year_statistical

def wordcloud_view(data_detail):
    # Chuỗi văn bản đầu vào
    text = ' '.join(data_detail['Content'])
    # Tạo Word Cloud
    wordcloud = WordCloud(width=750, height=400, background_color='white').generate(text)
    # Lưu Word Cloud vào một đối tượng BytesIO
    image_stream = BytesIO()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(image_stream, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    # Đọc dữ liệu từ đối tượng BytesIO và mã hóa base64
    image_stream.seek(0)
    image_data = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    return image_data

def convert_graph_to_json(graph):
    # Convert graph to dictionary representation
    graph_data = nx.node_link_data(graph)
    # Serialize the dictionary to JSON string
    json_data = json.dumps(graph_data)
    return json_data


def create_link_analysis(data_detail):
    # Xác định danh sách các liên kết
    links = data_detail[['Sender_email', 'To']].values.tolist()
    # Đếm số lần xuất hiện của mỗi liên kết
    link_counts = pd.DataFrame(links, columns=['Sender_email', 'To']).value_counts()
    # Tạo đồ thị
    G = nx.Graph()
    # Thêm các nút (nodes) và cạnh (edges) vào đồ thị
    for link in links:
        sender_email, to = link
        G.add_edge(sender_email, to)
    return G,link_counts

def find_links_by_emails(data_detail, email_list):
    # Tạo một danh sách chứa tất cả các email trong email_list
    all_emails = set(email_list)
    # Tạo đồ thị và thêm các email trong danh sách này vào đồ thị là các nút
    G = nx.Graph()
    G.add_nodes_from(all_emails)

    # Lọc ra các dòng có email trong danh sách email đã cho
    filtered_data = data_detail[data_detail['Sender_email'].isin(email_list) | data_detail['To'].isin(email_list)]
    # Xác định danh sách các liên kết chỉ giữa các email trong email_list
    links = filtered_data[filtered_data['Sender_email'].isin(email_list) & filtered_data['To'].isin(email_list)][['Sender_email', 'To']].values.tolist()
    # Đếm số lần xuất hiện của mỗi liên kết chỉ giữa các email trong email_list
    link_counts = pd.DataFrame(links, columns=['Sender_email', 'To']).value_counts()
    
    # Thêm các liên kết chỉ giữa các email trong email_list vào đồ thị là các cạnh
    for link in links:
        sender_email, to = link
        G.add_edge(sender_email, to)

    return G, link_counts



def convert_csv_to_dataframe(csv_file_path):
    data = pd.read_csv(csv_file_path)
    # Chuẩn hóa dữ liệu, dùng biến data_detail để lưu dữ liệu cần thiết
    arr_message_detail = []
    for item in data.message:
        x=re.split(r'Message-ID: |\nDate: |\nFrom: |\nSender_name: |\nSender_email: |\nTo: |\nSubject: |\nMime-Version: |\nContent-Type: |\nContent-Transfer-Encoding: |\nCc: |\nBcc: |\nContent: |\n\n', item,maxsplit=14)
        del x[0]
        del x[13]
        arr_message_detail.append(x)
    data_detail = DataFrame(arr_message_detail, columns=['MassageID','Date','From','Sender_name','Sender_email','To','Subject','MimeVersion','ContentType','ContentTransferEncoding','Xcc','Xbcc','Content'])
    data_detail.insert(loc=0, column="file",value=np.array(data.file))
    tmt=[]
    for item in data_detail['Date']:
        tmt.append(item[:-12])
    data_detail['Date']=tmt
    data_detail['Date']= pd.to_datetime(data_detail.Date)   
    return data_detail

def extract_email(to_email):
    if to_email is None:
        return None
    email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+')  # Mẫu tìm kiếm địa chỉ email
    match = email_pattern.search(to_email)
    
    if match:
        return match.group()  # Trả về địa chỉ email tìm thấy
    else:
        return None  # Không tìm thấy địa chỉ email
    
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
    delivered_to = eml_message['Delivered-To']
    to = eml_message['To']
    if to is None and delivered_to is not None:
        to = delivered_to
    to = extract_email(to)
    if to is None:
        to=''
    cc = eml_message['CC']
    if cc is None:
        cc = ''
    from_email = eml_message['From']
    sender_name, sender_email = parseaddr(from_email)
    decoded_name = decode_header(sender_name)[0][0]
    if isinstance(decoded_name, bytes):
        sender_name = decoded_name.decode()
    else:
        sender_name = decoded_name
    if(sender_name==""):
        from_email ="<" + sender_email + ">"
    else:
        from_email = sender_name +" "+ "<" + sender_email + ">"
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
            sender_name, sender_email = parseaddr(from_email)
            if(sender_name == ""):
                sender_name = sender_email
            decoded_name = decode_header(sender_name)[0][0]
            if isinstance(decoded_name, bytes):
                sender_name = decoded_name.decode()
            else:
                sender_name = decoded_name
            from_email = sender_name +" "+ "<" + sender_email + ">"

            # to_email = eml_message['To']
            # to_email = extract_email(to_email)
            delivered_to = eml_message['Delivered-To']
            to_email = eml_message['To']
            if to_email is None and delivered_to is not None:
                to_email = delivered_to
            to_email = extract_email(to_email)
            if to_email is None:
                to_email=''
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
            csv_row = f'{"Message-ID"}: {message_id}\n{"Date"}: {date}\n{"From"}: {from_email}\n{"Sender_name"}: {sender_name}\n{"Sender_email"}: {sender_email}\n{"To"}: {to_email}\n{"Subject"}: {subject_decoded}\n{"Mime-Version"}: {mime_version}\n{"Content-Type"}: {content_type}\n{"Content-Transfer-Encoding"}: {content_encoding}\n{"Cc"}: {x_cc}\n{"Bcc"}: {x_bcc}\n{"Content"}: {email_content}'
            # Định dạng thành chuỗi tương ứng
            writer.writerow([file_name, csv_row])   
    return  csv_file_path

<<<<<<< HEAD
    # with open(csv_file_path, 'rb') as file:
    #     shutil.copy(csv_file_path, "D:\\hoc tap\\")

def decode_subject(subject):
    decoded_subject = ''
    for part, encoding in decode_header(subject):
        if isinstance(part, bytes):
            if encoding is None:
                decoded_subject += part.decode('utf-8')
            else:
                decoded_subject += part.decode(encoding)
        else:
            decoded_subject += part
    return decoded_subject



def decode_subject(subject):
    decoded_subject = ''
    for part, encoding in decode_header(subject):
        if isinstance(part, bytes):
            if encoding is None:
                decoded_subject += part.decode('utf-8')
            else:
                decoded_subject += part.decode(encoding)
        else:
            decoded_subject += part
    return decoded_subject

def convert_eml_to_pdf(eml_file, pdf_file):
    with open(eml_file, 'r', encoding='utf-8') as file:
        eml_parser = EMLParser(eml_file)
        eml_data = eml_parser.decode_email()

    # Tạo tệp PDF mới
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="converted.pdf"'

    # Tạo canvas PDF
    p = canvas.Canvas(response, pagesize=letter)

    # Ghi nội dung EML lên canvas PDF
    p.drawString(100, 700, 'From: ' + eml_data['header']['from'])
    p.drawString(100, 680, 'To: ' + eml_data['header']['to'])
    # Ghi thêm thông tin khác từ eml_data vào canvas PDF theo yêu cầu

    # Lưu và hoàn thành tệp PDF
    p.showPage()
    p.save()

    return response


def convert_eml_files_to_pdf(upload_path, export_path, folder_name):
    # Create a list of EML files in the folder
    list_eml_files = [f for f in os.listdir(upload_path) if f.endswith('.eml')]

    pdf_folder_path = os.path.join(export_path, folder_name)

    # Create the folder if it doesn't exist
    os.makedirs(pdf_folder_path, exist_ok=True)

    # Iterate through the list of EML files and convert each to PDF
    for eml_file in list_eml_files:
        eml_file_path = os.path.join(upload_path, eml_file)
        pdf_file_name = eml_file.replace('.eml', '.pdf')
        pdf_file_path = os.path.join(pdf_folder_path, pdf_file_name)
        convert_eml_to_pdf(eml_file_path, pdf_file_path)

    return pdf_folder_path

def decode_content(part):
    if part.get_content_charset():
        return part.get_payload(decode=True).decode(part.get_content_charset())
    else:
        return part.get_payload()

def convert_eml_to_html(eml_file, html_file):
    with open(eml_file, 'r', encoding='utf-8') as file:
        eml_content = file.read()

    msg = email.message_from_string(eml_content)

    # Extract From, To, Subject, Received On
    sender = msg.get('From')
    recipient = msg.get('To')
    subject = msg.get('Subject')
    received_on = msg.get('Date')

    # Extract HTML content from the body
    html_content = ''
    for part in msg.walk():
        content_type = part.get_content_type()
        if content_type == 'text/html':
            html_content = decode_content(part)
            break

    # Build the HTML content
    html_content = f'''
        <p><strong>From:</strong> {sender}</p>
        <p><strong>To:</strong> {recipient}</p>
        <p><strong>Subject:</strong> {subject}</p>
        <p><strong>Received On:</strong> {received_on}</p>
        <hr />
        <div>{html_content}</div>
    '''

    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

def convert_eml_files_to_html(upload_path, export_path, folder_name):
    # Tạo một danh sách các tệp EML trong thư mục
    list_eml_files = [f for f in os.listdir(upload_path) if f.endswith('.eml')]

    html_folder_path = os.path.join(export_path, folder_name)
    if not os.path.exists(html_folder_path):
        os.makedirs(html_folder_path)           

    # Lặp qua danh sách tệp EML và chuyển đổi thành tệp HTML
    for eml_file in list_eml_files:
        eml_file_path = os.path.join(upload_path, eml_file)
        html_file_name = eml_file.replace('.eml', '.html')
        html_file_path = os.path.join(html_folder_path, html_file_name)
        convert_eml_to_html(eml_file_path, html_file_path)

    return html_folder_path

def convert_eml_to_text(eml_file, txt_file):
    with open(eml_file, 'r', encoding='utf-8') as file:
        eml_content = file.read()

    msg = email.message_from_string(eml_content)

    # Extract From, To, Subject, Received On
    sender = msg.get('From')
   
    recipient = msg.get('To')
    
    subject = msg.get('Subject')
    subject = decode_subject(subject)  # Decode the subject

    received_on = msg.get('Date')
    
    # Extract HTML or plain text content from the body
    txt_content = ''
    for part in msg.walk():
        content_type = part.get_content_type()
        if content_type == 'text/html':
            txt_content = decode_content(part)
            break
        elif content_type == 'text/plain':
            plain_text_content = decode_content(part)
            txt_content = f'<pre>{escape(plain_text_content)}</pre>'
            break

    # Build the HTML content
    txt_content = f'''
        From: {sender}
        To: {recipient}
        Subject: {subject}
        Received On: {received_on}
        
        {txt_content}
    '''

    with open(txt_file, 'w', encoding='utf-8') as file:
        file.write(txt_content)


def convert_eml_files_to_text(upload_path, export_path, folder_name):
    # Tạo một danh sách các tệp EML trong thư mục
    list_eml_files = [f for f in os.listdir(upload_path) if f.endswith('.eml')]

    text_folder_path = os.path.join(export_path, folder_name)

    # Tạo thư mục nếu nó chưa tồn tại
    os.makedirs(text_folder_path, exist_ok=True)

    # Lặp qua danh sách tệp EML và chuyển đổi thành tệp văn bản
    for eml_file in list_eml_files:
        eml_file_path = os.path.join(upload_path, eml_file)
        text_file_name = eml_file.replace('.eml', '.txt')
        text_file_path = os.path.join(text_folder_path, text_file_name)
        convert_eml_to_text(eml_file_path, text_file_path)

    return text_folder_path
=======

def convert_eml_to_html(upload_path,html_folder_path):
    list_eml_files = [f for f in os.listdir(upload_path) if f.endswith('.eml')]
    for file_name in list_eml_files:
        eml_file_path = upload_path+ "\\"+ file_name
        # Đọc file EML
        with open(eml_file_path, 'r') as file:
            eml_content = file.read()

        # Phân tích cấu trúc EML
        msg = email.message_from_string(eml_content)

        # Trích xuất nội dung HTML từ EML
        html_content = None
        for part in msg.walk():
            if part.get_content_type() == 'text/html':
                html_content = part.get_payload(decode=True).decode('utf-8')
                break
        if html_content is None:
            continue
        else:
            # Chuyển đổi các thẻ HTML không hợp lệ thành chuỗi hợp lệ
            soup = BeautifulSoup(html_content, 'html.parser')
            html_content_valid = str(soup)

        # Tạo tên file HTML từ tên file EML
        file_name_html = os.path.splitext(file_name)[0] + '.html'
        


        # Tạo đường dẫn đầy đủ cho file HTML đích
        html_file_path = os.path.join(html_folder_path, file_name_html)
        
        # Ghi nội dung HTML vào file HTML đích
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write(html_content_valid)
    return html_file_path
>>>>>>> 53a6da94dd4f15560221dcbf58e6e04500558761
