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
#   OS   SELECT qty1 FROM syql_ats WHERE code=0650 and color='BLK';
    cursor=cnx.cursor()
    qtyN=''
    try:
       if size == '8':
           qtyN='qty1'
           sql = "SELECT qty1 FROM syql_ats WHERE code=%s and color =%s "
    
       
       data=(style,color)
       cursor.execute(sql, (style,color))
       for qty1 in cursor:
           print ( "qty value is ", qty1 )
    except mysql.connector.Error as e:
       print( 'query error!{}'.format(e) )	
    return qty1[0]

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

style='0650'
color='BLK'
size='8'
a=searchDB(style,color,size)
print (a[0])
