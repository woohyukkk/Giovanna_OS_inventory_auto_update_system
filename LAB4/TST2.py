#IN: 'ATS.csv'

import csv
import smtplib
import sys
#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

def colorMatch(color1,color2):# color1 for ATS color(short)
    existC=0
    color1=color1.upper()
    color2=color2.upper()
    color2=color2.replace('-','/')
    color1=color1.replace('.','')
    color2=color2.replace('.','')
    color1=color1.replace(' ','')
    color2=color2.replace(' ','')
    c1=color1.count('/')
    c2=color2.count('/')
    if c1!=c2:
       return 0
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

def output(filename,headArray,styleLib):
    fo= open(filename,"w",newline='') 
    fieldnames=headArray	
    writer=csv.DictWriter(fo,fieldnames=fieldnames)
    writer.writerow({'IN':'IN','Supplier Sku':jcpCode,'YES':'Yes','Quantity':v,'Decription':dec,'SKU':SKU,'JCPENNEY':'JCPENNEY' })
    for item in styleLib.items():
       style=item[0]
       (sku,upc),=item[1]['sku'].items()
       title = item[1]['title']
       dec = item[1]['dec']
    print (style,sku,upc,title)

def ATS_loader():
  count=0
  f= open('Z:/Zoe/ATS/ATS.csv',"r")  
  look=csv.reader(f)
  ATS={}
  ATS0=[]
  negativeList={}
  sf=0
  for item in look:
    size=[]
    qty=[]
    style=(item[0])
    for n in range(70):
       if item[n]=='size1':
          sizeN=n
       if item[n]=='ats1':
          atsN=n

    if style == 'code':
       continue
    color=(item[1])
    cate=item[6]
    des=item[2]
    size.append(item[sizeN])
    size.append(item[sizeN+1])
    size.append(item[sizeN+2])
    size.append(item[sizeN+3])
    size.append(item[sizeN+4])
    size.append(item[sizeN+5])
    size.append(item[sizeN+6])
    size.append(item[sizeN+7])
    size.append(item[sizeN+8])
    size.append(item[sizeN+9])
    size.append(item[sizeN+10])
    size.append(item[sizeN+11])

    qty.append(item[atsN])
    qty.append(item[atsN+1])
    qty.append(item[atsN+2])
    qty.append(item[atsN+3])
    qty.append(item[atsN+4])
    qty.append(item[atsN+5])
    qty.append(item[atsN+6])
    qty.append(item[atsN+7])
    qty.append(item[atsN+8])
    qty.append(item[atsN+9])
    qty.append(item[atsN+10])
    qty.append(item[atsN+11])


    #print (style,color,size)
    for i in range(12):
      #print (i)
      if size[i]!='':
        key = style+"-"+color+"-"+str(size[i])
        Qty = qty[i]
        #print (Qty,Qty.find('.'),Qty[0:Qty.find('.')])
        if Qty!='0':
           Qty=Qty[0:Qty.find('.')]
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
        count+=1
      else:
        continue
  f.close()
  return ATS0

ATS0=ATS_loader()
UPClib={}

f= open('output.csv',"r")  
look=csv.reader(f)
styleLib={}
for item in look:
    if item[0]=='Style':
      continue
    style=item[0]
    sku  =item[1]
    upc=item[2]
    title=item[3]
    dec=item[4]
    size=item[5]
    color=item[6]
    style=style.replace('#','')
    list=[]
    list.append(style)
    list.append(sku)
    list.append(upc)
    list.append(title)
    list.append(dec)
    list.append(size)
    list.append(color)
    styleLib[sku]=list
    #print(sku,upc)

fo= open('output-winaUPC.csv',"w",newline='') 
fieldnames=['Style','Supplier SKU','UPC','Title','Description','Size','Color','URL']	
writer=csv.DictWriter(fo,fieldnames=fieldnames)
writer.writeheader()
checklist=set()
for item in ATS0:
    flag=0
    style0=item[0]
    color0=item[1]
    size0 =item[2]
    style0=style0.replace('W','')
    title0=''
    dec0=''
    for sku, list in styleLib.items():
       s0=sku.find('-',0)
       s1=sku.find('-',s0+1)
       style = sku[0:s0]
       style=style.replace('W','')
       color = sku[s0+1:s1]
       size  = sku[s1+1:]
       if style0==style and size==size0 and (colorMatch(color0,color)==1 or colorMatch(color,color0)==1 ):
         print (list[1],list[2],list[3])
         style=list[0]
         sku = list[1]
         upc = list[2]
         title = list[3]
         dec = list[4]
         size = list[5]
         color = list[6]
         if style0[0]=='0':
           style0='#'+style0
         writer.writerow({'Style':style0, 'Supplier SKU':sku,'UPC':upc,'Title':title,'Description':TagDel(dec0),'Size':size,'Color':color})
         flag=1
         break
       elif style0==style:
         style=list[0]
         sku = list[1]
         upc = list[2]
         title = list[3]
         dec = list[4]
         size = list[5]
         color = list[6]
         dec0=dec
         title0=title

    if flag==0:
       style1=style0
       print ('Not found: ',style0,color0,size0,'<---------------------------------')
       if 'W' in size0:
          style1=style0+'W'
       if style0[0]=='0':
          style0='#'+style0
       writer.writerow({'Style':style0, 'Supplier SKU':style1+'-'+color0+'-'+size0,'UPC':'','Title':title0,'Description': TagDel(dec0),'Size':size0,'Color':color0})



input(" exit")