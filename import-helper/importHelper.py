print('''Viedoc Data Import Application Helper, version 1.\n

This application helps with the setup of data imports via the Data Import Application.
Step 1: Create your data mappings in Viedoc Designer - Global Design Settings.
Step 2: Publish your Global Design Settings and download the mapping files.
Step 3: Create one main folder for your imports and place all your mapping files in it.
Step 4: Create a WCF API client in Viedoc Admin. Copy the GUID.
Step 5: Run this application.
''')

from tkinter import Tk
from tkinter.filedialog import askdirectory,askopenfilename
import os.path
import os
import re
import csv

def checkMappingFiles(pars):
    #This function searches the mapping files for some common mistakes.
    warnings = 0
    for i in pars["mappingfiles"]:
        with open(pars["path"] + "/" + i, "r") as f:
            mf = f.read()
        #The mapping file must contain a mapped {SiteCode}:
        if not re.search("{SiteCode}", mf):
            print("SiteCode not defined in mapping file " + i + "!")
            warnings += 1
        #Sometimes the $-sign is forgotten in $THIS:
        if re.search("{THIS", mf):
            print("THIS used instead of $THIS in mapping file " + i + "!")
            warnings += 1
        #Newlines in the Column Name are indicated &#xa; and can interfere with the mapping:
        newlines = re.findall("(?<=SASFieldName=\")[\w\s]+(?=&#xA;)", mf)
        for j in newlines:
            print("There is a newline in column name " + j + " in mapping file " + i + "!")
            warnings += 1
        #Extra whitespaces at the end of the Column Name can interfere with the mapping:
        extraspaces = re.findall("(?<=SASFieldName=\")[\w\s]+(?=\s\"\>)", mf)
        for j in extraspaces:
            print("There is a whitespace at the end of column name " + j + " in mapping file " + i + "!")
            warnings += 1
    return warnings

def writexml(pars):
    with open(pars["path"] + "/" + "config.xml", "a") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>')
        f.write('\n<ViedocImportConfiguration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n')
        f.write('<BasePath>' + pars["path"] + '</BasePath>\n')
        for i in pars["mappingfiles"]:
            f.write('<ImportConfiguration>\n')
            f.write('<FolderName>' + i[:-4] + '</FolderName>\n')
            f.write('<DefineXmlFileName>' + i + '</DefineXmlFileName>\n')
            f.write('<FileEncoding>utf-8</FileEncoding>\n')
            f.write('<FileDelimiter>' + pars["delimiter"] + '</FileDelimiter>\n')
            f.write('<ApiUrl>' + pars["server"] + '</ApiUrl>\n')
            f.write('<ClientGuid>' + pars["GUID"] + '</ClientGuid>\n')
            f.write('<UserName>' + pars["email"] + '</UserName>\n')
            f.write('<AllowCreatingSubjects>' + pars["createSubj"] + '</AllowCreatingSubjects>\n')
            f.write('<AllowInitiatingStudyEvents>' + pars["initEvent"] + '</AllowInitiatingStudyEvents>\n')
            f.write('</ImportConfiguration>\n')
        f.write('</ViedocImportConfiguration>')

runApp = input("Did you complete the above steps? [Y/N]: ").strip()
yes = ["Y", "Yes", "y", "yes", "True", "true", "1"]
if runApp in yes:
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    pars = {}
    print("Select the main folder for your imports (containing the mapping files).")
    pars["path"] = askdirectory(title = "Select the main folder for your imports.", parent = root)
    pars["mappingfiles"] = [x for x in os.listdir(pars["path"]) if x.endswith(".xml")]
    print("")
    warnings = checkMappingFiles(pars)
    if warnings == 1:
        print("\nThere was " + str(warnings) + " warning about your mapping file(s). It is recommended to fix it first.")
        runApp = input("Continue running this program anyway? [Y/N]: ").strip()
    if warnings > 1:
        print("\nThere were " + str(warnings) + " warnings about your mapping file(s). It is recommended to fix them first.")
        runApp = input("Continue running this program anyway? [Y/N]: ").strip()
if runApp in yes:
    print("Select one of your CSV files.")
    csvFile = askopenfilename(title = "Select one of your CSV files.", parent = root)
    with open(csvFile) as f:
        pars["delimiter"] = csv.Sniffer().sniff(f.read(1000)).delimiter
    print('The delimiter in your CSV file is "' + pars["delimiter"] + '".')
    serverType = 0
    while serverType not in ["1", "2"]:
        serverType = input("On which server TYPE is your study? 1=Production, 2=Training [1/2]: ").strip()
    if serverType == "1":
        serveroptions = ["https://v4api.viedoc.net/HelipadService.svc", "https://api.us.viedoc.com/HelipadService.svc", "https://v4apijp.viedoc.net/HelipadService.svc", "https://api.viedoc.cn/HelipadService.svc"]
    elif serverType == "2":
        serveroptions = ["https://v4apitraining.viedoc.net/HelipadService.svc", "https://apitraining.us.viedoc.com/HelipadService.svc", "https://v4apitrainingjp.viedoc.net/HelipadService.svc", "https://apitraining.viedoc.cn/HelipadService.svc"]
    serverRegion = 0
    while serverRegion not in ["1", "2", "3", "4"]:
        serverRegion = input("On which server REGION is your study? 1=EU, 2=US, 3=Japan, 4=China [1/2/3/4]: ").strip()
    pars["server"] = serveroptions[int(serverRegion) - 1]
    pars["GUID"] = ""
    while not re.search(r"^[0-9a-f-]{36}$", pars["GUID"]):
        pars["GUID"] = input("Provide the study GUID obtained from Viedoc Admin - API Configuration: ").strip()
    pars["email"] = ""
    while not re.search(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$', pars["email"]):
        pars["email"] = input("What is the email address for the account performing the imports?: ").strip()
    pars["createSubj"] = "true" if input("Is the import allowed to create subjects? [Y/N]: ").strip() in yes else "false"
    pars["initEvent"] = "true" if input("Is the import allowed to initiate events? [Y/N]: ").strip() in yes else "false"
    writexml(pars)
    print("\nConfiguration file created!")
    for i in pars["mappingfiles"]:
        if not os.path.exists(pars["path"] + "/" + i[:-4]):
            os.makedirs(pars["path"] + "/" + i[:-4])
        os.rename(pars["path"] + "/" + i, pars["path"] + "/" + i[:-4] + "/" + i)
    print('''Subfolders created for each import (for each mapping file).

    \nNext steps:
1. Download the Data Import Application from Viedoc Designer.
2. Place your CSV data files in the correct subfolders.
3. Run the Data Import Application.
4. (Optional) Set up Task Scheduler: https://help.viedoc.net/l/5b5c16/en/''')
print("Program ended.")