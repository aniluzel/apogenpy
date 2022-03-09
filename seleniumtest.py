import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

os.environ['PATH'] += r"C:\ChromeDriver"
driver = webdriver.Chrome()

class SeleniumTest(object):
    def __init__(self, driver):
        self.driver = driver
        self.driver.get("http://localhost:8080/")
        self.driver.implicitly_wait(5)

        test = (By.XPATH, "//a[@href='/owners/find']")

        time.sleep(0.5)
        self.FindOwners = driver.find_element(*test)
        self.FindOwners.click()
        time.sleep(0.5)
        self.AddOwner = driver.find_element(By.XPATH, "//a[text()='Add Owner']")
        self.AddOwner.click()
        time.sleep(0.5)
        self.AddOwnerFirstName = driver.find_element(By.XPATH, "//*[@id='firstName']")
        self.AddOwnerFirstName.send_keys("TestName")
        time.sleep(0.5)
        self.AddOwnerLastName = driver.find_element(By.XPATH, "//*[@id='lastName']")
        self.AddOwnerLastName.send_keys("TestSurname")
        time.sleep(0.5)
        self.AddOwnerAddress = driver.find_element(By.XPATH, "//*[@id='address']")
        self.AddOwnerAddress.send_keys("TestAddress")
        time.sleep(0.5)
        self.AddOwnerCity = driver.find_element(By.XPATH, "//*[@id='city']")
        self.AddOwnerCity.send_keys("TestCity")
        time.sleep(0.5)
        self.AddOwnerTelephone = driver.find_element(By.XPATH, "//*[@id='telephone']")
        self.AddOwnerTelephone.send_keys("01230")
        time.sleep(0.5)
        self.AddOwnerFinish = driver.find_element(By.XPATH, "//button[text()='Add Owner']")
        self.AddOwnerFinish.click()
        time.sleep(0.5)
        self.AddPet = driver.find_element(By.XPATH, "//a[normalize-space(text()) = 'Add New Pet']")
        self.AddPet.click()
        time.sleep(0.5)
        self.AddPetName = driver.find_element(By.XPATH, "//*[@id='name']")
        self.AddPetName.send_keys("Cody")
        time.sleep(0.5)
        self.AddPetDate = driver.find_element(By.XPATH, "//*[@id='birthDate']")
        self.AddPetDate.send_keys("01012020")
        time.sleep(0.5)
        self.AddPetType = Select(driver.find_element(By.XPATH, "//*[@id='type']"))
        self.AddPetType.select_by_value('dog')
        time.sleep(0.5)
        self.AddPetFinish = driver.find_element(By.XPATH, "//button[text()='Add Pet']")
        self.AddPetFinish.click()
        time.sleep(0.5)
        self.AddVisit = driver.find_element(By.XPATH, "//a[normalize-space(text()) = 'Add Visit']")
        self.AddVisit.click()
        time.sleep(0.5)
        self.AddVisitDescription = driver.find_element(By.XPATH, "//*[@id='description']")
        self.AddVisitDescription.send_keys("Test Visit")
        time.sleep(0.5)
        self.AddVisitFinish = driver.find_element(By.XPATH, "//button[text()='Add Visit']")
        self.AddVisitFinish.click()
        time.sleep(0.5)
        self.FindOwners = driver.find_element(By.XPATH, "//a[@href='/owners/find']")
        self.FindOwners.click()
        time.sleep(0.5)
        self.FindOwnersSearch = driver.find_element(By.XPATH, "//*[@id='lastName']")
        self.FindOwnersSearch.send_keys("TestSurname")
        time.sleep(0.5)
        self.FindOwnersFinish = driver.find_element(By.XPATH, "//button[normalize-space(text()) = 'Find Owner']")
        self.FindOwnersFinish.click()


SeleniumTest(driver)
