import csv
import smtplib
import sys
#!/usr/bin/python
# -*- coding: UTF-8 -*-
emails={}
emails2={}
def loadEmails():
   f= open('cusAction.csv',"r")  
   look=csv.reader(f)

   for item in look:
      if item[0]=='Customer Code':
        continue
      action=item[1]
      email=(item[2])
      customerCode=(item[0])
      print ("Code: "+customerCode+" action: "+action+" email: "+email)
      #cus=Customer(customerName,customerCode,email)
      emails[customerCode]=[action,email]
      #cus.displayCustomer()

	
      #print (emails)
   f.close()
   return
def loadEmails2():
   f= open('./Completed/customer_emails.csv',"r")  
   look=csv.reader(f)

   for item in look:
      customerName=(item[73])
      email=(item[59])
      customerCode=(item[72])
      #print ("Customer: "+customerName+" Code: "+customerCode+" email: "+email)
      #cus=Customer(customerName,customerCode,email)
      emails2[customerCode]=email
      #cus.displayCustomer()

	
      #print (emails)
   f.close()
   return
loadEmails2()  
loadEmails()
mode = input("Search for :") 
n=0;
name = ''

f= open('input.csv',"r")  
look=csv.reader(f)
result = {}
result2= {}

mail_check='0'
for item in look:
    cusCode=item[2]
    CODcheck=(item[12])
    if CODcheck[0:2]=='COD':
      print ( cusCode,"need COD")
      continue
    if mode=='M':
      try:
         mail_check=emails[cusCode][0]
      except Exception:
         print ("ERROR:",cusCode,"cant find")
         continue
      inv=(item[0])
      if(mail_check==mode):
         print (cusCode,"need",mode)
         name = name + 'invoiceno ='+inv+' or '
         if cusCode not in result:
          list=[]
          list.append(inv)
          result[cusCode]=list
         else:
          list=result[cusCode]
          list.append(inv)
          result[cusCode]=list
         n=n+1
    elif mode=='E':
       if cusCode in emails:
          if emails[cusCode][0]=='N' or emails[cusCode][0]=='M':
            continue
       if cusCode in emails2:
         if (emails2[cusCode]!=''):
           inv=(item[0])
           name = name + 'invoiceno ='+inv+' or '
           n=n+1           
	   
	   
print (name)
for code,list in result.items():
  print(code,list)

print ("Total "+mode+": ",n)	   
f.close()
