import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
import json


def parse():
    driver = webdriver.Chrome()

    url = "https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Extract the IDs of all menu items from the HTML content
    product_ids = [item['data-product-id'] for item in soup.find_all('li', class_='cmp-category__item')]

    products = []

    # Iterate over each product ID and parse its details
    for product_id in product_ids:
        try:
            driver.get(f"https://www.mcdonalds.com/ua/uk-ua/product/{product_id}.html")
            driver.find_element(by=By.ID, value='accordion-29309a7a60-item-9ea8a10642-button').click()
            time.sleep(2)

            # Extract the energy values from the nutrition summary section
            energy_values = driver.find_element(By.CSS_SELECTOR, 'ul.cmp-nutrition-summary__heading-primary').text
            energy_lines = energy_values.split('\n')
            energy_values_list = [line.split()[0] for line in energy_lines]

            # Extract the nutrition values from the nutrition details section
            nutrition_values = driver.find_element(by=By.XPATH,
                                                   value='/html/body/div/div/div/main/div/div/div[1]/div/div/div[3]/div/div[1]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[2]/div/div/div/div[1]').text.strip()
            nutrition_lines = nutrition_values.split('\n')
            nutrition_values_list = [line.split()[0] for line in nutrition_lines]

            product = {
                'id': product_id,
                'name': driver.find_element(By.XPATH,
                                            '/html/body/div[1]/div/div/main/div/div/div[1]/div/div/div[1]/div/div[1]/div/div[3]/div[1]/h1/span[2]').text.strip(),
                'description': driver.find_element(By.CSS_SELECTOR,
                                                   'div.cmp-product-details-main__description').text.strip(),
                'calories': energy_values_list[0],
                'fats': energy_values_list[6],
                'carbs': energy_values_list[11],
                'proteins': energy_values_list[16],
                'unsaturated_fats': nutrition_values_list[1],
                'sugar': nutrition_values_list[4],
                'salt': nutrition_values_list[7],
                'portion': nutrition_values_list[10]
            }
            products.append(product)

            with open("mcdonalds_menu.json", "w", encoding="utf-8") as file:
                json.dump(products, file, ensure_ascii=False)
        except Exception as _ex:
            print(_ex)


parse()
