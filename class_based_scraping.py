from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

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
    
    def extract_table(self):
        table_ = self.driver.find_element(By.XPATH, "//div[@id='contentH']/table[@id='tableH']")
        self.wait_to_load("//tbody[@id='hBody']/tr")

        table_head_elements = table_.find_elements(By.XPATH, ',//thead/tr')
        table_body = table_.find_element(By.TAG_NAME, "tbody")

        head_elements_data = []
        for m in table_head_elements:
            head_elements_data += list(x.text for x in m.find_elements(By.TAG_NAME, 'th') if x.text != '')
        head_elements_data = head_elements_data[:head_elements_data.index('Score')] + ['', 'Score_NS', 'Score_WE']
        
        
