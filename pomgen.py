from urllib.parse import urlparse

from selenium.webdriver.common.by import By

import utils
import selenium


def file_gen(url, html_object_array):
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
        for html_object in html_object_array:

            # OBJECT DECODE
            html_object = HTMLElement()  # delete later

            object_name_array = html_object.object_name_picker()



            if '>' and '<' in elem.data:
                elem_tmp = (elem.data.split(">"))[1].split("<")[0]
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
    is_url = valid_url(url)

    if is_url:
        page_html = utils.requests.get(url).text
        soup = utils.BeautifulSoup(page_html, "html.parser")
    else:
        page_html = open(url, "r")
        soup = utils.BeautifulSoup(page_html, "html.parser")

    return soup


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
        print("id: " + self.id)
        print("classname: " + self.classname)
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

    def get_html_id(self):
        return self.html_id

    def get_element_screenshot(self, url):
        driver = utils.webdriver.Chrome()
        driver.get(url)
        screenshot_loc='screenshots' + "\\" + self.GUI_window_adder()
        if self.id is not None:
            elem = driver.find_element(By.ID, self.id)

            elem.screenshot(screenshot_loc)
        elif self.text is not None:
            print("text")
        elif self.href is not None:
           print("href")

        elif self.classname is not None:
            print("classname")




    def GUI_window_adder(self):
        gui_string = "!undefined_element"

        if self.text is not None and len(self.multiple_text) == 0:
            gui_string = "Text -> " + self.text
        elif self.id is not None:
            gui_string = "ID -> " + self.id
        elif self.name is not None:
            gui_string = "Name -> " + self.name
        elif self.title is not None:
            gui_string = "Title -> " + self.title
        elif self.classname is not None:
            gui_string = "Classname -> " + self.classname
        elif self.type is not None:
            gui_string = "Type -> " + self.type
        elif self.multiple_text is not None and len(self.multiple_text) > 0:
            gui_string = "First Value of List -> " + self.multiple_text[0]
        elif self.href is not None:
            gui_string = "Href -> " + self.href
        elif self.tag is not None:
            gui_string = "HTML Tag -> " + self.tag

        return str(self.html_id) + ". " + gui_string

    def GUI_window_more_info(self):
        gui_string_array = []

        if self.tag is not None:
            gui_string_array.append("HTML Tag: " + self.tag)
        if self.id is not None:
            gui_string_array.append("ID: " + self.id)
        if self.classname is not None:
            gui_string_array.append("Classname: " + self.classname)
        if self.text is not None:
            gui_string_array.append("Display Text: " + self.text)
        if self.name is not None:
            gui_string_array.append("Name: " + self.name)
        if self.title is not None:
            gui_string_array.append("Title: " + self.title)
        if self.type is not None:
            gui_string_array.append("Type: " + self.type)
        if self.href is not None:
            gui_string_array.append("Href: " + self.href)
        if self.multiple_text is not None and len(self.multiple_text) > 0:
            gui_string_array.append("List Values: " + self.multiple_text[0])

        gui_string_info = ""

        for i in range(len(gui_string_array)):
            if not i == len(gui_string_array) - 1:
                gui_string_info += gui_string_array[i] + "\n"
            else:
                gui_string_info += gui_string_array[i]

        return gui_string_info

    def object_name_picker(self):
        object_name_array = []
        object_name = "UNDEFINED_ELEMENT"

        if self.text is not None and len(self.multiple_text) == 0:
            object_name_array.append("text::")
            object_name_array.append(self.text)
        if self.id is not None:
            object_name_array.append("id::")
            object_name_array.append(self.id)
        if self.name is not None:
            object_name_array.append("name::")
            object_name_array.append(self.name)
        if self.title is not None:
            object_name_array.append("title::")
            object_name_array.append(self.title)
        if self.classname is not None:
            object_name_array.append("classname::")
            object_name_array.append(self.classname)
        if self.type is not None:
            object_name_array.append("type::")
            object_name_array.append(self.type)
        if self.multiple_text is not None and len(self.multiple_text) > 0:
            object_name_array.append("multiple_text::")
            object_name_array.append(str(self.multiple_text))
        if self.href is not None:
            object_name_array.append("href::")
            object_name_array.append(self.href)
        if self.tag is not None:
            object_name_array.append("tag::")
            object_name_array.append(self.tag)

        if "text::" in object_name_array and "id::" in object_name_array:
            object_name = object_name_array[1] + "_" + object_name_array[3]
        elif "text::" in object_name_array:
            object_name = object_name_array[1]
        elif "id::" in object_name_array:
            index = object_name_array.index("id::") + 1
            object_name = object_name_array[index]
        elif "name::" in object_name_array:
            index = object_name_array.index("name::") + 1
            object_name = object_name_array[index]
        elif "title::" in object_name_array:
            index = object_name_array.index("title::") + 1
            object_name = object_name_array[index]
        elif "classname::" in object_name_array:
            index = object_name_array.index("classname::") + 1
            object_name = "class_" + object_name_array[index]
            if " " in object_name:
                object_name = object_name.replace(" ", "_")
                object_name = "multi_" + object_name
        elif "type::" in object_name_array:
            index = object_name_array.index("type::") + 1
            object_name = "type_" + object_name_array[index]
        elif "href::" in object_name_array:
            index = object_name_array.index("href::") + 1
            object_name = "link_to_" + object_name_array[index]
        elif "multiple_text::" in object_name_array:
            index = object_name_array.index("multiple_text::") + 1
            object_name = "list_first_elem_" + self.multiple_text[0]
        elif "tag::" in object_name_array:
            index = object_name_array.index("tag::") + 1
            object_name = "ambiguous_html_tag" + object_name_array[index] + "_" + self.html_id

        return object_name


def HTMLFilterer(url, html_tags):
    data_array = []
    html_id = 0

    for tag in html_tags:
        soup = htmlsoup(url).find_all(tag)

        for i in soup:
            html_element_array = []
            parser = utils.HTMLParser()
            parser.feed(str(i))
            # print("HTML_PARSE_ID: " + str(html_id) + "\n" + parser.return_data())
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
                elem.set_text(i[3][0])
                elem.set_multiple_text(i[3])

        element_array.append(elem)

    return element_array



#arrr = HTMLFilterer(url, html_tags)
