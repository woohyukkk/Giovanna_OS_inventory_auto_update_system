import csv
import smtplib
import sys
from datetime import datetime
from datetime import timedelta
import pandas as pd
today=datetime.now().strftime('%Y%m%d')
dateTest=datetime.now()-timedelta(days=5)
dateTest=dateTest.strftime('%Y%m%d')
dateTest=str(dateTest)
#!/usr/bin/python
# -*- coding: UTF-8 -*-
emails={}
emails2={}
Mlist={}
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

def mailCheck():
  s=''
  rtn=[]
  n=0
  f= open('./Invoice Reports.csv',"r")  
  look=csv.reader(f)
  for item in look:
    code=item[4]
    d=item[0]
    cus=item[2]
    t=dateTest
    if d < t :
       continue
    if code=='M':
       if cus not in Mlist:
         newlist=[]
         newlist.append(item[1])
         Mlist[cus]=newlist
       else:
         Mlist[cus].append(item[1])
       s=s+'invoiceno ='+item[1]+' or '
       n+=1
  rtn.append(n)
  rtn.append(s)
  return rtn

def mailConfirm(Mlist): #pandas used
  n=0
  f= pd.read_csv('./Invoice Reports.csv')  
  for code,list in Mlist.items():
    for inv in list:
      n+=1
      f.loc[f["Inv#"]==inv,"Result"]='M'
      f.to_csv('./Invoice Reports.csv', index=False)
      print ('Inv#',inv,"Result=>",'M')
  print ('Total',n,'processed.')
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
if mode=='M':
       list=mailCheck()
       n=list[0]
       name=list[1]
for item in look:
    cusCode=item[2]
    CODcheck=(item[12])
    if CODcheck[0:2]=='COD':
      print ( cusCode,"need COD")
      continue
    if mode=='E':
       if cusCode in emails:
          if emails[cusCode][0]=='N' or emails[cusCode][0]=='M'or emails[cusCode][0]=='F':
            continue
       if cusCode in emails2:
         if (emails2[cusCode]!=''):
           inv=(item[0])
           name = name + 'invoiceno ='+inv+' or '
           n=n+1           
	   
	   
print (name)
for code,list in Mlist.items():
  print(code,list)

print ("Total "+mode+": ",n)
f.close()
inp=''
while (inp!='N' or input!='n')and(mode=='M'):
   inp=input("Confirme Mail(Y/N): ")
   if inp=='Y' or inp=='y':
     print ('Mails confirming.....')
     try:
      mailConfirm(Mlist)
     except Exception:
      print ('Mail confimation failed, Pls close save file and try again...')
      continue
     break
   else:
     print('Exiting mail confirmation')
     break
   print ('All mails mailed')
input('any to exit')


