#imports
def filegenerator(filename,url,id,linktext,classname,CSS):
    imports= "from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nfrom selenium.webdriver.chrome.service import Service\nimport POMGen"
    with open(filename,'w') as f:
        f.write(imports)

        f.write("\nobj=POMGen.ObjectGen(\'"+id+"\',\'"+linktext+"\',\'"+classname+"\',\'"+CSS+"\','http://localhost:8080/owners/new')")




filegenerator("test.py","testurl","firstName","test3","test4","test5")