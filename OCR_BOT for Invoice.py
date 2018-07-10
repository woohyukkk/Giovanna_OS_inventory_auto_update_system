#V3 Check all files and OCR .pdf with .txt files, combo -2 files if any, add customer name from input.csv
import os
import csv
import smtplib
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter
e=0
flag=0
for filename in os.listdir("."):
     if 'pdf' in filename:
       l=len(filename) - 4
       try:
         f=open(filename[0:l]+'.txt','r',newline='')
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
          s4=s3+1

          while text[s4].isdigit()==False:
              s4+=1
          #print ("text[4]:",text[s4])
          s=text[s4:s4+5]
          #print(s)
       if len(s)>6:
         e+=1
         print ('ERROR: cant find INV#:',filename)
         continue
       newName=s+'.pdf'
       while os.path.isfile(newName):
          newName=s+'-'+str(n)+'.pdf'
          flag=1
          n+=1
       print(filename,"---->",newName)
       try:

         os.renames(filename,newName)

       except Exception:
         e+=1
         print ('Error cant rename:',filename)
       f.close()
       try:
         os.remove(filename[0:l]+'.txt')
         print ()
       except Exception:
         print ("ERROR: Can't remove file:",filename[0:l]+'.txt')
		 
if flag==1:
  print ("-2 files dectected. Combo pdf function start......")
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
print ('Adding customer name from input.csv')

f= open('../input.csv',"r")  
look=csv.reader(f)
n=0
e=0
for item in look:
    if item[0]=='invoiceno':
      continue
    inv=(item[0])
    name=(item[16])
    file=''
    for filename in os.listdir("."):
        
        if inv==filename[0:5]:
           file='Inv# '+inv+" "+name
           print ("renaming...."+filename+"---->"+file+".pdf")
           try:
               os.rename(filename,file+".pdf")
               n=n+1
           except Exception:
               print ("ERROR "+filename)
               e=e+1
           break		   
           
print ("Success: ",n," Error: ",e)
input('Press any key to exit')


