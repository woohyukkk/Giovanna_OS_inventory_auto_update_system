#!/usr/bin/python
import os
import csv
import smtplib
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter
# This tool help combo PDF files ex.1234.pdf + 1234-2.pdf = 1234.pdf(2 pages)

for filename in os.listdir("."):
    if "-2" in filename:
        l=len(filename) - 6
        print (filename[0:l]+"   +++++++++++   "+filename)
        output = PdfFileWriter()
        try:
          f1=open(filename[0:l]+".pdf", "rb")
        except Exception:
          print ("ERROR: cant find file: "+filename[0:l]+".pdf")
        f2=open(filename, "rb")
        input1 = PdfFileReader(f1)
        input2 = PdfFileReader(f2)
        page1=input1.getNumPages()
        page2=input2.getNumPages()
        for i in range (page1):
          output.addPage(input1.getPage(i))
        for i in range (page2):
          output.addPage(input2.getPage(i))
        outputStream = open("New"+".pdf", "wb")
        output.write(outputStream)
        outputStream.close()
        f1.close()
        f2.close()
        os.remove(filename)
        os.remove(filename[0:l]+'.pdf')
        os.renames("New.pdf",filename[0:l]+'.pdf')


