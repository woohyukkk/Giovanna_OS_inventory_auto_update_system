import os
import csv
import smtplib
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter
report=[]

def colorMatch(color1,color2):# color1 for ATS color(short)
    existC=0
    color1=color1.upper()
    color2=color2.upper()
    color2=color2.replace('-','/')
    color1=color1.replace('.','')
    color2=color2.replace('.','')
    color1=color1.replace(' ','')
    color2=color2.replace(' ','')
    for item in color1:
       #print('item:',item,color)
       s=color2.find(item)
       if s==-1:
          #print ('b2')
          return 0
       else:
          existC+=1
          color2=color2[s+1:]
       if existC==len(color1):
              return 1
c1=''

while c1!='exit':
 c1=input("color1 input:")
 c2=input("color2 input:")
 s=colorMatch(c1,c2)
 if s==1:
  print ('Match!')
 else:
  print ('Not Match!')
