#V4 auto pick customer actions and expert reports version with backup reports function
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import sys
import os
#!/usr/bin/python
# -*- coding: UTF-8 -*-
n=0
e=0
####################################login in eamil
email_user = 'info@giovanna-apparel.com'
email_password = '***********'
body = 'Dear customer,\n\nPlease see attached invoice for your reference. \n\nWe appreciate your business!\n\nGiovanna Apparel Corp. \n214 West 39th Street, Suite# 607\nNew York, NY 10018\nTel: 212-382-2500\nFax: 212-382-2553'
# 定义函数
emails={}
emails2={}
reports={}
def loadEmails():#############################check cusAction -> emails{}
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

def loadEmails2():######################check emails-> emails2{}
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

def sendEmail( filename, email_send ):########### send emails with attachment
    s=0
    subject = filename[0:(len(filename)-4)]
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject


    msg.attach(MIMEText(body,'plain'))
    try:
        attachment=open('./INV/'+filename,'rb')
        part = MIMEBase('application','octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',"attachment; filename= "+filename)

        msg.attach(part)
        text = msg.as_string()
    except Exception:
        print ("Error: No attachement.")
        s=-1


    try:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email_user,email_password)
        server.sendmail(email_user,email_send,text)
        s=1
        print ("%s Email send successfully!" % (filename))
    except Exception:
        print ("Error: %s Email send failed!" % (filename))
        S=-1



    server.quit()
    return s
 

loadEmails2()
loadEmails()
f= open('input.csv',"r")  
look=csv.reader(f)
f1=0
for item in look:
    if f1==0: 
      f1=1
      continue
    processCode=''
    invoiceNO=(item[0])
    customerName=(item[16])
    customerCode=(item[2])
    CODcheck=(item[12])
    reports[invoiceNO]=[customerCode,customerName,'0','0'] # code name, process, done
    if (customerCode=='OVE841') or (customerCode=='JCP750'):    ########Skip jcp OS
       reports[invoiceNO]=[customerCode,customerName,'N','N']
       print ('JCP/OS Inv Skipped.')
       #reports[invoiceNO]=[customerCode,customerName,'NE','NE']
       continue
    if customerCode in emails:########### check M F S
       if emails[customerCode][0]=='M':
          reports[invoiceNO][2]='M'
          continue
       elif emails[customerCode][0]=='F':
          reports[invoiceNO][2]='F'
          continue
       elif emails[customerCode][0]=='S':
          reports[invoiceNO][2]='S'
          continue
    if 'COD' in CODcheck:##############  Check COD
       reports[invoiceNO]=[customerCode,customerName,'COD','0']
       print ('COD INV skipped.')
       continue
    filename=("Inv# "+invoiceNO+" "+customerName+".pdf")

    try:#################### Check email address for cusCode in emails{}
        email=emails2[customerCode]
        #processCode=emails[customerCode][0]
    except Exception:
        print ("ERROR: Inv# "+invoiceNO+" Can't find customerCode["+ customerCode +"] in emails.")
        continue
  
    if (filename=='N/A')or(filename==''):
       continue
    if (email==''):
       print (customerCode,'no email address found!')
       e=e+1
       reports[invoiceNO]=[customerCode,customerName,'NE','NE']
       continue
    s=sendEmail(filename,email)
    #s=1	
    print (n+1,' sending....'+filename+"----->"+email)
    if s==1:
      n=n+1
      reports[invoiceNO]=[customerCode,customerName,'E','E']
    elif s==-1:
      reports[invoiceNO]=[customerCode,customerName,'N','N']

#print (reports)
date=datetime.now().strftime('%Y%m%d')
try:
   fo= open('Invoice Reports.csv',"a",newline='')
except Exception:
   fo= open('Backup_Reports# '+date+'.csv',"a",newline='')
   print ('Invoice Reports.csv open failed.......saving to back up Report: '+'Backup_Reports# '+date+'.csv')
fieldnames=['Date','Inv#','CusCode','CusName','Process Code','Done']
writer=csv.DictWriter(fo,fieldnames=fieldnames)
writer.writeheader()

for inv,info in reports.items():
    writer.writerow({'Date':date,'Inv#':inv, 'CusCode':info[0],'CusName':info[1],'Process Code':info[2],'Done':info[3] })
    print ("Report: ",inv,info[0],info[2],info[3],info[1])
os.system('copy Invoice Reports.csv Invoice Reports-backup.csv')
print ('Backup successed.@Reports-backup.csv')
print ("Emails Sent: ", n," No Email Address: ",e," Total Processed: ",n+e)
f.close()
fo.close()
input("Enter to exit")
