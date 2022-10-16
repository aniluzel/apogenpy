# demo.py, file_gen.py ve pom_gen.py bu dosyada olacak
# bütün url okuma, element bulma, page object oluşturma ve page object içlerine element functionları yazma bu dosyada olacak
import os
import utils


#crawler url data buraya gelicek
url = ["http://localhost:8080/owners/find","http://localhost:8080/owners/new","http://localhost:8080/"]
def filegen(url):

    folderpathuntrimmed = utils.urlparse(url[0])
    folderpath=utils.folder_name_changer(folderpathuntrimmed[1])
    folderpath = folderpath+"-POM"
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)
    else:
        print("Directory already exist moving on")

    for urls in url:
        domain = utils.urlparse(urls)
        #folderpathname= utils.folder_name_changer(domain[1])+"-POM"
        filename = utils.file_name_changer(domain[2]) #owners_1
        with open(folderpath+"\\"+ filename+".py", "a") as f:
            f.write("asdasdadsadasddasdas"+"\n") ##importlar gelicek dosya içine yazma id finder vs de olcak


#def idfinder(array):
 #   url = array
  #  page_html = requests.get(url).text
   # soup = BeautifulSoup(page_html, "html.parser")
   # idSoup = [tag['id'] for tag in soup.find_all(id=True)]

    #burada dosyalar generate edilecek

filegen(url)