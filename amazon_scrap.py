from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os
import django
import re
from decimal import Decimal

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_scraping.settings")
django.setup()

from data.models import Products

# Specify the path to the updated Chrome WebDriver executable
PATH = "/home/ansari/work/web_scraping/django_scrap/chromedriver-linux64/chromedriver"  # Make sure to include the .exe extension

# Create a ChromeService object with the executable path
chrome_service = ChromeService(executable_path=PATH)

# Create the WebDriver instance with the Chrome service
driver = webdriver.Chrome(service=chrome_service)

# Navigate to the website
website = "https://www.amazon.com/"
driver.get(website)

search = driver.find_element(By.XPATH, '//input[@id="twotabsearchtextbox"]')

search.send_keys("Gaming Laptop")
search.submit()

# Find all product elements
products = driver.find_elements(
    By.XPATH, '//div[@data-component-type="s-search-result"]'
)

print(products)

time.sleep(5)

product_names = []
product_prices = []
product_list_prices = []


for product in products:
    try:
        title_element = product.find_element(By.XPATH, ".//h2/a/span")
        price_element = product.find_element(
            By.XPATH, ".//div[1]/div/div[1]/div/a/span/span[1]"
        ).get_attribute("textContent")
        list_price = product.find_element(By.XPATH, './/div/div/div/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[1]/div/a/div/span[2]/span[2]').get_attribute("textContent")
        product_name = title_element.text
        product_price = price_element
        product_names.append(product_name)
        product_prices.append(product_price)
        product_list_prices.append(list_price)

    except Exception as e:
        # Handle exceptions if an element is not found
        print(f"An error occurred: {str(e)}")


time.sleep(5)



# Populate the data in the database
for product_name, product_price in zip(product_names, product_prices):
    try:
        # Clean the product_price value by removing non-numeric characters
        cleaned_price = re.sub(r'[^\d.]', '', product_price)
        # Convert the cleaned value to a decimal
        decimal_price = Decimal(cleaned_price)
        
        # Check if a product with the same name already exists in the database
        existing_product = Products.objects.filter(name=product_name).first()

        if not existing_product:
            # If the product doesn't exist, create and save it
            product = Products(name=product_name, price=decimal_price)
            product.save()
        else:
            # If the product already exists, you can optionally update its price or handle it as needed
            print(f"Product '{product_name}' already exists.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


time.sleep(5)
driver.quit()

df = pd.DataFrame({"Product": product_names, "Price": product_prices, 'List Price': list_price})
# df.to_csv("amazon_laptops.csv", index=False)
print(df)


# //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[5]/div/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[1]/div/a/span/span[2]/span[2]
# //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[1]/div/a/div/span[2]/span[2]
# //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[3]/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/div/a/div/span[2]/span[2]


# //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]
# //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[1]/div/a/div/span[2]/span[2]
# //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[3]/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/div/a/div/span[2]/span[1]