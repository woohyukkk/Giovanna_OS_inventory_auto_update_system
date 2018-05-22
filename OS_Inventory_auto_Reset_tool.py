#Only work for Python 2.7, use cmd "py -2 xxxx.py" to run
#version 0.01 Connect ATS_db and search for 0 styles returns
import os
import csv
import smtplib
import sys
import mysql.connector
from mysql.connector import errorcode

def searchDB(style,color,size):
# size1 size2 size3 size4 size5 size6 size7 size8 size9 size10 size11
#   8     10   12    14    16    18    20
#              14W   16W   18W   20W   22W   24W   26W   28W    30W
#          M     L    XL    1X    2X    3X  
#   OS  
    qtyN=''
    if size = '8':
       qtyN='qty1'
    sql = "SELECT %s FROM syql_ats WHERE code=%s and color =%s "
    data=(qtyN,style,color)
    cursor.execute(sql, data)
    return



##############################Conncet DB###############################
config = {
  'user': 'Chen He',
  'password': '123456',
  'host': 'localhost',
  'database': 'winfa_ats',
  'raise_on_warnings': True,
}
try:
   cnx = mysql.connector.connect(**config)
   print ('DataBase: '+config['database']+' connected.')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

  #cnx.close()


##############################Conncet DB###############################

##############################Search csv###############################
f= open('0 Styles_Reset.csv',"r")  
look=csv.reader(f)
style=''
color=''
size=''
first=1
n1=0;
for item in look:
    if first == 1:
       first=0
       continue
    SKU=(item[1])
    onhand=(item[2])
    onhand=0
    SKU.upper()
    SKU=SKU.split('-')
    if(len(SKU)==1):
       SKU=SKU[0].split(' ')
	   
    #print (SKU)
    style=SKU[0]
    if len(SKU)>1:
       color=SKU[1]
    else:
       color='N/A'
    if len(SKU)>2: 
       size =SKU[2]
    else:
       size='N/A'
    print ("CSV: Style:"+style+"     Color:"+color+"     Size:"+size)
    searchDB(style,color,size)
################################################################################    


