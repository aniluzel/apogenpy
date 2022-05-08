import csv


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


# MAIN
# Needs change in order to read from csv
# DATA FROM CRAWLER NEEDS TO BE FED
# -------------------------------------------------------------------------------

importgenerator("http://localhost:8080/owners/new")  # url from csv as filename

with open("GENERATED_CSV/DEMO_SCRAP.csv", "r") as f:
    reader = csv.reader(f)
    row1 = next(reader)
    ids = row1
    print(ids)
    next(reader)
    row2 = next(reader)
    buttons = row2
    print(buttons)


    for elem in ids:
        filegenerator(elem, "http://localhost:8080/owners/new", elem.replace('-', '_'))

    #newbuttons = buttons(list).split(",")
    newlist = [word for line in buttons for word in line.split(",")]
    print(newlist)
    for elem in newlist:

        elem=(elem.split(">"))[1].split("<")[0]
        if(len(elem)>1):

            filegenerator(elem, "http://localhost:8080/owners/new", elem.replace(' ', '_'))




# filegenerator("testid","testlink","testclass","testcss","http://localhost:8080/owners/new")
