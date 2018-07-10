#Auto PTs generator
#Combo all PTs and labels (.pdf) to one pdf file
#label should end with '-2'
#Check when the new PT processing, warning if exist in the record,So avoid to send PT twice. 
import os
import csv
import smtplib
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter
from datetime import datetime

def check(n): #The function which check the number n, see if it in the record file
   f= open('PT Reports.csv',"r",newline='')
   look = csv.reader(f)
   size=os.path.getsize('PT Reports.csv')
   for item in look:
      if size==0: # return 0 if file is empty
        print ('File empty')
        return 0
      print (item)
      if len(item)<2:
         continue
      if item[1]=='PT#':# skip header
         continue
      if n==item[1]: # warning if n exist in record
         print ('Warning! PT#',n,'already in the record')
         f.close()
         return -1
   f.close()
   return 1




print ('#Strating PT combo and recording system...................')
output = PdfFileWriter()
list=[]
PTN=''
total=0
print ("#Checking '.pdf' files......................")
for filename in os.listdir("."):# scan all files and only pick the right PT files
     if '.pdf' in filename:
       l=len(filename) - 4
       name=filename[0:l]
       s1=name.find('#')
       s2=name.find(',')
       s3=name.find('-')
       if s1!=-1 and s2==-1:
         number=name[s1+2:len(name)]
         if total==0:
           r=check(number)
           if r==-1:
              #print ('PT#',number,'skipped')
              continue
           if s3==-1:
             PTN=PTN+' '+number
             list.append(number)
             total+=1
           else:
             print ('PT# '+number[0:len(number)-2]+' Label['+number+'] added')
         else:
           r=check(number)
           if r==-1:
              #print ('PT#',number,'skipped')
              continue
           if s3==-1:
             PTN=PTN+', '+number
             list.append(number)
             total+=1
           else:
             print (' Label['+number+'] added')
       else:
         print ('cant find # in filename:',filename)
         continue
       f1=open(filename, "rb")
       input1= PdfFileReader(f1)
       page=input1.getNumPages()

       print ( 'Name:',name,'NO.:',number,'Page:',page)
       for i in range (page):
          output.addPage(input1.getPage(i))
print ('Total processed:',total,'Writing '+'PT# '+PTN+".pdf")
if total>0:
 newFile='PT# '+PTN+".pdf"
 outputStream = open('PT# '+PTN+".pdf", "wb")
 output.write(outputStream)
 outputStream.close()
else:
 print ("No item comboed")

################################report###############################
print ('#Recording..................................\n')
date=datetime.now().strftime('%Y%m%d')
try:
   fo= open('PT Reports.csv',"a",newline='')
except Exception:
   fo= open('PT Backup_Reports# '+date+'.csv',"a",newline='')
   print ('Reports.csv open failed.......saving to back up Report: '+'Backup_Reports# '+date+'.csv')
fieldnames=['Date','PT#']
writer=csv.DictWriter(fo,fieldnames=fieldnames)

writer.writeheader()


for number in list:
    writer.writerow({'Date':date,'PT#':number})
    print ("Report: ",number)

fo.close()
input("Press any key to exit")