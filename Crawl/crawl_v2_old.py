# Import

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def write_to_csv(list_input):
    # The scraped info will be written to a CSV here.
    try:
        with open("URls.csv", 'w', newline='') as fopen:  # Open the csv file.
            for domain in list_input:
                fopen.write(domain + '\n')
    except:
        return False


# Define Browser Options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Hides the browser window
# Reference the local Chromedriver instance
#chrome_path = r'C:\chromedriver.exe'
chrome_path = r'/Users/denis/Documents/CS401/chromedriver'
driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
# Run the Webdriver, save page an quit browser
driver.get("http://localhost:8080/owners/find")

general = []

checked = []


def crawl_one(page_url, domain):
    general = []

    # global general
    driver.get(page_url)
    # Scroll page to load whole content
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page
        # time.sleep(2)
        # Calculate new scroll height and compare with last height.
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    htmltext = driver.page_source

    # Parse HTML structure
    soup = BeautifulSoup(htmltext, "html.parser")

    for link in soup.find_all("a", href=True):

        if link.get('class') is not None:

            if link.get('class')[0] == "btn":
                tmp = link.get('href')
                tmp = tmp.split("/", 2)
                if driver.current_url + link.get('href') not in checked:
                    if driver.current_url + "/" + link.get('href') not in checked:
                        prev = driver.current_url
                        # print(prev)
                        # print(link.text)
                        #  if "\n" not in link.text:
                        #     # print("here")
                        #      bt = driver.find_element(By.PARTIAL_LINK_TEXT, link.text)
                        #  else:
                        #      # print(link.text)
                        #      yyt = link.text.split("\n", 1)
                        #
                        #      yyt = yyt[0] + yyt[1]
                        #
                        #      yyt = yyt.split(" ", 1)
                        #    #  print(yyt[0])
                        #      yyt = yyt[0].replace(" ", "") +" "+ yyt[1].lstrip(' ')
                        #      # print(len(yyt))
                        #    #  print(yyt + " ytt")
                        #      bt = driver.find_element(By.PARTIAL_LINK_TEXT, yyt)
                        bt = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//a[@href="' + link.get('href') + '"]')))
                        bt.click()
                        print(driver.current_url + " == btn")
                        general.append(driver.current_url)
                        driver.get(prev)


            # navlink parsing
            elif link.get('class')[0] == "nav-link":
                if domain + link.get('href') not in checked:
                    print(domain + link.get('href') + " == navlink")
                    general.append(domain + link.get('href'))

            else:
                tmp3 = link.get('href')
                tmp3 = tmp3.split("/", 1)

                if link.get('class')[0] == "fa":
                    if domain + link.get('href') not in checked:
                        print(domain + link.get('href') + " == forward")
                        general.append(domain + link.get('href'))

                elif driver.current_url + link.get('href') not in checked:
                    if driver.current_url + "/" + tmp3[1] not in checked:
                        if tmp3[1] != "":
                            print(driver.current_url + "/" + tmp3[1] + " == not btn")

                            general.append(driver.current_url + "/" + tmp3[1])



        else:
            tmp2 = link.get('href')
            tmp2 = tmp2.split("/", 1)

            if driver.current_url + link.get('href') not in checked:
                if driver.current_url + "/" + tmp2[1] not in checked:
                    prev1 = driver.current_url
                    # print(driver.current_url + " ==  current page")
                    # press = driver.find_element(By.PARTIAL_LINK_TEXT, element[0].lstrip(" ") + " " + element[1].lstrip(" "))

                    press = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//a[@href="' + link.get('href') + '"]')))

                    # press = driver.find_element(By.XPATH, '//a[@href="'+link.get('href')+'"]')
                    try:
                        press.click()
                        print(driver.current_url + " == no class")
                        general.append(driver.current_url)
                        driver.get(prev1)
                    except WebDriverException:
                        print("Element is not clickable")
                    # else:
                    #
                    #
                    #     # if len(element) == 1:
                    #     # # element[0] = element[0].replace("'", "")
                    #     # # element[0] = element[0].replace("'", "")
                    #     #     press = driver.find_element(By.PARTIAL_LINK_TEXT, str(element[0]))
                    #     # else:
                    #     #     press = driver.find_element(By.PARTIAL_LINK_TEXT, element)
                    #     press = WebDriverWait(driver, 10).until(
                    #         EC.element_to_be_clickable((By.XPATH, '//a[@href="' + link.get('href') + '"]')))
                    #     press.click()

    # else:
    #     # print(link.get('href'))
    #     # print("not here")
    #     tmp2 = link.get('href')
    #     tmp2 = tmp2.split("/", 1)
    #     if link.get('class') is not None:
    #
    #         # print(link.get('class')[0])
    #         if link.get('class')[0] == "nav-link":
    #             if domain + link.get('href')not in checked:
    #                 print(domain + link.get('href')+" == navlink 2")
    #                 general.append(domain + link.get('href'))
    #                 count.append(0)
    #     else:
    #      if driver.current_url + link.get('href') not in checked:
    #         if driver.current_url + "/" + tmp2[1] not in checked:
    #             print(driver.current_url + "/" + tmp2[1] + " == array empty")
    #             general.append(driver.current_url + link.get('href'))
    #             count.append(0)

    for button_case in soup.find_all("button", type='submit'):
        if button_case.get('class')[1] == "btn-primary":

            button = driver.find_element(By.CLASS_NAME, button_case.get("class")[1])
            button.click()

            item = driver.current_url

            if item not in checked:
                print(item + " == submit button")
                general.append(item)

    return general


def looping(array, domain):
    for i in array:
        if i not in checked:
            checked.append(i)
            looping(crawl_one(i, domain), domain)


if __name__ == '__main__':
    # print(crawl_one("http://localhost:8080/owners/1"))
    start_url = "http://localhost:8080"
    domain = "http://localhost:8080"
    looping(crawl_one(start_url, domain), domain)
    print(str(len(checked)) + " sites crawled")
    write_to_csv(checked)
    driver.quit()
