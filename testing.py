from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# testing example code on selenium page getting started 
driver = webdriver.Chrome()                     #making a firefox websriver
driver.get("http://www.python.org")              #getting the web page python.org using the driver                           

assert "Python" in driver.title

elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()