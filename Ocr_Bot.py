#V2 find answer and failList, search ans for failList
import os
import csv
import smtplib
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter
ans=''
failList=[]
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
         s1=text.find('*',s2+1)
         s2=text.find('*',s1+1)
         if(s1==-1)or(s2==-1):
           break
       Inv=text[s1+1:s2].split()
       s=''
       for item in Inv:
           s=s+item
           ans=s[0:3]
       if len(s)>6:
         print ('ERROR: cant find INV#:',filename)
         failList.append(filename)
         continue
       
       newName="Shipping_PT# "+s+'.pdf'
       while os.path.isfile(newName):
          newName="Shipping_PT# "+s+'-'+str(n)+'.pdf'
          n+=1
       print(filename,"---->",newName)
       try:
         os.renames(filename,newName)
         #os.remove(filename[0:l]+'.txt')
       except Exception:
         print ('Error cant rename:',filename)
       f.close()
print ('Ans=',ans)
print ('Starting fix......')
for filename in failList:
       
       l=len(filename) - 4
       try:
         f=open(filename[0:l]+'.txt','r')
       #print (filename[0:l]+'.txt')
       except Exception:
         print ("No txt file:",filename)
         continue
       text=f.read()
       s=''
       s1=text.find(ans)
       if s1!=-1:
         #print(filename,s1)
         s=text[s1:s1+5]
       if s.isdigit():
          newName="Shipping_PT# "+s+'.pdf'
       else:
          continue
       while os.path.isfile(newName):
          newName="Shipping_PT# "+s+'-'+str(n)+'.pdf'
          n+=1
       print(filename,"-fx->",newName)
       try:
         os.renames(filename,newName)
         #os.remove(filename[0:l]+'.txt')
       except Exception:
         print ('Error cant rename:',filename)
       f.close()
      