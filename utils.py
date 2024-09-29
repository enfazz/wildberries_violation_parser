from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


def read_txt_file(filepath: str) -> list:
    with open(filepath, 'r') as f:
        result = f.read().splitlines()
    return result

def get_urls(base_url: str, keywords: list  ):
    replace_pattern = {
        " ": "%20"
    }
    clean_keywords = []
    urls = []
    for keyword in keywords:
        for key, value in replace_pattern.items():
            clean_keywords.append(keyword.replace(key, value))
    for clean_keyword in clean_keywords:
        urls.append(base_url + clean_keyword)
    return urls

def scroll_down(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height

def render_page_html(url: str):
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    WebDriverWait(driver, 2).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "product-card__wrapper"))
    )
    scroll_down(driver)
    html = driver.page_source
    driver.quit()
    return html

if __name__ == '__main__':
    keywords = ['Samyun Wan', 'Самюн Ван', 'Самуин Ван', 'Сам Ван', "Cаму Ван"]
    original_sellers = ["Samyun Wan"]
    base_url = "https://www.wildberries.ru/catalog/0/search.aspx?search="

    urls = get_urls(base_url, keywords)
    url = urls[0]   
    html = render_page_html(url)
    soup = BeautifulSoup(html, features="lxml")
    product_panel = soup.find("div", class_="catalog-page__content")
    product_cards = product_panel.find_all("div", class_="product-card__wrapper")
    product_card_links = []
    product_urls = []
    for product_card in product_cards:
        product_card_links.extend(product_card.find_all("a", class_="product-card__link j-card-link j-open-full-product-card"))
    for product_url in product_card_links: 
        product_urls.append(product_url["href"])
    print(product_urls)