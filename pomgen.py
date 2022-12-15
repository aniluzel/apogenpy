from urllib.parse import urlparse
import utils


# class Element:
#     def __init__(self, data, name, type):
#         self.data = data
#         self.name = name
#         self.type = type


def file_gen(url, elems):
    parsed_url = utils.urlparse(url)
    folder_path = utils.folder_name_changer(parsed_url[1]) + "_POM"
    invalid = '<>:"/\|?* -.'
    for char in invalid:
        folder_path = folder_path.replace(char, '_')
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
                elem_tmp = (elem.data.split(">"))[1].split("<")[0]  #####BURASINI ALDIM
                if (len(elem_tmp) > 1):
                    elem_tmp = "//button[text()=\\\'" + elem_tmp + "\\\']"
                    f.write(
                        "\ndef " + elem.name + "(input=\"\", timeout=0.5):\n\ttestdriver.selenium(\'" + elem_tmp + "\', input, timeout, driver, \"" + elem.type + "\")\n\n")
            else:

                f.write(
                    "\ndef " + elem.name + "(input=\"\", timeout=0.5):\n\ttestdriver.selenium(\"" + elem.data + "\", input, timeout, driver, \"" + elem.type + "\")\n\n")

    with open("TEST_FILE_" + folder_path.removesuffix("_POM") + ".py", "a") as f:
        f.write("import " + folder_path + "." + file_name + " as " + file_name + "\n# GoTo")
        for elem in elems:
            elem_tmp2 = elem.data

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


def htmlsoup(url):
    isurl = valid_url(url)
    if isurl == True:
        page_html = utils.requests.get(url).text
        soup = utils.BeautifulSoup(page_html, "html.parser")
    else:
        page_html = open(url, "r")
        soup = utils.BeautifulSoup(page_html, "html.parser")
    return soup


# def elemprinter(elemarray):
#     for x in elemarray:
#         print("data: " + x.data + " name: " + x.name + " type: " + x.type)
#
#
# def idfinder(url):
#     type = "id"
#     soup = htmlsoup(url)
#     idSoup = [tag['id'] for tag in soup.find_all(id=True)]
#     elemarray = []
#     for x in idSoup:
#         elemarray.append(Element(x, utils.namechanger(x, type), type))
#     return elemarray
#
#
# def buttonfinder(url):
#     type = "xpath"
#     buttons = []
#     soup = htmlsoup(url)
#     divSoup = soup.find_all('div')
#     for i in divSoup:
#         buttonSoup = str(soup.find_all('button'))
#         if buttonSoup is not None and buttonSoup not in buttons:
#             buttons.append(buttonSoup)
#     returnarray = []
#     if len(buttons) != 0:
#         buttons[0] = buttons[0].removesuffix("]")
#         buttons[0] = buttons[0].removeprefix("[")
#         buttons[0] = " ".join(buttons[0].split())
#         # print(buttons[0])
#         subs = ">, <"
#         for i in buttons[0].split(subs):
#             str1 = ""
#             if i == buttons[0].split(subs)[0]:
#                 str1 = i + ">"
#             elif i == buttons[0].split(subs)[len(buttons[0].split(subs)) - 1]:
#                 str1 = "<" + i
#             else:
#                 str1 = "<" + i + ">"
#
#             returnarray.append(str1)
#     elemarray = []
#     for elem in returnarray:
#         elemarray.append(Element(elem, utils.namechanger(elem, type), type))
#     return elemarray
#
#
# # alt commente bak öyle çıkıyor 2 dimension array
# # ['[<button class="navbar-toggler" data-bs-target="#main-navbar" data-bs-toggle="collapse"
# # type="button">\n<span class="navbar-toggler-icon"></span>\n</button>,
# # <button class="btn btn-primary" type="submit">Find\r\n          Owner</button>]']
#
# def hreffinder(url):
#     href = []
#     soup = htmlsoup(url)
#     testSoup = soup.find_all('a')
#     for i in testSoup:
#         test = i.get('href')
#         if test is not None and test not in href:
#             href.append(test)
#     return href
#
#
# def classfinder(url):
#     type = "class"
#     classes = []
#     soup = htmlsoup(url)
#     testSoup = soup.find_all('a')
#     for i in testSoup:
#         test = i.get('class')
#         if test is not None and test not in classes:
#             classes.append(test)
#     returnarray = []
#     for i in classes:
#
#         if len(i) > 1:
#             str1 = ""
#
#             for j in i:
#                 str1 = str1 + str(j) + " "
#
#             str1 = str1.removesuffix(" ")
#             returnarray.append(str1)
#         else:
#             returnarray.append(i[0])
#     elemarray = []
#     for x in returnarray:
#         elemarray.append(Element(x, utils.namechanger(x, type), type))
#
#     return elemarray
#
#
# def elemfinder(url):
#     elems = idfinder(url) + buttonfinder(url) + classfinder(url)
#     return elems
#
#
# def buttonfinder2(url):
#     buttons = []
#     soup = htmlsoup(url)
#
#
# def otherparser(url):
#     page_html = utils.requests.get(url).text
#     utils.parser.feed(page_html)
#     print(utils.parser.data_text)


url = 'http://localhost:8080/owners/2/pets/new'
html_tags = ["a", "button", "input", "select"]


class HTMLElementData:
    def __init__(self, html_data):
        self.html_data = html_data


class HTMLElement:
    def __init__(self):
        self.html_id = None
        self.id = None
        self.classname = None
        self.name = None
        self.href = None
        self.text = None
        self.tag = None
        self.type = None
        self.title = None
        self.multiple_text = []

    def set_id(self, id):
        self.id = id

    def set_class(self, classname):
        self.classname = classname

    def set_name(self, name):
        self.name = name

    def set_href(self, href):
        self.href = href

    def set_text(self, text):
        self.text = text

    def set_tag(self, tag):
        self.tag = tag

    def set_type(self, type):
        self.type = type

    def set_title(self, title):
        self.title = title

    def set_html_id(self, html_id):
        self.html_id = html_id

    def set_multiple_text(self, multiple_text):
        self.multiple_text = multiple_text

    def print(self):
        print("HTML_ID: " + str(self.html_id))
        print("id: "+self.id)
        print("classname: "+self.classname)
        print("name: " + self.name)
        print("href: " + self.href)
        print("text: " + self.text)
        print("tag: " + self.tag)
        print("type: " + self.type)
        print("title: " + self.title)
        if len(self.multiple_text) > 0:
            print("multiple text: " + str(self.multiple_text))
        print()

    def GUI_highlight_info(self):
        if self.text is not None:
            return self.text
        else:
            return ""

    def GUI_window_adder(self):
        GUI_string = "!undefined_element"

        if self.text is not None and len(self.multiple_text) == 0:
            GUI_string= "Display Text -> " + self.text
        elif self.id is not None:
            GUI_string = "ID -> " + self.id
        elif self.name is not None:
            GUI_string = "Name -> " + self.name
        elif self.title is not None:
            GUI_string = "Title -> " + self.title
        elif self.classname is not None:
            GUI_string = "Classname -> " + self.classname
        elif self.type is not None:
            GUI_string = "Type -> " + self.type
        elif self.multiple_text is not None and len(self.multiple_text) > 0:
            GUI_string = "First Value of List -> " + self.multiple_text[0]
        elif self.href is not None:
            GUI_string = "Href -> " + self.href
        elif self.tag is not None:
            GUI_string = "HTML Tag -> " + self.tag

        return GUI_string

    def GUI_window_more_info(self):
        GUI_string=""
        GUI_string_array = []
        if self.tag is not None:
            GUI_string_array.append("HTML Tag: " + self.tag)
        if self.id is not None:
            GUI_string_array.append("ID: " + self.id)
        if self.classname is not None:
            GUI_string_array.append("Classname: " + self.classname)
        if self.text is not None:
            GUI_string_array.append("Display Text: " + self.text)
        if self.name is not None:
            GUI_string_array.append("Name: " + self.name)
        if self.title is not None:
            GUI_string_array.append("Title: " + self.title)
        if self.type is not None:
            GUI_string_array.append("Type: " + self.type)
        if self.href is not None:
            GUI_string_array.append("Href: " + self.href)
        if self.multiple_text is not None and len(self.multiple_text) > 0:
            GUI_string_array.append("List Values: " + self.multiple_text[0])
        GUI_string_return=""
        for i in range(len(GUI_string_array)):
            if not i == len(GUI_string_array)-1:
                GUI_string_return += GUI_string_array[i] + "\n"
            else:
                GUI_string_return += GUI_string_array[i]
        return GUI_string_return


def HTMLReader(data):
    type = "main"
    for line in data.splitlines():
        if "SUB_BEGIN" in line:
            type = "sub"
        elif "SUB_END" in line:
            type = "main"


def HTMLFilterer(url, html_tags):
    data_array = []
    html_id = 0
    for tag in html_tags:
        soup = htmlsoup(url).find_all(tag)
        for i in soup:
            html_element_array = []
            parser = utils.HTMLParser()
            parser.feed(str(i))
            html_data = parser.return_data()
            # print("HTML_PARSE_ID: " + str(html_id) + "\n" + html_data)
            html_element_array.append(html_id)
            html_element_array.append(parser.main_tag)
            html_element_array.append(parser.attrs)
            html_element_array.append(parser.data)
            data_array.append(html_element_array)
            # html_element_array.append(parser.sub_tags)
            # html_element_array.append(parser.sub_attrs)
            html_id += 1

    element_array = []  # OBJECT ARRAY

    for i in data_array:
        # print(i)
        elem = HTMLElement()
        elem.set_html_id(i[0])

        elem.set_tag(i[1])
        attribute_array = i[2]
        for attr in attribute_array:
            if attr[0] == 'class':
                elem.set_class(attr[1])
            elif attr[0] == 'href':
                elem.set_href(attr[1])
            elif attr[0] == 'name':
                elem.set_name(attr[1])
            elif attr[0] == 'type':
                elem.set_type(attr[1])
            elif attr[0] == 'title':
                elem.set_title(attr[1])
            elif attr[0] == 'id':
                elem.set_id(attr[1])

        if len(i[3]) > 0:
            if len(i[3]) == 1:
               elem.set_text(i[3][0])
            else:
                elem.set_text(max(i[3], key=len))
                elem.set_multiple_text(i[3])

        element_array.append(elem)

    # for elem in element_array:
    #     elem.print()
    return element_array


arrr = HTMLFilterer(url, html_tags)
