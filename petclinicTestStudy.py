from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
service = Service(r'C:\Users\ozgun\Desktop\pythonProjects\apogen\chromedriver.exe')
browser = webdriver.Chrome(service=service)


browser.get("http://localhost:8080")
print(browser.title)
def vetListTest():
    vets=browser.find_element(By.XPATH,"/html/body/nav/div/div/ul/li[3]/a")
    vets.click()
    time.sleep(3)
    secondPage=browser.find_element(By.XPATH,"/html/body/div/div/div[1]/span[4]")
    secondPage.click()
def addOwnerTest():
    owners = browser.find_element(By.XPATH,"/html/body/nav/div/div/ul/li[2]/a")
    owners.click()
    time.sleep(3)
    addOwnerPage = browser.find_element(By.XPATH,"/html/body/div/div/form/a")
    addOwnerPage.click()
    time.sleep(3)
    browser.find_element(By.ID,"firstName").send_keys("testName")
    time.sleep(1)
    browser.find_element(By.ID,"lastName").send_keys("testLastName")
    time.sleep(1)
    browser.find_element(By.ID,"address").send_keys("testAddress")
    time.sleep(1)
    browser.find_element(By.ID,"city").send_keys("testCity")
    time.sleep(1)
    browser.find_element(By.ID,"telephone").send_keys("11111111")
    time.sleep(1)
    browser.find_element(By.XPATH,"/html/body/div/div/form/div[2]/div/button").click()
    browser.find_element(By.XPATH,"/html/body/div/div/a[2]").click() #add new pet
    browser.find_element(By.ID,"name").send_keys("testPetName")
    browser.find_element(By.ID,"birthDate").send_keys("11111111")
    browser.find_element(By.ID,"type").click()
    time.sleep(3)
    browser.find_element(By.XPATH,"/html/body/div/div/form/div[1]/div[4]/div/select/option[5]").click() #select lizard
    time.sleep(3)
    browser.find_element(By.XPATH,"/html/body/div/div/form/div[2]/div/button").click()


#--------------------------------------------------------------------------------------

addOwnerTest()
time.sleep(5)
vetListTest()

#




