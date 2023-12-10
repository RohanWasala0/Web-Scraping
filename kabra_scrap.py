import pandas as pd

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

    fTable_head = []
    table_head_elements = table_head.find_elements(By.TAG_NAME, 'tr')
    for m in table_head_elements:
        table_head_data = m.find_elements(By.TAG_NAME, 'th')
        for x in table_head_data:
            _ = x.text
            if _ != '':
                fTable_head.append(_)
    
    fTable_head = fTable_head[:fTable_head.index('Score')] + ['', 'Score_NS', 'Score_WE'] + fTable_head[fTable_head.index('Score')+1:-2]
    table_body_elements = table_body.find_elements(By.TAG_NAME, 'tr')
    Round, Opponent = '', ''
    fTable_body = []
    for n in table_body_elements:
        table_body_data = n.find_elements(By.TAG_NAME, 'td')
        _temp = list(h.text for h in table_body_data)
        no=0
        if len(_temp) == 13:
            Round = _temp[0]
            Opponent = _temp[1]
            no= 2
        _temp = [Round, Opponent] + _temp[no:]
        fTable_body.append(_temp)
else:
    print("player pair is not in the player pair list")
fTable_body.pop(0)
fTable_body.pop(-1)
print(fTable_head, fTable_body)
df = pd.DataFrame(fTable_body, columns=fTable_head)
df.to_csv("kabra.csv", index=False)
driver.quit()