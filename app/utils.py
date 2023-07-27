import os
import csv
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

def list_from_by_to(data_detail,received_emails):
    filtered_data = data_detail[data_detail['To'] == received_emails]
    grouped_data = filtered_data.groupby(['Sender_email', 'To']).size().reset_index(name='Count')
    result_list = []
    for index, row in grouped_data.iterrows():
        sender = row['Sender_email']
        to = row['To']
        count = row['Count']
        result_list.append({'sender_email': sender, 'to': to, 'counts': count})
    return result_list

def get_list_from(data_detail):
    list_from = data_detail.groupby(['Sender_name', 'Sender_email']).size().reset_index()
    list_from.columns = ['sender_name', 'sender_email', 'counts']
    return list_from

def get_list_to(data_detail):
    list_from = data_detail.To.value_counts().reset_index()
    list_from.columns = ['to', 'counts']
    return list_from

def get_list_from_and_to(data_detail, keyword_search=None):
    sender_emails = data_detail['Sender_email'].unique()
    to_emails = data_detail['To'].unique()
    # Nếu có từ khóa tìm kiếm, lọc danh sách các email chứa từ khóa
    if keyword_search:
        sender_emails = [email for email in sender_emails if keyword_search.lower() in email.lower()]
        to_emails = [email for email in to_emails if keyword_search.lower() in email.lower()]

    # Kết hợp và loại bỏ giá trị trùng nhau
    unique_emails = set(sender_emails).union(set(to_emails))
    return unique_emails

def count_emails_sent_by_email(data_detail, email):
    return data_detail[data_detail['Sender_email'] == email].shape[0]

def count_emails_received_by_email(data_detail, email):
    return data_detail[data_detail['To'] == email].shape[0]

def find_most_received_emails(data_detail, email):
    # Lọc các dòng có giá trị cột "From" bằng với email
    sent_emails = data_detail[data_detail['Sender_email'] == email]
    # Tính số lần thư gửi đến tương ứng với từng email
    received_counts = sent_emails['To'].value_counts()
    # Lấy số lần gửi đến lớn nhất
    most_received_count = received_counts.max()
    # Lọc danh sách các email có số lần gửi đến bằng với số lần gửi đến lớn nhất
    most_received_emails = received_counts[received_counts == most_received_count].index.tolist()
    return most_received_emails, most_received_count

def find_most_sent_emails(data_detail, email):
    # Lọc các dòng có giá trị cột "To" bằng với email
    sent_emails = data_detail[data_detail['To'] == email]
    # Tính số lần thư được nhận tương ứng với từng email
    sent_counts = sent_emails['Sender_email'].value_counts()
    # Lấy số lần được nhận lớn nhất
    most_sent_count = sent_counts.max()
    # Lọc danh sách các email có số lần được nhận bằng với số lần được nhận lớn nhất
    most_sent_emails = sent_counts[sent_counts == most_sent_count].index.tolist()
    return most_sent_emails, most_sent_count

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
    # Add link_counts to the graph_data dictionary
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
        count = link_counts[(link_counts.index.get_level_values('Sender_email') == sender_email) & (link_counts.index.get_level_values('To') == to)].values[0]
        print(f"Sender_email: {sender_email}, To: {to}, Count: {count}")
        G.add_edge(sender_email, to)
        G.edges[sender_email, to]['count'] = count
    return G, link_counts

def is_spam_email(email):
    # Các quy tắc đơn giản để phát hiện email thư rác
    # Các quy tắc này có thể không hoạt động tốt với mọi loại email thư rác và email hợp lệ
    spam_keywords = ['lottery', 'win', 'free', 'promotion', 'prize', 'money', 'discount', 'urgent', 'viagra']
    spam_threshold = 2  # Ngưỡng số lượng từ thư rác xuất hiện trong nội dung email

    # Chuyển đổi nội dung email thành chữ thường để so sánh dễ dàng hơn
    email = email.lower()

    # Đếm số lượng từ thư rác xuất hiện trong nội dung email
    spam_count = sum(keyword in email for keyword in spam_keywords)

    # Kiểm tra xem số lượng từ thư rác có vượt qua ngưỡng hay không
    return spam_count >= spam_threshold

def count_spam_emails(data_frame):
    # Biến đếm số lượng email thư rác
    spam_count = 0

    # Lặp qua từng dòng trong DataFrame
    for index, row in data_frame.iterrows():
        # Lấy nội dung email từ cột 'email_content'
        email_content = row['Content']

        # Kiểm tra xem email có phải là thư rác hay không
        if is_spam_email(email_content):
            spam_count += 1

    return spam_count


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

def list_from_extract_email_address(upload_path):
    list_eml_files = [f for f in os.listdir(upload_path) if f.endswith('.eml')]
    email_addresses = set() # Sử dụng set để loại bỏ các địa chỉ email trùng nhau
    for file_name in list_eml_files:
        eml_file_path = os.path.join(upload_path, file_name)
        # Đọc file EML
        with open(eml_file_path, 'rb') as file:
            eml_data = file.read()
        eml_message = Parser().parsestr(eml_data.decode('utf-8', errors='ignore'))
        from_email = eml_message['From']
        sender_name, sender_email = parseaddr(from_email)
        if sender_name == "":
            sender_name = sender_email
        decoded_name = decode_header(sender_name)[0][0]
        if isinstance(decoded_name, bytes):
            sender_name = decoded_name.decode()
        else:
            sender_name = decoded_name
        from_email = sender_name + " <" + sender_email + ">"
        # Thêm địa chỉ email vào set
        email_addresses.add(sender_email)
    
    # Chuyển đổi set thành danh sách
    email_addresses_list = list(email_addresses)
    return email_addresses_list



def list_to_extract_email_address(upload_path):
    list_eml_files = [f for f in os.listdir(upload_path) if f.endswith('.eml')]
    email_addresses = set()  # Sử dụng set để loại bỏ các địa chỉ email trùng nhau
    for file_name in list_eml_files:
        eml_file_path = os.path.join(upload_path, file_name)
        # Đọc file EML
        with open(eml_file_path, 'rb') as file:
            eml_data = file.read()
        eml_message = Parser().parsestr(eml_data.decode('utf-8', errors='ignore'))
        delivered_to = eml_message['Delivered-To']
        to_email = eml_message['To']
        if to_email is None and delivered_to is not None:
            to_email = delivered_to
        to_email = extract_email(to_email)
        if to_email is None:
            to_email=''
        # Thêm địa chỉ email vào set
        email_addresses.add(to_email)
    # Chuyển đổi set thành danh sách
    email_addresses_list = list(email_addresses)
    return email_addresses_list

def list_cc_extract_email_address(upload_path):
    list_eml_files = [f for f in os.listdir(upload_path) if f.endswith('.eml')]
    email_addresses = set() # Sử dụng set để loại bỏ các địa chỉ email trùng nhau
    for file_name in list_eml_files:
        eml_file_path = os.path.join(upload_path, file_name)
        # Đọc file EML
        with open(eml_file_path, 'rb') as file:
            eml_data = file.read()
        eml_message = Parser().parsestr(eml_data.decode('utf-8', errors='ignore'))
        x_cc = eml_message.get('Cc', '')
        # Thêm địa chỉ email vào set
        if(x_cc!=''):
            email_addresses.add(x_cc)
    # Chuyển đổi set thành danh sách
    email_addresses_list = list(email_addresses)
    return email_addresses_list

def list_bcc_extract_email_address(upload_path):
    list_eml_files = [f for f in os.listdir(upload_path) if f.endswith('.eml')]
    email_addresses = set()  # Sử dụng set để loại bỏ các địa chỉ email trùng nhau
    for file_name in list_eml_files:
        eml_file_path = os.path.join(upload_path, file_name)
        # Đọc file EML
        with open(eml_file_path, 'rb') as file:
            eml_data = file.read()
        eml_message = Parser().parsestr(eml_data.decode('utf-8', errors='ignore'))
        x_bcc = eml_message.get('Bcc', '')
        # Thêm địa chỉ email vào set
        if(x_bcc!=''):
            email_addresses.add(x_bcc)
    # Chuyển đổi set thành danh sách
    email_addresses_list = list(email_addresses)
    return email_addresses_list

import re

def list_from_extract_phone_number(upload_path):
    list_eml_files = [f for f in os.listdir(upload_path) if f.endswith('.eml')]
    phone_numbers = set()
    phone_number_patterns = [
        r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # XXX-XXX-XXXX hoặc XXX.XXX.XXXX hoặc XXX XXX XXXX
        r'\b\(\d{3}\)\s?\d{3}[-.\s]?\d{4}\b',  # (XXX) XXX-XXXX hoặc (XXX)XXX-XXXX hoặc (XXX) XXX.XXXX
        r'\b\+\d{1,3}\s?\d{2,3}[-.\s]?\d{3,4}[-.\s]?\d{4}\b',  # +XXX XXX-XXXX hoặc +XXX-XXX-XXXX hoặc +XXX XXX.XXXX hoặc +XXX.XXX.XXXX
        # Thêm các định dạng khác tùy vào quy chuẩn số điện thoại của bạn
    ]

    for file_name in list_eml_files:
        eml_file_path = os.path.join(upload_path, file_name)
        # Đọc file EML
        with open(eml_file_path, 'rb') as file:
            eml_data = file.read()
        eml_message = Parser().parsestr(eml_data.decode('utf-8', errors='ignore'))
   
        # Tìm các số điện thoại trong nội dung EML
        for part in eml_message.walk():
            if part.get_content_type() == 'text/plain' or part.get_content_type() == 'text/html':
                content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                # Sử dụng regular expression để tìm các số điện thoại trong nội dung
                for phone_number_pattern in phone_number_patterns:
                    phone_numbers_found = re.findall(phone_number_pattern, content)
                    phone_numbers.update(phone_numbers_found)
    
    # Chuyển đổi set thành danh sách
    phone_number_list = list(phone_numbers)
    return phone_number_list

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
    return html_folder_path