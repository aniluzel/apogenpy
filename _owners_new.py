from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import POMGen
#main_navbar=POMGen.ObjectGen('main-navbar','http://localhost:8080/owners/new')
#add_owner_form=POMGen.ObjectGen('add-owner-form','http://localhost:8080/owners/new')
firstName=POMGen.ObjectGen('firstName','http://localhost:8080/owners/new')
lastName=POMGen.ObjectGen('lastName','http://localhost:8080/owners/new')
#address=POMGen.ObjectGen('address','http://localhost:8080/owners/new')
#city=POMGen.ObjectGen('city','http://localhost:8080/owners/new')
#telephone=POMGen.ObjectGen('telephone','http://localhost:8080/owners/new')

firstName.object.send_keys("anıl")
lastName.object.send_keys("uzel")