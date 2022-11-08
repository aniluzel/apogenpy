from urllib.parse import urlparse

import utils


def file_gen(url, elems):
    parsed_url = utils.urlparse(url)
    folder_path = utils.folder_name_changer(parsed_url[1]) + "-POM"
    if not utils.os.path.exists(folder_path):
        utils.os.mkdir(folder_path)
    else:
        print("Directory already exists, moving on")

    file_name = utils.file_name_changer(parsed_url[2])
    with open(folder_path + "\\" + file_name + ".py", "a") as f:
        for elem in elems:
            if '>' and '<' in elem:
                elem = (elem.split(">"))[1].split("<")[0]
                if (len(elem) > 1):
                    elem_name = elem.replace(' ', '_')
                    elem = "//button[text()=\\\'" + elem + "\\\']"
            else:
                elem_name = elem.replace('-', '_')
                elem_name=elem_name.replace(" ","_")

            f.write("\ndef " + elem_name + "(input=\"\"):\n\t" + elem_name + " = POM_GEN.ObjectGen(\'" + elem + "\', driver.driver)"
            "\n\tif not input:\n\t\t" + elem_name + ".object.click()\n\telse:\n\t\t" + elem_name + ".object.send_keys(input)\n\n")



def valid_url(to_validate: str) -> bool:
    o = urlparse(to_validate)
    return True if o.scheme and o.netloc else False

#print(valid_url("http://localhost:8080"))
#print(valid_url(r"C:\Users\ozgun\Desktop\apogen\PetClinic __ a Spring Framework demonstration.html"))

def htmlsoup(url):
    isurl=valid_url(url)
    if isurl == True:
        page_html = utils.requests.get(url).text
        soup = utils.BeautifulSoup(page_html, "html.parser")
    else:
        page_html = open(url,"r")
        soup = utils.BeautifulSoup(page_html, "html.parser")
    return soup


def idfinder(url):
    soup = htmlsoup(url)
    idSoup = [tag['id'] for tag in soup.find_all(id=True)]
    return idSoup


def buttonfinder(url):
    buttons= []
    soup = htmlsoup(url)
    divSoup = soup.find_all('div')
    for i in divSoup:
        buttonSoup = str(soup.find_all('button'))
        if buttonSoup is not None and buttonSoup not in buttons:
            buttons.append(buttonSoup)
    returnarray = []
    buttons[0]=buttons[0].removesuffix("]")
    buttons[0] = buttons[0].removeprefix("[")
    buttons[0]=" ".join(buttons[0].split())
    #print(buttons[0])
    subs= ">, <"
    for i in buttons[0].split(subs):
        str1 =""
        if i == buttons[0].split(subs)[0]:
            str1 = i+">"
        elif i == buttons[0].split(subs)[len(buttons[0].split(subs))-1]:
            str1="<"+i
        else:
            str1="<"+i+">"
        returnarray.append(str1)




    return returnarray


# alt commente bak öyle çıkıyor 2 dimension array
# ['[<button class="navbar-toggler" data-bs-target="#main-navbar" data-bs-toggle="collapse"
# type="button">\n<span class="navbar-toggler-icon"></span>\n</button>,
# <button class="btn btn-primary" type="submit">Find\r\n          Owner</button>]']

def hreffinder(url):
    href=[]
    soup = htmlsoup(url)
    testSoup = soup.find_all('a')
    for i in testSoup:
        test = i.get('href')
        if test is not None and test not in href:
            href.append(test)
    return href

def classfinder(url):
    classes = []
    soup = htmlsoup(url)
    testSoup = soup.find_all('a')
    for i in testSoup:
        test = i.get('class')
        if test is not None and test not in classes:
            classes.append(test)
    returnarray=[]
    for i in classes:

        if len(i) > 1:
            str1 = ""

            for j in i:
                str1 = str1 + str(j) + " "
            str1 = str1.removesuffix(" ")
            returnarray.append(str1)
        else:
            returnarray.append(i[0])
    return returnarray

def elemfinder(url):
    elems = idfinder(url)+buttonfinder(url)+classfinder(url)

    return elems

#print(buttonfinder(url))
#print(classfinder(url))


#print(elemfinder("C:\Users\ozgun\Desktop\apogen\PetClinic __ a Spring Framework demonstration.html"))
#print("---------------------------------------------")
#print(elemfinder("http://localhost:8080/owners/new"))

