import csv


def filegenerator(param,url,elemid):
    invalid = '<>:"/\|?* '
    filename = url + ".py"
    for char in invalid:
        filename = filename.replace(char, '_').removeprefix('http://localhost:8080')
    with open(filename,'a') as f:

        f.write("\n"+elemid+"=POMGen.ObjectGen(\'"+param+"\',\'"+url+"\')")


def importgenerator(url):
    invalid = '<>:"/\|?* '
    filename = url+".py"
    for char in invalid:
        filename = filename.replace(char, '_').removeprefix('http://localhost:8080')

    imports = "from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nfrom selenium.webdriver.chrome.service import Service\nimport POMGen"
    with open(filename,'w') as f:
        f.write(imports)




importgenerator("http://localhost:8080/owners/new")#url from csv as filename

with open("DEMO/DEMO_SCRAP.csv", "r") as f:
    reader =csv.reader(f)
    row1=next(reader)
    ids = row1
    print(ids)
    for elem in ids:

        filegenerator(elem,"http://localhost:8080/owners/new",elem.replace('-','_'))




#filegenerator("testid","testlink","testclass","testcss","http://localhost:8080/owners/new")