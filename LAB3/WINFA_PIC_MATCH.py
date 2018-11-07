#!/usr/bin/python
#v1.0 check for ATS and Alert
import csv
import smtplib
import sys
import os
#!/usr/bin/python
# -*- coding: UTF-8 -*-
outputList=['Quantity']
#mode = input("Search for :") 
count=0

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

def searchIMG(style , color):
    code=style[0]
    flag=0
    if code !='0' and code!='D' and code!='H' and code!='G' and code!='G' and code!='P'and code!='S':
       return 
    for filename in os.listdir("Z:/Style Library/"+code+" Styles/Watermark"):
        fcolor=filename[filename.find(' ')+1:]
        if '_'in color:
           fcolor=fcolor[0:color.find('_')]
        if style.replace('W','') in filename and colorMatch(color,fcolor)==1:
           print(style,color,filename)
           flag=1
        else:
           co=''
           #print(style,color,'<---------------No file')
    if flag==0:
       print(style,color,'<-------------------------------------------------------No file')
f= open('ATSWIP.csv',"r")  
look=csv.reader(f)
ATS={}
ATS0=[]
ATS_Style={}
negativeList={}
sf=0
for item in look:
    size=[]
    qty=[]
    style=(item[0])
    if style == 'code':
       continue
    color=(item[1])
    cate=item[6]
    des=item[2]
    size.append(item[21])
    size.append(item[22])
    size.append(item[23])
    size.append(item[24])
    size.append(item[25])
    size.append(item[26])
    size.append(item[27])
    size.append(item[28])
    size.append(item[29])
    size.append(item[30])
    size.append(item[31])
    size.append(item[32])
    

    qty.append(item[38])	
    qty.append(item[39])
    qty.append(item[40])
    qty.append(item[41])
    qty.append(item[42])
    qty.append(item[43])
    qty.append(item[44])
    qty.append(item[45])
    qty.append(item[46])
    qty.append(item[47])
    qty.append(item[48])
    qty.append(item[49])


    #print (style,color,size)
    for i in range(12):
      #print (i)
      if size[i]!='':
        key = style+"-"+color+"-"+size[i]
        Qty = qty[i]
        #print("ATS: "+key+" <= "+Qty)
        if int(Qty)<0:
           negativeList[key]=Qty
        Alist=[]
        Alist.append(style)
        Alist.append(color)
        Alist.append(size[i])
        Alist.append(qty[i])
        Alist.append(cate)
        ATS0.append(Alist)
        ATS[key]=Qty
        ATS_Style[style+"-"+color]='Y'
        count+=1
      else:
        continue
	   

for list in ATS0:
   style=list[0]
   color=list[1]
   searchIMG(style,color)
   #print (style, color)



f.close()
input(" exit")