import requests
from bs4 import BeautifulSoup
import csv
import django
import os

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_scraping.settings")
django.setup()

from data.models import Leadership

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarybFriDF1iUKeDfsZ5',
    # 'Cookie': '_ga=GA1.3.1761002096.1695017427; _gid=GA1.3.653759949.1695017427; _ga=GA1.1.1761002096.1695017427; _gat_GSA_ENOR0=1; _ga_CSLL4ZEK4L=GS1.1.1695017427.1.1.1695017597.0.0.0',
    'Origin': 'https://department.va.gov',
    'Referer': 'https://department.va.gov/biographies/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}



base_url = 'https://department.va.gov/'

csv_file = open('va_department_bios.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Name', 'Department', 'Designation', 'Email', 'Contact No.'])  # CSV header

page_size = 10  # Number of records per page
total_records = None  # Total number of records, initialize to None to get it from the first response

while True:
    params = {
        'wpgb-ajax': 'refresh',
        '_load_more_bios': str(page_size),
    }

    data = '------WebKitFormBoundarybFriDF1iUKeDfsZ5\r\nContent-Disposition: form-data; name="wpgb"\r\n\r\n{"is_main_query":0,"main_query":[],"permalink":"https://department.va.gov/biographies/","facets":[6,7,9,11,12,14],"lang":"","id":2}\r\n------WebKitFormBoundarybFriDF1iUKeDfsZ5--\r\n'

    response = requests.post(base_url, params=params, headers=headers, data=data).json()

    data = response.get('posts')

    # Check if we have total_records yet, if not, extract it from the first response
    if total_records is None:
        total_records = int(response.get('total'))
        print(f"Total records: {total_records}")

    soup = BeautifulSoup(data, 'html.parser')

    Phone = ""
    Email = ""
    articles = soup.find_all('article')
    for article in articles:
        name = article.find('h2').text
        dep_element = article.find('div', {'class': 'wpgb-block-3 wpgb-idle-scheme-1'})
        dep = dep_element.text if dep_element else ""
        title = article.find('div', class_='wpgb-block-2').text


        print(name)
        csv_writer.writerow([name, dep, title, Email, Phone])

    # Check if a person with the same name already exists in the database
        existing_person = Leadership.objects.filter(name=name).first()

        if not existing_person:
            # If the person doesn't exist, create and save it
            leadership_instance = Leadership(name=name, dep=dep, title=title, email=Email, phone_number=Phone)
            leadership_instance.save()
        else:
            # If the person already exists, you can optionally update their information or handle it as needed
            print(f"Person '{name}' already exists.")

    if page_size >= total_records+10:
        break

    page_size += 10

# Close the CSV file
csv_file.close()

print("Data saved to 'va_department_bios.csv'.")