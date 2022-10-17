import utils


def file_gen(url):

    parsed_url = utils.urlparse(url)
    folder_path = utils.folder_name_changer(parsed_url[1]) + "-POM"
    if not utils.os.path.exists(folder_path):
        utils.os.mkdir(folder_path)
    else:
        print("Directory already exists, moving on")

    #folderpathname= utils.folder_name_changer(domain[1])+"-POM"
    file_name = utils.file_name_changer(parsed_url[2]) #owners_1
    with open(folder_path + "\\" + file_name + ".py", "a") as f:
        f.write("# File write success" + "\n") ##importlar gelicek dosya içine yazma id finder vs de olcak


#def idfinder(array):
 #   url = array
  #  page_html = requests.get(url).text
   # soup = BeautifulSoup(page_html, "html.parser")
   # idSoup = [tag['id'] for tag in soup.find_all(id=True)]

    #burada dosyalar generate edilecek