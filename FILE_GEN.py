import csv

# obsolete
def filegenerator(param, url, elemid):
    invalid = '<>:"/\|?* '
    filename = url + ".py"
    for char in invalid:
        filename = filename.replace(char, '_').removeprefix('http://localhost:8080')
    with open(filename, 'a') as f:
        f.write("\ndef " + elemid + "(input=\"\"):\n\t" + elemid + " = POM_GEN.ObjectGen(\'" + param + "\', driver.driver)"
            "\n\tif not input:\n\t\t" + elemid + ".object.click()\n\telse:\n\t\t" + elemid + ".object.send_keys(input)\n\n")


def importgenerator(url):
    invalid = '<>:"/\|?* '
    filename = url + ".py"
    for char in invalid:
        filename = filename.replace(char, '_').removeprefix('http://localhost:8080')

    imports = "import POM_GEN"
    with open(filename, 'w') as f:
        f.write(imports)
        f.write("\n""driver = POM_GEN.Driver(\'" + url + "\')\n\n")


def gen(url):
    importgenerator(url)
    filename1 = url
    invalid = '<>:"/\|?* '
    for char in invalid:
        filename1 = filename1.replace(char, '_').removeprefix('http://localhost:8080')
    with open("GENERATED_CSV/"+filename1+".csv", "r") as f:
        reader = csv.reader(f)
        row1 = next(reader)
        ids = row1
        next(reader)
        row2 = next(reader)
        buttons = row2
        print(buttons)

        for elem in ids:
            filegenerator(elem, url, elem.replace('-', '_'))

        newlist = [word for line in buttons for word in line.split(",")]
        print(newlist)
        for elem in newlist:

            elem=(elem.split(">"))[1].split("<")[0]
            if(len(elem)>1):
                elem1 = "//button[text()=\\\'"+elem+"\\\']"
                filegenerator(elem1, url, elem.replace(' ', '_'))
