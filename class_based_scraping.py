from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import pandas as pd

class Scrape():
    def __init__(self, website: str, options: Options) -> None:
        self.driver = webdriver.Firefox(options=options)
        self.driver.get(website)
        pass
    """
    node_Xpath: str 
        - XPATH string to the node that has to be loaded
    the driver waits till the node_Xpath is loaded or for 10s
    """
    def wait_to_load(self, node_Xpath: str):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_all_elements_located(
                (By.XPATH, node_Xpath)
            )
        )
        pass
    
    def make_pairs_list(self):
        self.wait_to_load("//tbody[@id='rBody']/tr")
        self.pair_numbers = self.driver.find_elements(By.XPATH, "//a[contains(@class, 'pairNumberLink')]")
        self.display_pair_numbers = list(int(x.text) for x in self.pair_numbers if x.text != '')
        return self.display_pair_numbers
    """
    IP_pair_number: int
        - 
    """
    def click_pair_number(self, IP_pair_number: int):
        try:
            self.pair_numbers[self.display_pair_numbers.index(IP_pair_number)].click()
            return True
        except Exception:
            print(f"The player pair {IP_pair_number} is not in the player pair table")
            return False

    def extract_table(self):
        table_ = self.driver.find_element(By.XPATH, "//div[@id='contentH']/table[@id='tableH']")
        self.wait_to_load("//tbody[@id='hBody']/tr")

        table_head_elements = table_.find_elements(By.XPATH, './/thead/tr')
        table_body_elements = table_.find_elements(By.XPATH, './/tbody/tr')

        head_elements_data = []
        for m in table_head_elements:
            head_elements_data += list(x.text for x in m.find_elements(By.TAG_NAME, 'th') if x.text != '')
        head_elements_data = head_elements_data[:head_elements_data.index('Score')] + ['Score_NS', 'Score_WE'] + head_elements_data[head_elements_data.index('Score'):-2]
        
        body_elements_data = []
        Round, Opponent = '', ''
        for n in table_body_elements: 
            temp = n.find_elements(By.TAG_NAME, "td")
            no = 0
            if len(temp) == 13:
                Round, Opponent, no = temp[0].text, temp[1].text, 2 
            list_to_append = list([Round, Opponent] + list(y.text for y in temp[no:]))
            print(len(list_to_append), len(head_elements_data))
            if len(list_to_append) == len(head_elements_data):
                body_elements_data.append(list_to_append)
        
        
        return head_elements_data, body_elements_data
    
    def quit_driver(self):
        self.driver.quit()
    
    
    
options = Options()
options.add_argument('-headless')

website = "https://bfi.net.in/wp-content/uploads/2023/kabrapairs/"
obj = Scrape(website, options)

pair_list = obj.make_pairs_list()
print(pair_list)

input_pair = int(input("Enter the players pair number from the above list \n"))
exception_bool = obj.click_pair_number(input_pair)
if exception_bool:
    o1, o2 = obj.extract_table()
    print(o2[:7])
    df = pd.DataFrame(o2, columns=o1)
    df.to_csv(f"{input_pair}_kabra.csv", index=False)

obj.quit_driver()
