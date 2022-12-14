from urllib.parse import urlparse

import utils

class Element:
    def __init__(self,data,name,type):
        self.data=data
        self.name=name
        self.type=type





def file_gen(url, elems):
    parsed_url = utils.urlparse(url)
    folder_path = utils.folder_name_changer(parsed_url[1]) + "_POM"
    if not utils.os.path.exists(folder_path):
        utils.os.mkdir(folder_path)
    else:
        print("Directory already exists, moving on")

    file_name = utils.file_name_changer(parsed_url[2])
    with open(folder_path + "\\" + file_name + ".py", "a") as f:
        f.write(
            "import testdriver\n\nurl = \"" + url + "\"\ndriver = testdriver.Driver.driver\n\n\ndef GoTo():\n\tdriver.get(url)\n\n")
        for elem in elems:
            if '>' and '<' in elem.data:
                elem_tmp = (elem.data.split(">"))[1].split("<")[0]    #####BURASINI ALDIM
                if (len(elem_tmp) > 1):

                    elem_tmp = "//button[text()=\\\'" + elem_tmp + "\\\']"
                    f.write("\ndef " + elem.name + "(input=\"\", timeout=0.5):\n\ttestdriver.selenium(\'" + elem_tmp + "\', input, timeout, driver, \"" + elem.type + "\")\n\n")
            else:

                f.write( "\ndef " + elem.name + "(input=\"\", timeout=0.5):\n\ttestdriver.selenium(\"" + elem.data + "\", input, timeout, driver, \"" + elem.type + "\")\n\n")


    with open("TEST_FILE_" + folder_path.removesuffix("_POM") + ".py", "a") as f:
        f.write("import " + folder_path + "." + file_name + " as " + file_name + "\n# GoTo")
        for elem in elems:
            elem_tmp2=elem.data

            if '>' and '<' in elem_tmp2:
                elem_tmp2 = (elem_tmp2.split(">"))[1].split("<")[0]
                if (len(elem_tmp2) > 1):
                    elem_name = elem_tmp2.replace(' ', '_')
            else:
                elem_name = elem_tmp2.replace('-', '_')
                elem_name = elem_tmp2.replace(" ", "_")
            f.write(", " + elem_name)
        f.write("\n")


def valid_url(to_validate: str) -> bool:
    o = urlparse(to_validate)
    return True if o.scheme and o.netloc else False


# print(valid_url("http://localhost:8080"))
# print(valid_url(r"C:\Users\ozgun\Desktop\apogen\PetClinic __ a Spring Framework demonstration.html"))

def htmlsoup(url):
    isurl = valid_url(url)
    if isurl == True:
        page_html = utils.requests.get(url).text
        soup = utils.BeautifulSoup(page_html, "html.parser")
    else:
        page_html = open(url, "r")
        soup = utils.BeautifulSoup(page_html, "html.parser")
    return soup

def elemprinter(elemarray):
    for x in elemarray:
        print("data: "+x.data+" name: "+ x.name + " type: "+x.type)



def idfinder(url):
    type="id"
    soup = htmlsoup(url)
    idSoup = [tag['id'] for tag in soup.find_all(id=True)]
    elemarray=[]
    for x in idSoup:
        elemarray.append(Element(x,utils.namechanger(x,type),type))
    return elemarray


def buttonfinder(url):
    type="xpath"
    buttons = []
    soup = htmlsoup(url)
    divSoup = soup.find_all('div')
    for i in divSoup:
        buttonSoup = str(soup.find_all('button'))
        if buttonSoup is not None and buttonSoup not in buttons:
            buttons.append(buttonSoup)
    returnarray = []
    if len(buttons) !=0:
        buttons[0] = buttons[0].removesuffix("]")
        buttons[0] = buttons[0].removeprefix("[")
        buttons[0] = " ".join(buttons[0].split())
        # print(buttons[0])
        subs = ">, <"
        for i in buttons[0].split(subs):
            str1 = ""
            if i == buttons[0].split(subs)[0]:
                str1 = i + ">"
            elif i == buttons[0].split(subs)[len(buttons[0].split(subs)) - 1]:
                str1 = "<" + i
            else:
                str1 = "<" + i + ">"

            returnarray.append(str1)
    elemarray=[]
    for elem in returnarray:
        elemarray.append(Element(elem,utils.namechanger(elem,type),type))
    return elemarray


# alt commente bak öyle çıkıyor 2 dimension array
# ['[<button class="navbar-toggler" data-bs-target="#main-navbar" data-bs-toggle="collapse"
# type="button">\n<span class="navbar-toggler-icon"></span>\n</button>,
# <button class="btn btn-primary" type="submit">Find\r\n          Owner</button>]']

def hreffinder(url):
    href = []
    soup = htmlsoup(url)
    testSoup = soup.find_all('a')
    for i in testSoup:
        test = i.get('href')
        if test is not None and test not in href:
            href.append(test)
    return href


def classfinder(url):
    type = "class"
    classes = []
    soup = htmlsoup(url)
    testSoup = soup.find_all('a')
    for i in testSoup:
        test = i.get('class')
        if test is not None and test not in classes:
            classes.append(test)
    returnarray = []
    for i in classes:

        if len(i) > 1:
            str1 = ""

            for j in i:
                str1 = str1 + str(j) + " "

            str1 = str1.removesuffix(" ")
            returnarray.append(str1)
        else:
            returnarray.append(i[0])
    elemarray=[]
    for x in returnarray:
        elemarray.append(Element(x,utils.namechanger(x,type),type))

    return elemarray


def elemfinder(url):
    elems = idfinder(url) + buttonfinder(url) + classfinder(url)
    #print(elems)
    return elems


# print(buttonfinder(url))
# print(classfinder(url))
def buttonfinder2(url):

    buttons = []
    soup = htmlsoup(url)



# print(elemfinder("C:\Users\ozgun\Desktop\apogen\PetClinic __ a Spring Framework demonstration.html"))
# print("---------------------------------------------")
#print(buttonfinder2("http://localhost:8080/owners/new"))
#data_text = []
def otherparser(url):
    page_html = utils.requests.get(url).text
    utils.parser.feed(page_html)
    print(utils.parser.data_text)
#elemprinter(idfinder("http://localhost:8080/owners/new"))
#elemprinter(buttonfinder("http://localhost:8080/owners/new"))
#otherparser("http://localhost:8080/owners/new")
#elemprinter(elemfinder("http://localhost:8080/owners/find"))
url = 'http://localhost:8080/owners/new'





class RawElementData:
    def __init__(self,RawData,OrderedData):
        self.rawdata = RawData
        self.ordereddata = OrderedData


    def print(self):
        print(self.rawdata)
        print(self.ordereddata)

def ArrayPrinter(data_array):
    for elem in data_array:
        elem.print()
        print("--------------")

class HTMLElement:
    def __init__(self, rawdata):
        self.rawdata = rawdata
        self.id = ""
        self.classname = ""
        self.href = ""
        self.displaytext = ""
        self.tag = ""
        self.type = ""

    def set_id(self,id):
        self.id=id

    def set_class(self,Class):
        self.classname=Class

    def set_href(self,href):
        self.href=href

    def set_displaytext(self,dt):
        self.displaytext=dt

    def set_tag(self,tag):
        self.tag=tag

    def set_type(self, type):
        self.type = type


tags=["a", "button", "input"]


def elemfinder2(url,tags):

    data_array = []
    for tag in tags:
        soup = htmlsoup(url).find_all(tag)
        for i in soup:
            parser1 = utils.MyHTMLParser()
            rawdata = (str(i))
            parser1.feed(rawdata)
            ordered_data = parser1.return_data()
            data_array.append(RawElementData(rawdata, ordered_data))
    print("array print")
    #ArrayPrinter(data_array)
    for data in data_array:
        element = HTMLElement(data.rawdata)
        print(data.ordereddata)
        print("----------")






elemfinder2(url,tags)
