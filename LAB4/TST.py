#input: 'UPCdata.csv', 'dataOS_2.csv'
#match
#output: 'output.csv'-> SKU-UPClib.csv

import csv
import smtplib
import sys
#!/usr/bin/python
# -*- coding: UTF-8 -*-
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
  f= open('ATS.csv',"r")  
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

def UPC_loader():
    f= open('UPCdata.csv',"r")  
    look=csv.reader(f)
    UPClib={}
    for item in look:
       if item[1]=='UPC':
         continue
       sku=item[3]
       brand=item[2]
       upc12=item[1]
       upc14=item[0]
       s0=sku.find('-',0)
       s1=sku.find('-',s0+1)
       style = sku[0:s0]
       color = sku[s0+1:s1]
       size  = sku[s1+1:]
       UPCinfo={}
       UPCinfo['sku']=sku.upper()
       UPCinfo['brand']=brand
       UPCinfo['upc12']=upc12
       UPCinfo['upc14']=upc14
       UPCinfo['color']=color
       UPCinfo['size']=size
       UPCinfo['style']=style.replace('W','')
       UPClib[sku]=UPCinfo
       #print (sku,upc12)
    return UPClib
	


UPClib={}
UPClib=UPC_loader()
f= open('dataOS.csv',"r")  
look=csv.reader(f)
styleLib={}
for item in look:
    sku=item[2].upper()
    title=item[3]
    dec= item[5]
    style='N/A'
    color='N/A'
    size='0'
    upc='0'
    styleInfo={}
    #print (sku)
    if '-' in sku:
       s0=sku.find('-',0)
       s1=sku.find('-',s0+1)
       style = sku[0:s0]
       style=style.replace('W','')
       color = sku[s0+1:s1]
       size  = sku[s1+1:]
       if sku in UPClib:
          upc=UPClib[sku]['upc12']
          print (sku,upc)
       else:
          #print (sku,upc,'<--------------------------------------------------------------')
          for UPCsku,info in UPClib.items():
            if style == info['style'] and size==info['size']:
              skuColor=info['color']
              if colorMatch(skuColor,color)==1 or colorMatch(color,skuColor)==1:
                 upc=UPClib[UPCsku]['upc12']
                 print (UPCsku,sku, skuColor, color,upc,'<--------------------------------------------------------------')

       skuUPClist={}
       skuUPClist[sku]=upc
       styleInfo['sku']=skuUPClist
       styleInfo['title']=title
       styleInfo['dec']=dec

    else:
       print ('skip: ',sku)
       continue
    if style not in styleLib:
       styleLib[style]=styleInfo
    else:
       styleLib[style]['sku'][sku]=upc
    #print (sku,style,color,size)


ATS0=ATS_loader()
fo= open('output.csv',"w",newline='') 
fieldnames=['Style','Supplier SKU','UPC','Title','Description','Size','Color','URL']	
writer=csv.DictWriter(fo,fieldnames=fieldnames)
writer.writeheader()
for item in styleLib.items():
    style=item[0]
    title = item[1]['title']
    dec = item[1]['dec']
    #print (item[1])
    for sku,upc in item[1]['sku'].items():
       color=sku[sku.find('-')+1:sku.find('-',sku.find('-',0)+1)]
       size = sku[sku.find('-',sku.find('-',0)+1)+1:]
       #print (sku,upc,title,size,color)
       if style[0]=='0':
          style='#'+style
       print ('writing.....',style,sku,upc,title)
       writer.writerow({'Style':style, 'Supplier SKU':sku,'UPC':'#'+upc,'Title':title,'Description':dec,'Size':size,'Color':color})
print (styleLib) 
#print (ATS0)
for list in ATS0:
   style=list[0]
   check=list[0]
   check=check.replace('W','')
   if check not in styleLib:
      print (style)

fo.close()
input(" exit")