import os
import csv
import smtplib
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter
report=[]


def readCSV():
  yCount=0
  nCount=0
  f= open('all hats ATS.csv',"r")  
  look=csv.reader(f)
  print ('#############Start')
  for item in look:
    style=item[0]
    color=item[1]
    color=color.upper()
    color=color.replace('.','')
    #print ('read',style,color)
    s=0
    f=0
    for filename in os.listdir("./2018 Hat Clean Pics"):
       #print('Scaning....',filename)
       filename=filename.upper()
       filename=filename.replace('-','/')
       existC=0
       
       if '.JPG' in filename:
         #print (filename,'jpg found')
         if filename.find(style)!=-1:
           #print (style,'found')
           #print (color,filename)
           color=str(color)
           for item in color:
             #print('item:',item,color)
             
             s=filename.find(item)

             if s==-1:
               #print ('b2')
               break
             else:
                existC+=1
                filename=filename[s+1:]
           if existC==len(color):
              yCount+=1
              print (style,color,'found')
              list=[]
              list.append(style)
              list.append(color)
              list.append('Yes')
              report.append(list)
              f=1
              #print ('b3')
              break
    if f!=1:
              list=[]
              list.append(style)
              list.append(color)
              list.append('NO')
              report.append(list)
              nCount+=1
              print ('@',style,color,'not found!')
  print ('Total found:',yCount,'Not found:',nCount)
readCSV()

#print (report)
fo= open('Hat Report.csv',"w",newline='') 
fieldnames=['Style','Color','Found']	
writer=csv.DictWriter(fo,fieldnames=fieldnames)
writer.writeheader()
for list in report:

   writer.writerow({'Style':list[0],'Color':list[1],'Found':list[2]})
fo.close()
input('Enter to quit')
