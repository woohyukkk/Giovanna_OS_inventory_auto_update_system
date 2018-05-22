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
        f1=open(filename[0:l]+".pdf", "rb")
        f2=open(filename, "rb")
        input1 = PdfFileReader(f1)
        input2 = PdfFileReader(f2)
        output.addPage(input1.getPage(0))
        output.addPage(input2.getPage(0))
        outputStream = open("New"+".pdf", "wb")
        output.write(outputStream)
        outputStream.close()
        f1.close()
        f2.close()
        os.remove(filename)
        os.remove(filename[0:l]+'.pdf')
        os.renames("New.pdf",filename[0:l]+'.pdf')


