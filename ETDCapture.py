__author__ = 'fenichele'
"""Program to capture ETDs from Digital Library"""

import tkinter
import csv
import urllib.request
import requests
import os

root = tkinter.Tk()
root.withdraw()

webPrefix = 'http://fau.digital.flvc.org'
testURL = 'http://purl.flvc.org/fau/fd/FA00004426'

def loadURLs():
    """load the csv list of URLs"""
    from tkinter import filedialog

    marcPath = tkinter.filedialog.askopenfile()
    PDFFile = marcPath.name

    pdfList = []

    with open(PDFFile, 'r') as f:
        reader = csv.reader(f)
        pdfFileList = list(reader)

    for row in pdfFileList:
        pdfList.append(row)

    return pdfList


def returnURL(row):

    try:
        url2Use = row[1]
        req = requests.get(url2Use)
    except ValueError:
        print("ValueError with ", row)

    return url2Use

def returnPDFURL(testurl):

    embargoPhrase = 'http://fau.digital.flvc.org/node/14'
    searchPhrase = 'Download pdf'
    endField = '"'

    with urllib.request.urlopen(testurl) as response:
        html = response.read()

        # print(response.geturl())
        if response.geturl() == embargoPhrase:
            return '-1'


    startText = html.decode().find(searchPhrase)+16
    endText = html.decode().find(endField, startText)
    endText2 = html.decode().find(endField, endText+2)

    htmlString = html.decode()


    pdfURL = htmlString[endText+1:endText2]
    useURL = webPrefix+pdfURL

    return useURL

def getNameOfFile(row):
    try:
        name2Use = row[0]
    except ValueError:
        print("ValueError with ",row)

    return name2Use

def writePDFToFile(saveDirectory, pdfURL, name):
    path = saveDirectory
    pdfFile = name+'.pdf'

    filename = os.path.join(path, pdfFile)

    req = requests.get(pdfURL)
    with open(filename, 'wb') as x:
        x.write(req.content)

def chooseSaveDirectory():
    from tkinter import filedialog

    saveDirect = tkinter.filedialog.askdirectory()

    return saveDirect

def downloadETDs():

    print("this program will download the PDFs from a CSV file...\n")
    cont = input("press any key to select your Save Directory or 'n' to cancel...\n")
    if cont == 'n':
        print("\nUser entered 'n' to cancel!")
        return

    saveD = chooseSaveDirectory()

    cont = input("press any key to select your CSV file or 'n' to cancel...\n")
    if cont == 'n':
        print("\nUser entered 'n' to cancel!")
        return

    records = loadURLs()
    print("\nThanks! Getting PDFs, I'll let you know when I'm done\n")


    for r in records:
        url = returnURL(r)
        name = getNameOfFile(r)

        pdfURL = returnPDFURL(url)
        if pdfURL == '-1':
            print(name, "is embargoed, skipping...")
            continue
        print("getting ", pdfURL)

        writePDFToFile(saveD, pdfURL, name)

        print("retrieved PDF for ", name)

    print("\nFinished!")



