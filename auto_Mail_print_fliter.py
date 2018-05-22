import csv
import smtplib
import sys
#!/usr/bin/python
# -*- coding: UTF-8 -*-

mode = input("Search for :") 
n=0;
name = ''

f= open('input.csv',"r")  
look=csv.reader(f)
result = {}
result2={}
for item in look:
    mail_check=(item[0])
    inv=(item[2])
    if(mail_check==mode):
       name = name + 'invoiceno ='+inv+' or '
       n=n+1
	   
	   
print (name)
print ("Total "+mode+": ",n)	   
f.close()
