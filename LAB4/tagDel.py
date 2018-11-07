import csv
import smtplib
import sys


f= open('inp.csv',"r")  
look=csv.reader(f)
styleLib={}


def TagDel(dec):
   s0=0
   s1=0
   while dec.find('<',s1)!=0:
      s0=dec.find('<',s1)
      s1=dec.find('>',s0)
      if s0==-1 or s1==-1:
         print ('break')
         break
      print ('del',s0,s1,dec[s0:s1+1])
      dec=dec.replace(dec[s0:s1+1],'')
      s0=0
      s1=0
   return dec

fo= open('output-winaUPC.csv',"w",newline='') 
fieldnames=['Description']	
writer=csv.DictWriter(fo,fieldnames=fieldnames)
for item in look:
    if len(item)==0:
       writer.writerow({'Description':' '})
       continue
    dec=item[0]
    #print (dec)
    dec=TagDel(dec)
    #print (dec)
    writer.writerow({'Description':dec})