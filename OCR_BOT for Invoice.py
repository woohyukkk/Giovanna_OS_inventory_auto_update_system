import os
import csv
import smtplib
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter

for filename in os.listdir("."):
     if 'pdf' in filename:
       l=len(filename) - 4
       try:
         f=open(filename[0:l]+'.txt','r')
       #print (filename[0:l]+'.txt')
       except Exception:
         print ("No txt file:",filename)
         continue
       text=f.read()
       pt=text.find('PT#')
       if pt!=-1:
         newName=text[pt+4:pt+9]
         try:
           os.rename(filename,"Shipping_PT# "+newName+'-2.pdf')
         except Exception:
           print('cant rename',filename)
       s1=0
       s2=0
       n=2
       while(s2-s1<5):
         #print ('while.....')
         s1=text.find('*',s2+1)
         s2=text.find('*',s1+1)
         if(s1==-1)or(s2==-1):
           break
       Inv=text[s1+1:s2].split()
       s3=text.find('INVOICE')
       
       s=''
       for item in Inv:
           s=s+item
       if s3!=-1:
          s=text[s3+3+6:s3+8+6]
       if len(s)>6:
         print ('ERROR: cant find INV#:',filename)
         continue
       newName=s+'.pdf'
       while os.path.isfile(newName):
          newName=s+'.pdf'
          n+=1
       print(filename,"---->",newName)
       try:
         os.renames(filename,newName)
         #os.remove(filename[0:l]+'.txt')
       except Exception:
         print ('Error cant rename:',filename)