# This tool help combo PDF files ex.1234.pdf + 1234-2.pdf = 1234.pdf(2 pages)
#V2 now can combo n pages
import os
import csv
import smtplib
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter


def comboPDF(file1,file2,newfile):
        print (file1+"   +++++++++++   "+file2)
        output = PdfFileWriter()
        f1=open(file1, "rb")
        f2=open(file2, "rb")
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
        try:
           os.remove(file1)
           os.remove(file2)
        except Exception:
           print ("ERROR: Can't remove file" )
        os.renames("New.pdf",newfile)

comboList=[]
for filename in os.listdir("."):
    if '.pdf' in filename:
      if '-'in filename:
        print ('-n detected in',filename)
        s=filename.find('-')
        file=filename[0:s]
        index=filename[s+1:]
        if index=='2.pdf':
           comboList.append(file+'.pdf')
        print ("File:",file,"index:",index)
        if (file+'.pdf') not in comboList:
           comboList.append(file+'.pdf')
        else:
           comboPDF(file+'.pdf',filename,file+'.pdf')



