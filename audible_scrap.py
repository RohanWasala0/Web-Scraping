from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("https://www.audible.com/adblbestsellers")

categories = driver.find_element(By.XPATH, "//form[@class = 'refinementsAndPagingForm refinementsForm']")
categories_list = categories.find_elements(By.TAG_NAME, "li")
print(len(categories_list))
for x in categories_list:
    print(x.text)
driver.quit()