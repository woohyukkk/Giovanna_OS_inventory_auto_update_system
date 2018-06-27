import os
import csv
import smtplib
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter

output = PdfFileWriter()
PTN=''
total=0
for filename in os.listdir("."):
     if 'pdf' in filename:
       l=len(filename) - 4
       name=filename[0:l]
       s1=name.find('#')
       if s1!=-1:
         number=name[s1+2:len(name)]
         if total==0:
           PTN=PTN+' '+number
           total+=1
         else:
           PTN=PTN+', '+number
           total+=1
       else:
         print ('cant find # in filename')
         continue
       f1=open(filename, "rb")
       input= PdfFileReader(f1)
       page=input.getNumPages()

       print ( 'Name:',name,'NO.:',number,'Page:',page)
       for i in range (page):
          output.addPage(input.getPage(i))
print ('Total processed:',total,'Writing '+'PT# '+PTN+".pdf")
outputStream = open('PT# '+PTN+".pdf", "wb")
output.write(outputStream)
outputStream.close()