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
outList=[]
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
def findSizes(div):
    sizes='N/A'
    if div=='M3':
       sizes='6-16'
    elif div=='M1':
       sizes='10-18'
    elif div=='M10':
       sizes='10-20'
    elif div=='M4':
       sizes='12-18'
    elif div=='M9':
       sizes='12-20'
    elif div=='M6':
       sizes='14-18'
    elif div=='M6':
       sizes='14-18'
    elif div=='W11':
       sizes='14W-22W'
    elif div=='W2':
       sizes='14W-24W'
    elif div=='W3':
       sizes='14W-26W'
    elif div=='W13':
       sizes='14W-28W'
    elif div=='W12':
       sizes='14W-30W'
    elif div=='W15':
       sizes='14W-32W'
    elif div=='W8':
       sizes='16W-22W'
    elif div=='W6':
       sizes='16W-24W'
    elif div=='W1':
       sizes='16W-26W'
    elif div=='W14':
       sizes='18W-24W'
    elif div=='W16':
       sizes='28W-36W'
    elif div=='M7':
       sizes='6-18'
    elif div=='M8':
       sizes='8-16'
    elif div=='M5':
       sizes='8-18'
    elif div=='M-2X':
       sizes='M,L,XL,1X,2X'
    elif div=='M-3X':
       sizes='M,L,XL,1X,2X,3X'
    elif div=='M-1X':
       sizes='M-1X'
    elif div=='SKRT':
       sizes='M-1X,2X-4X'
    elif div=='ONE':
       sizes='OS'
    elif div=='DRES':
       sizes='XL-2X'
    elif div=='S-2X':
       sizes='S-2X'
    elif div=='S-XL':
       sizes='S-XL'
    return sizes

def searchIMG(style , color, div, writer):
    style=style.replace('A','')
    style=style.replace('/','-')
    color= color.replace(' ','')
    if '#' in color:
       color=color[0:color.find('#')]
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
           if style+color not in outList:
              outList.append(style+color)
              writer.writerow({'style':'#'+style,'color':color, 'sizes':'#'+findSizes(div),'image file':filename })
           flag=1
           break
        else:
           co=''
           #print(style,color,'<---------------No file')
    if flag==0:
       print(style,color,'<-------------------------------------------------------No file')
       if style+color not in outList:
          outList.append(style+color)
          writer.writerow({'style':'#'+style,'color':color, 'sizes':'#'+findSizes(div),'image file':'N/A' })
f= open('Z:/Zoe/ATS/ATSWIP.csv',"r")  
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
    division=item[6]
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
        Alist.append(division)
        ATS0.append(Alist)
        ATS[key]=Qty
        ATS_Style[style+"-"+color]='Y'
        count+=1
      else:
        continue
	   
fo= open('output.csv',"w",newline='')
fieldnames=['style','color','sizes','image file']
writer=csv.DictWriter(fo,fieldnames=fieldnames)
writer.writeheader()
for list in ATS0:
   style=list[0]
   color=list[1]
   div=list[5]
   searchIMG(style,color,div, writer)
   #print (style, color)



f.close()
input(" exit")