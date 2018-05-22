import os
import csv
import smtplib
import sys

f= open('../input.csv',"r")  
look=csv.reader(f)
n=0
e=0
for item in look:
    mail_check=(item[0])
    inv=(item[2])
    name=(item[11])
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


