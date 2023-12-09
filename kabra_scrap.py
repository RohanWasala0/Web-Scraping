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

pair_tbody = driver.find_element(By.TAG_NAME, 'tbody')
WebDriverWait(pair_tbody, 8).until(
    expected_conditions.presence_of_all_elements_located(
        (By.XPATH, "//a[contains(@class, 'pairNumberLink')]")
    )
)
pair_numbers = pair_tbody.find_elements(By.XPATH, "//a[contains(@class, 'pairNumberLink')]")
temp = list(x.text for x in pair_numbers)
print(temp)
input_pair_number = input("Enter the players pair number from the above list \n")
if input_pair_number in temp:
    input_pair_number_index = temp.index(input_pair_number)
    pair_numbers[input_pair_number_index].click()
    table_element = driver.find_element(By.ID, "tableH")
    WebDriverWait(table_element, 10).until(
        expected_conditions.presence_of_all_elements_located(
            (By.XPATH, "//tb[contains(@rowspan='6')]")
        )
    )
    table_data = []
    for row in table_element.find_elements(By.TAG_NAME, "tr"):
        row_data = []
        for cell in row.find_elements(By.TAG_NAME, "td"):
            row_data.append(cell.text)
    table_data.append(row_data)
    print(table_data)
else:
    print("player pair is not in the player pair list")

driver.quit()