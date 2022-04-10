from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import POMGen
obj=POMGen.ObjectGen('firstName','test3','test4','test5','http://localhost:8080/owners/new')
obj.object.send_keys("adımbu")