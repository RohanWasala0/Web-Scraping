import cutie
import pandas as pd

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

def click_next(driver):
    next_page = driver.find_element(By.XPATH, "//span[contains(@class, 'nextButton')]")
    next_page.click()

def select_categories(categories_list):
    categories_text_list = [x.text for x in categories_list]
    selected_categories_index = cutie.select(categories_text_list, caption_indices=[0], selected_index=len(categories_list))

    link_text = categories_list[selected_categories_index].text
    print(f"Selected Category: {link_text}")
    categories_list[selected_categories_index].click()

options = Options()
options.add_argument('-headless')

website = "https://www.audible.in/adblbestsellers"
driver = webdriver.Firefox(options= options)
driver.get(website)

categories = driver.find_element(By.XPATH, "//form[contains(@class, 'refinementsAndPagingForm')]")
categories_list = categories.find_elements(By.TAG_NAME, "li")

select_categories(categories_list)

pages_container = driver.find_element(By.XPATH, "//ul[contains(@class, 'pagingElements')]")
pages = pages_container.find_elements(By.TAG_NAME,"li")
_last_page_index = int(pages[-2].text)

current_page_index = 1

_title, _author, _narrator, _duration, _released_data, _language, _rating = [], [], [], [], [], [], []
while current_page_index <= _last_page_index:
    container = WebDriverWait(driver, 2).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container ')))
    books = WebDriverWait(container, 2).until(expected_conditions.presence_of_all_elements_located((By.XPATH, "./div/span/ul/li")))
    
    for book in books:
        _title.append(book.find_element(By.XPATH, ".//h3[contains(@class, 'bc-heading')]/a").text)
        _author.append(book.find_element(By.XPATH, ".//li[contains(@class, 'authorLabel')]/span/a").text)
        _narrator.append(book.find_element(By.XPATH, ".//li[contains(@class, 'narratorLabel')]/span/a").text)
        _duration.append(book.find_element(By.XPATH, ".//li[contains(@class, 'runtimeLabel')]").text)
        _released_data.append(book.find_element(By.XPATH, ".//li[contains(@class, 'releaseDateLabel')]").text)
        _language.append(book.find_element(By.XPATH, ".//li[contains(@class, 'languageLabel')]").text)
#        _rating.append(book.find_element(By.XPATH, ".//li/span[@class='bc-text bc-pub-offscreen']").text)

    current_page_index += 1

    try:
        click_next(driver)
    except Exception:
        break

df = pd.DataFrame({
    'title': _title,
    'author': _author,
    'narrator': _narrator,
    'duration': _duration,
    'released data': _released_data,
    "language": _language, 
})
df.to_csv("audible_by_categories.csv", index=False)
driver.quit()

