import requests
from bs4 import BeautifulSoup
import csv
import django
import os

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_scraping.settings")
django.setup()

from data.models import Leadership

# Function to scrape data from the current page
def scrape_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        divs = soup.find_all('div', {"class": 'leadership-row'})

        # Initialize a list to store the extracted data
        data = []

        for div in divs:
            name = div.find('h3', {"class": 'leader-name'}).text
            destination = div.find('div', {'class': 'leader-title'}).text
            data.append([name, destination])

        return data, soup  # Return both the data and the soup object

    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        return [], None

# Define the URL and CSV file name
base_url = "https://www.commerce.gov/about/leadership?q=/about/leadership&page="
csv_file = "leadership_data.csv"

# Initialize a CSV file and write the header
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Title'])

# Loop through the pages and scrape data
page_number = 0
while True:
    page_url = base_url + str(page_number)
    data, soup = scrape_page(page_url)  # Get data and the updated soup

    if not data:
        break  # Stop if no more data is found on the page

    # Append the data to the CSV file
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    # Append the data to database
    for name, title in data:

        # Check if a person with the same name already exists in the database
        existing_product = Leadership.objects.filter(name=name).first()

        if not existing_product:
            # If the person doesn't exist, create and save it
            leadership_instance = Leadership(name=name, title=title)
            leadership_instance.save()
        else:
            # If the person already exists, you can optionally update its price or handle it as needed
            print(f"Person '{name}' already exists.")

    page_number += 1

    # Find the next page URL
    next_page = soup.find('a', {'class': 'usa-pagination__button', 'rel': 'next'})
    if next_page:
        next_page_url = next_page['href']
    else:
        break  # Stop if there is no next page

print("Data has been scraped and saved to", csv_file)
