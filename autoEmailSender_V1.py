import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
#!/usr/bin/python
# -*- coding: UTF-8 -*-
n=0
e=0

email_user = 'info@giovanna-apparel.com'
email_password = '20171006Newpw'
body = 'Dear customer,\n\nPlease see attached invoice for your reference. \n\nWe appreciate your business!\n\nGiovanna Apparel Corp. \n214 West 39th Street, Suite# 607\nNew York, NY 10018\nTel: 212-382-2500\nFax: 212-382-2553'
# 定义函数
def sendEmail( filename, email_send ):
    	
	subject = filename[0:(len(filename)-4)]
	msg = MIMEMultipart()
	msg['From'] = email_user
	msg['To'] = email_send
	msg['Subject'] = subject


	msg.attach(MIMEText(body,'plain'))

	try:
		attachment  =open('./INV/'+filename,'rb')


		part = MIMEBase('application','octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition',"attachment; filename= "+filename)

		msg.attach(part)
		text = msg.as_string()
	except Exception:
		print ("Error: No attachement.")
	
	
	try:
		server = smtplib.SMTP('smtp.gmail.com',587)
		server.starttls()
		server.login(email_user,email_password)
		server.sendmail(email_user,email_send,text)
		print ("%s Email send successfully!" % (filename))
	except Exception:
		print ("Error: %s Email send failed!" % (filename))



	server.quit()
	return
 



f= open('input.csv',"r")  
look=csv.reader(f)

for item in look:
    filename=(item[2])
    email=(item[14])
    result=(item[1])
    if (filename=='N/A')or(filename=='')or(result=='E'):
       continue
    if (email=='0'):
       e=e+1
       continue
    sendEmail(filename+'.pdf',email)	
    #print (n+1,' sending....'+filename+'.pdf'+"----->"+email)
    n=n+1
	
print ("Emails Sent: ", n," No Email Address: ",e," Total Processed: ",n+e)
f.close()
