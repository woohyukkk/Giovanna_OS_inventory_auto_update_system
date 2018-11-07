#！C:\Users\youngwoo\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Python 3.6
#V2.1 find answer and failList, search ans for failList
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
       if pt!=-1 and text[pt+4:pt+9].isdigit():
         newName=text[pt+4:pt+9]
         try:
           print ('Label found') #FOR LABEL
           os.rename(filename,"Shipping_PT# "+newName+'-2.pdf')
           addlabel()
           continue
         except Exception:
           print('cant rename',filename, sys.exc_info()[0])
           continue
       elif pt==-1 and text.find('*')==-1:
         print ("Error:",filename,"failed")
         failList.append(filename)
         continue
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
          if (item.isdigit()):
             s=s+item
       print(s)
       if len(s)>6 or len(s)<5:
         print (len(s),'ERROR: cant find INV#:',filename)
         failList.append(filename)
         continue

       if (s.isdigit()==True):
          ans=s[0:3]
       if s!=''and s.isdigit():
          newName="Shipping_PT# "+s+'.pdf'
       else:
          newName=filename
          failList.append(filename)
          continue
       while os.path.isfile(newName):
          print (newName,'already exist')
          newName="Shipping_PT# "+s+'-'+str(n)+'.pdf'
          n+=1
       print(filename,"---->",newName)
       #try:
       os.renames(filename,newName)
         #os.remove(filename[0:l]+'.txt')
       #except Exception:
         #print ('Error cant rename:',filename)
       f.close()
print ('Ans=',ans)
ans=str(ans)
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
       spaceN=0
       while text.find(' ')!=-1:
         text=text.replace(' ','')

       s=''
       s1=text.find(ans)
       if s1==-1:
          s1=s1=text.find(str(int(ans)+1))
          if s1==-1:
             s1=text.find(str(int(ans)-1))
       if s1!=-1:
         #print(filename,s1)
         s=text[s1:s1+5]
       if s.isdigit():
          newName="Shipping_PT# "+s+'.pdf'
       else:
          print (filename,"fix failed.")
          continue
       n=2
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

input('Press any key to exit')