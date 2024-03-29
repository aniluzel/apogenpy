import os.path
import random
import sys
from urllib.parse import urlparse
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import utils
import selenium
from PIL import Image


def file_gen(url, html_object_array):
    invalid = '<>:"/\|?* -..&, …{}()\'@’[]+“”!#;™​—'
    parsed_url = utils.urlparse(url)
    folder_path = utils.folder_name_changer(parsed_url[1]) + "_POM"
    file_name = utils.file_name_changer(parsed_url[2])

    if not valid_url(url):
        url_temp = url
        temp = url_temp.split("/")
        file_name = temp[len(temp) - 1]
        folder_path = temp[len(temp) - 1] + "_POM"

        # if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
        #     url_temp = url
        #     temp = url_temp.split("/")
        #     file_name = temp[len(temp) - 1]
        #     folder_path = temp[len(temp) - 1] + "_POM"
        # else:
        #     url_temp = url
        #     temp = url_temp.split("\\")
        #     file_name = temp[len(temp) - 1]
        #     folder_path = temp[len(temp) - 1] + "_POM"

    if file_name == "":
        file_name = folder_path + "_" + str(random.randint(0, 1000))

    for char in invalid:
        folder_path = folder_path.replace(char, '_')
        file_name = file_name.replace(char, '_')

    if not utils.os.path.exists(folder_path):
        utils.os.mkdir(folder_path)
    else:
        print("Directory already exists")

    if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
        directory = folder_path + "/" + file_name
    else:
        directory = folder_path + "\\" + file_name

    with open(directory + ".py", "w", encoding="utf-8") as f:
        f.write("import testdriver\n\nurl = \"" + url + "\"\ndriver = testdriver.Driver.driver\n\n\ndef driver_goto("
                                                        "):\n\tdriver.get(url)\n\n\ndef driver_quit():\n\tdriver.quit()\n")

        object_duplicates = []
        name_duplicates = []
        duplicate_id = []
        duplicate_counter = []

        for html_object in html_object_array:

            object_name = html_object.object_name_picker()
            object_params = html_object.object_param_picker()
            object_comments = []

            if "class::" + str(html_object.classname) in object_params:
                index_class = object_params.index("class::" + str(html_object.classname))
                temp_class = object_params[index_class].split("::")[1].split(" ")

                if len(temp_class) > 1:
                    object_comments.append("# Class names: " + ", ".join(temp_class))
                    object_params[index_class] = "class::" + str(max(temp_class, key=len))

            if len(html_object.list_text) > 1:
                object_comments.append("# List values: " + str(html_object.list_text))

            for char in invalid:
                object_name = object_name.replace(char, '_')

            object_param_value_default = object_params[0].split("::")[1]
            object_param_type_default = object_params[0].split("::")[0]

            if object_name == "":
                object_name = str(html_object.tag) + "_" + object_param_type_default

            if object_name[0].isdigit() or object_name[0] == "_":
                object_name = object_name[1:]
                object_name += str(html_object.tag) + "_" + object_param_type_default + "_" + object_name
                while object_name[0].isdigit():
                    object_name = object_name[1:]

            if object_name[0] == "_":
                while object_name[0] == "_":
                    object_name = object_name[1:]

            if "text" in object_param_type_default:
                object_param_type_default = "normalize-space(text())"
            else:
                object_param_type_default = "@" + object_param_type_default
            object_param_tag = object_params[object_params.index("tag::" + html_object.tag)].split("::")[1]

            combined_object = "{},{},{}".format(object_param_tag, object_param_type_default, object_param_value_default)

            if object_name in name_duplicates:
                object_comments.append("# Method name is assigned an ID to avoid problems. "
                                       "You are free to change method names.")
                object_name += "_" + str(html_object.html_id)
            else:
                name_duplicates.append(object_name)

            duplicate_index = 0

            if combined_object in object_duplicates:
                object_comments.append("# Duplicate method found. Consider manually changing object type and value.")

                if object_duplicates.index(combined_object) in duplicate_id:
                    index = duplicate_id.index(object_duplicates.index(combined_object))
                    duplicate_counter[index] += 1
                    duplicate_index = duplicate_counter[index]

                else:
                    duplicate_id.append(object_duplicates.index(combined_object))
                    duplicate_counter.append(1)
                    duplicate_index = 1

            else:
                object_duplicates.append(combined_object)

            if len(object_params) > 1:
                object_comments.append("# You can change the tag and value parameter of the method from the list below")
                object_comments.append("# List of alternative object tags and parameters: " + str(object_params))

            f.write("\n\n# html_id_{}\ndef {}(input=\"\", timeout=0.35):\n\ttestdriver.selenium(driver, input, timeout, '{}', '{}',"
                    " '{}', {})\n\t".format(str(html_object.html_id), object_name, object_param_tag, object_param_type_default,
                                        object_param_value_default, duplicate_index) + "\n\t".join(object_comments) + "\n")

    with open("TEST_FILE_" + folder_path.removesuffix("_POM") + ".py", "a") as f:
        f.write("import " + folder_path + "." + file_name + " as " + file_name + "\n# Start testing by typing in"
                " {}.driver_goto() or choose from available methods inside {}.py\n".format(file_name, file_name))


def valid_url(to_validate: str) -> bool:
    o = urlparse(to_validate)
    return True if o.scheme and o.netloc else False


def htmlsoup(url):
    is_url = valid_url(url)

    if is_url:
        page_html = utils.requests.get(url).text
        soup = utils.BeautifulSoup(page_html, "html.parser")
    else:
        page_html = open(url, "r", encoding="utf-8")
        soup = utils.BeautifulSoup(page_html, "html.parser")

    return soup


# url = 'http://localhost:8080/owners/2/pets/new'
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
        self.list_text = []

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

    def set_list_text(self, list_text):
        self.list_text = list_text

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
        if len(self.list_text) > 0:
            print("list text: " + str(self.list_text))
        print()

    def GUI_highlight_info(self):
        if self.text is not None:
            return self.text
        else:
            return ""

    def get_html_id(self):
        return self.html_id

    def get_element_screenshot(self, url, patharray):
        chromepath = utils.chromedriver_path_name()
        chromeoptions = Options()
        chromeoptions.add_argument('--force-device-scale-factor=1')
        chromeoptions.add_argument("--headless")
        chromeoptions.add_argument(f"--window-size=1920x{patharray[3]}")
        # driver = utils.webdriver.Chrome(chromepath, options=chromeoptions)
        # driver.get(url)

        object_params = self.object_param_picker()

        object_param_value_default = object_params[0].split("::")[1]
        object_param_type_default = object_params[0].split("::")[0]

        if "text" in object_param_type_default:
            object_param_type_default = "normalize-space(text())"
        else:
            object_param_type_default = "@" + object_param_type_default
        object_param_tag = object_params[object_params.index("tag::" + self.tag)].split("::")[1]

        try:
            driver = patharray[2]

            ## TRY CATCH FOR SELENIUM EXCEPTION AND IMAGE NOT FOUND FILE NOT FOUND
            elem = driver.find_element(By.XPATH, "//{}[{}='{}']".format(object_param_tag, object_param_type_default, object_param_value_default))
            loc = elem.location
            size = elem.size
            x = loc['x']
            y = loc['y']
            height = y + size['height']
            width = x + size['width']
            img = Image.open(patharray[0])
            img_cropped = img.crop((int(x) - 20, int(y) - 20, int(width) + 20, int(height) + 20))
            img_cropped.save(patharray[1] + str(self.html_id) + ".png")
            img_path = patharray[1] + str(self.html_id) + ".png"
            # ob = Screenshot.Screenshot()
            # img_url = ob.get_element(driver,elem, save_location=patharray[1],image_name=str(self.html_id) + ".png")

        except (NoSuchElementException, FileNotFoundError, ElementNotInteractableException) as error:
            print(error)

        return img_path

    def GUI_window_adder(self):
        gui_string = "!undefined_element"

        if self.text is not None and len(self.list_text) == 0 and len(self.text) > 0:
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
        elif self.list_text is not None and len(self.list_text) > 0:
            gui_string = "First Value of List -> " + self.list_text[0]
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
        if self.text is not None and len(self.text) > 0:
            gui_string_array.append("Text: " + self.text)
        if self.name is not None:
            gui_string_array.append("Name: " + self.name)
        if self.title is not None:
            gui_string_array.append("Title: " + self.title)
        if self.type is not None:
            gui_string_array.append("Type: " + self.type)
        if self.href is not None:
            gui_string_array.append("Href: " + self.href)
        if self.list_text is not None and len(self.list_text) > 0:
            gui_string_array.append("List Values: " + self.list_text[0])

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

        if self.text is not None and len(self.text) > 0:
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
        if self.list_text is not None and len(self.list_text) > 0:
            object_name_array.append("list_text::")
            object_name_array.append(str(self.list_text))
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
                object_name = "multi_" + object_name.split(" ")[0]
        elif "type::" in object_name_array:
            index = object_name_array.index("type::") + 1
            object_name = "type_" + object_name_array[index]
        elif "href::" in object_name_array:
            index = object_name_array.index("href::") + 1
            object_name = "link_to_" + object_name_array[index]
        elif "list_text::" in object_name_array:
            object_name = "list_first_elem_" + self.list_text[0]
        elif "tag::" in object_name_array:
            index = object_name_array.index("tag::") + 1
            object_name = "ambiguous_html_tag" + object_name_array[index]

        return object_name

    def object_param_picker(self):
        object_param_array = []

        if self.id is not None:
            object_param_array.append("id::" + self.id)
        if self.href is not None:
            object_param_array.append("href::" + self.href)
        if self.text is not None and len(self.text) > 0:
            object_param_array.append("text::" + self.text)
        if self.name is not None:
            object_param_array.append("name::" + self.name)
        if self.title is not None:
            object_param_array.append("title::" + self.title)
        if self.classname is not None:
            object_param_array.append("class::" + self.classname)
        if self.type is not None:
            object_param_array.append("type::" + self.type)
        if self.list_text is not None and len(self.list_text) > 0:
            object_param_array.append("list::" + self.list_text[0])
        if self.tag is not None:
            object_param_array.append("tag::" + self.tag)

        return object_param_array


def get_page_screenshot(url):
    chromepath = utils.chromedriver_path_name()
    chromeoptions = Options()
    chromeoptions.add_argument('--force-device-scale-factor=1')
    chromeoptions.add_argument("--headless")
    #chromeoptions.add_argument("--window-size=2000x4000")
    driver = utils.webdriver.Chrome(chromepath, options=chromeoptions)

    driver.get(url)
    driver.maximize_window()
    height = driver.execute_script("return document.documentElement.scrollHeight")
    # print(height)
    size = "--window-size=1920x{}".format(height)
    driver.set_window_size(1920,height)
    parsed_url = utils.urlparse(url)

    folder_path = utils.folder_name_changer(parsed_url[1]) + "_screenshots"
    png_file_name = utils.file_name_changer(parsed_url[2]) + ".png"

    if not valid_url(url):
        if not valid_url(url):
            url_temp = url
            temp = url_temp.split("/")
            folder_path = temp[len(temp) - 1] + "_screenshots"
            png_file_name = temp[len(temp) - 1] + ".png"

            # if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
            #     url_temp = url
            #     temp = url_temp.split("/")
            #     folder_path = temp[len(temp) - 1] + "_screenshots"
            # else:
            #     url_temp = url
            #     temp = url_temp.split("\\")
            #     folder_path = temp[len(temp) - 1] + "_screenshots"

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        abspath = os.path.abspath(folder_path)

    else:
        abspath = os.path.abspath(folder_path)


    if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
        screen_shot_loc = [f"{abspath}" + "/" + png_file_name,
                           f"{abspath}" + "/" + utils.file_name_changer(parsed_url[2]), driver, height]
    else:
        screen_shot_loc = [f"{abspath}" + "\\" + png_file_name,
                           f"{abspath}" + "\\" + utils.file_name_changer(parsed_url[2]), driver,height]


    ##ob = Screenshot.Screenshot()
    # img_url = ob.full_Screenshot(driver, save_path= folder_path, image_name=png_file_name )
    driver.save_screenshot(screen_shot_loc[0])
    return screen_shot_loc


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
                elem.set_list_text(i[3])

        element_array.append(elem)

    return element_array
