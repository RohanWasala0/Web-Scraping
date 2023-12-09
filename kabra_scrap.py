from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

options = Options()
options.add_argument('-headless')

website = "https://bfi.net.in/wp-content/uploads/2023/kabrapairs/"
driver = webdriver.Firefox(options= options)
driver.get(website)

WebDriverWait(driver, 8).until(
    expected_conditions.presence_of_all_elements_located(
        (By.XPATH, "//tbody[@id='rBody']/tr")
    )
)
pair_numbers = driver.find_elements(By.XPATH, "//a[contains(@class, 'pairNumberLink')]")
temp = list(x.text for x in pair_numbers)
print(temp)
input_pair_number = input("Enter the players pair number from the above list \n")
if input_pair_number in temp:
    input_pair_number_index = temp.index(input_pair_number)
    pair_numbers[input_pair_number_index].click()
    table_element = driver.find_element(By.XPATH, "//div[@id='contentH']/table[@id='tableH']")
    WebDriverWait(table_element, 10).until(
        expected_conditions.presence_of_all_elements_located(
            (By.XPATH, "//tbody[@id='hBody']/tr")
        )
    )
    table_head = table_element.find_element(By.TAG_NAME, 'thead')
    table_body = table_element.find_element(By.TAG_NAME, 'tbody')

    table_head_elements = table_head.find_elements(By.XPATH, './td[contains(@scope, "col")]')
    table_body_elements = table_body.find_elements(By.TAG_NAME, 'tr')
    for m in table_head_elements:
        print(m.text)
    print(len(table_body_elements))
else:
    print("player pair is not in the player pair list")

driver.quit()