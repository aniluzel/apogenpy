from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

#For Windows
service = Service(r'C:\chromedriver.exe')


#service = Service("/Users/denis/Documents/CS401/chromedriver")
driver = webdriver.Chrome(service=service)
driver.get("http://localhost:8080/owners/find")
driver.maximize_window()

a_elements = driver.find_elements(By.TAG_NAME,"a")
button_elements = driver.find_elements(By.CLASS_NAME,"btn btn-primary")

for elem in a_elements:

    print(elem.get_attribute("href"))
    if elem.accessible_name.__contains__("FIND OWNERS"):
        ftmp =elem.get_property("class")
print(button_elements)



for elem in button_elements:
    elem.click()

time.sleep(5)
driver.quit()