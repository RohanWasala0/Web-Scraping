from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


options = Options()
options.add_argument('-headless')

website = "https://www.audible.in/adblbestsellers"
driver = webdriver.Firefox(options)

driver.get(website)

pagination = driver.find_element(By.XPATH, "//ul[contains(@class, 'pagingElements')]")
pages = pagination.find_elements(By.TAG_NAME, "li")
last_page = int(pages[-2].text)

current_page = 1

book_titles = []
book_authors = []
book_runtimes = []

while current_page <= last_page:
    container = WebDriverWait(driver, 2).until(ec.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container ')))
    products = WebDriverWait(container, 2).until(ec.presence_of_all_elements_located((By.XPATH, "./div/span/ul/li")))

    for product in products:
        book_titles.append(product.find_element(By.XPATH, ".//h3[contains(@class, 'bc-heading')]/a").text)
        book_authors.append(product.find_element(By.XPATH, ".//li[contains(@class, 'authorLabel')]").text)
        book_runtimes.append(product.find_element(By.XPATH, ".//li[contains(@class, 'runtimeLabel')]").text)

    current_page += 1

    try:
        next_page = driver.find_element(By.XPATH, "//span[contains(@class, 'nextButton')]")
        next_page.click()
    except Exception:
        break

df = pd.DataFrame({'title': book_titles, 'author': book_authors, 'runtimes': book_runtimes})
df.to_csv("audio_books.csv", index=False)

driver.quit()