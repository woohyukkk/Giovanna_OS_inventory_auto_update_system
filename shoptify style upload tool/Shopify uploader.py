#!/usr/bin/python
#v1.0 check for ATS and Alert
import csv
import smtplib
import sys
import pandas as pd
#!/usr/bin/python
# -*- coding: UTF-8 -*-
outputList=['Quantity']
#mode = input("Search for :") 

mode='G'
count=0
URLdata=[]
urlStack={}
def addTitleDec(style):
   style=style.replace('W','')
   f=open('StyleUploadLib-winfa.csv','r')
   look=csv.reader(f)
   output=['','','']
   for item in look:
       style0=item[0]
       style0=style0.replace('#','')
       upc = item[2]
       title=item[3]
       dec=  item[4]
       if style==style0:
          output[0]=upc
          output[1]=title
          output[2]=dec
          return output
   print ('Title Dec not found!<-------------------')
   return output

def urlSort(e):
   index=e[e.find('@')+1:]
   return index
def loadURL(data):
   f=open('./URL DATA/'+mode+'_ATS_URL.csv','r')
   look=csv.reader(f)
   for item in look:
    style=item[0]
    color=item[1]
    size=item[3]
    url=item[4]
    index=item[5]
    print (url)
    sublist=[]
    sublist.append(style)
    sublist.append(color)
    sublist.append(size)
    sublist.append(url)
    sublist.append(index)
    data.append(sublist)
   return data

def CheckList(ATS):
    f= open('checkList.csv',"r")  
    look=csv.reader(f)
    for item in look:
        osCode=item[0]
        code=item[1]
        color=item[2]
        size= item[0]
        n=size.find('-', 8)
        size=size[n+1:len(size)]
        if code=='WINFA CODE' or code=='':
           continue
        if (code[0]=='H'):     #is hat
           name=code+"-"+color+"-"+"OS"
        else:
           name=code+"-"+color+"-"+size
        if name in ATS:
           if (int(ATS[name])<3):
              print (name+": "+ATS[name])
        else:
           print (name+" does not exist!")
    f.close()
    return
	
def UpdateOS(ATS):
    print ('####################OS file updating####################')
    wcount=0
    addCount=0
    skip=0
    noMatch=0
    fo= open('./upload/output_OS.csv',"w",newline='') 
    fieldnames=['Supplier Sku','Quantity','Warehouse Name']	
    writer=csv.DictWriter(fo,fieldnames=fieldnames)
    writer.writeheader()
    f= open('checkList.csv',"r")  
    look=csv.reader(f)
    for item in look:
        osCode=item[0]
        code=item[1]
        color=item[2]
        color2=item[3]
        size= item[0]
        n=size.find('-', 8)
        size=size[n+1:len(size)]
		
        if code=='WINFA CODE':
           continue
        elif code=='':
           print (osCode+" skiped: 0 -----> 0")
           skip+=1
           writer.writerow({'Supplier Sku':osCode, 'Quantity':'0','Warehouse Name':'Waitex' })
           continue
        if (code[0]=='H'):     #is hat
           name=code+"-"+color+"-"+"OS"
           name2=''
        else:
           name=code+"-"+color+"-"+size
           name2=code+"-"+color2+"-"+size
        if ('0'+name)in ATS:
           name='0'+name
        if ('0'+name2)in ATS:
           name2='0'+name2
        if name in ATS:
              num=ATS[name]
              num=int(num)
              if '#'in name2:
                if name2 in ATS:
                  num2=ATS[name2]
                  num2=int(num2) 
                  print ('*'+name+" + "+color2+"----->" ,num, " + " ,num2)
                  num=num+num2
                else:
                  print (name2+" does not exist!")
              v=0
              if num>=2 and num<=3:
                 v=1
              elif (num>3 and num < 11):
                 v=2
              elif (num > 10):
                 v=3
              print (name+": ",num,"----->"+str(v))
              wcount+=1
              addCount=addCount+v
              writer.writerow({'Supplier Sku':osCode, 'Quantity':v,'Warehouse Name':'Waitex' })
        else:
           print (osCode+" cant find in ATS: 0 -----> 0")
           noMatch+=1
           writer.writerow({'Supplier Sku':osCode, 'Quantity':'0','Warehouse Name':'Waitex' })
    f.close()
    fo.close()
    print ("OS total wrote:",wcount,"skipped:",skip,"Ats no match:",noMatch, "and",addCount,"items added.\n\n")
    return  

def UpdateJCP(ATS):
    print ('####################JCP file updating####################')
    wcount=0
    addCount=0
    fo= open('./upload/output_JCP.csv',"w",newline='') 
    fieldnames=['IN','Supplier Sku','YES','Quantity','Blank','Blank','Blank','Blank','Decription','Blank','Blank','Blank','Blank','Blank','Blank','Blank','Blank','Blank','Blank','Blank','Blank','Blank','SKU','JCPENNEY']	
    writer=csv.DictWriter(fo,fieldnames=fieldnames)
    #writer.writeheader()
    f= open('JCP_checkList.csv',"r")  
    look=csv.reader(f)
    for item in look:
        jcpCode=item[0]
        code=item[1]
        color=item[2]
        color2=item[3]
        size= item[0]
        n=size.find('-', 8)
        size=size[n+1:len(size)]
        dec=item[4]
        SKU=item[5]
        name=''
        if code=='WINFA CODE':
           continue
        if (code!=''):
           if(code[0]=='H'):		#is hat
             name=code+"-"+color+"-"+"OS"
             name2=''
           else:
              name=code+"-"+color+"-"+size
              name2=code+"-"+color2+"-"+size
        if ('0'+name)in ATS:
              name='0'+name
        if ('0'+name2)in ATS:
              name2='0'+name2
        if name in ATS:
              num=ATS[name]
              num=int(num)
              if '#'in name2:
                if name2 in ATS:
                  num2=ATS[name2]
                  num2=int(num2) 
                  print ('*'+name+" + "+color2+"----->" ,num, " + " ,num2)
                  num=num+num2
                else:
                  print (name2+" does not exist!")
              v=0
              if num>=2 and num<=3:
                 v=1
              elif (num>3 and num < 11):
                 v=2
              elif (num > 10):
                 v=3
              print (name+": ",num,"----->"+str(v))
              wcount+=1
              addCount=addCount+v
              writer.writerow({'IN':'IN','Supplier Sku':jcpCode,'YES':'Yes','Quantity':v,'Decription':dec,'SKU':SKU,'JCPENNEY':'JCPENNEY' })
        else:
           print (name+" does not exist!!")
           writer.writerow({'IN':'IN','Supplier Sku':jcpCode,'YES':'Yes','Quantity':'0','Decription':dec,'SKU':SKU,'JCPENNEY':'JCPENNEY' })
    f.close()
    fo.close()
    print ("JCP total wrote:",wcount, "and",addCount,"items added.\n\n")
    return  

def shopify_import(ATS0):

    wcount=0
    addCount=0
    wrote={}
    collect=''
    checkList=['0710','0823','G1055','G1056','D1339','D1343','D1499']#['G0844','0650','G1060']
    fo= open(mode+'_product_template.csv',"w",newline='') 
    fieldnames=['Handle','Title','Body (HTML)','Vendor','Type','Tags','Published','Option1 Name','Option1 Value','Option2 Name','Option2 Value','Option3 Name','Option3 Value','Variant SKU','Variant Grams','Variant Inventory Tracker','Variant Inventory Qty','Variant Inventory Policy','Variant Fulfillment Service','Variant Price','Variant Compare At Price','Variant Requires Shipping','Variant Taxable','Variant Barcode','Image Src','Image Alt Text','Gift Card','Google Shopping / MPN','Google Shopping / Age Group','Google Shopping / Gender','Google Shopping / Google Product Category','SEO Title,SEO Description','Google Shopping / AdWords Grouping','Google Shopping / AdWords Labels','Google Shopping / Condition','Google Shopping / Custom Product','Google Shopping / Custom Label 0','Google Shopping / Custom Label 1','Google Shopping / Custom Label 2','Google Shopping / Custom Label 3','Google Shopping / Custom Label 4','Variant Image','Variant Weight Unit']	
    writer=csv.DictWriter(fo,fieldnames=fieldnames)
    writer.writeheader()
    print ('shopify import start',checkList)
    for list in ATS0: #list: color,size,qty,cate
       URLlink=''
       style=list[0]
       color=list[1]
       size =list[2]

       num  =list[3]
       cate=list[4]
       group=list[6]
       v=0
       num=str(num)
       if num!='0':
         num=num[0:num.find('.')]
       num=int(num)
       if num>=2 and num<=3:
                 v=1
       elif (num>3 and num < 11):
                 v=2
       elif (num > 10):
                 v=3
       if 'W' in style and style.replace('W','') in urlStack:
         continue
       for item in URLdata:
          #print (item[0],style,item[1],color)
          if item[0]==style:
             urlSet=set()
             index=item[4]
             url=item[3]
             url=url+'@'+index
             urlSet.add(url)
             if style not in urlStack:
                 urlStack[style]=urlSet
             else:
                 urlStack[style].add(url)

    for list in ATS0: #list: color,size,qty,cate
       #print (list)
       URLlink=''
       style=list[0]
       color=list[1]
       if '#' in color:
          color=color[0:color.find('#')]
          color=color.replace(' ','')
       size=list[2]
       num=list[3]
       cate=list[4]
       group=list[5]
       temp=addTitleDec(style)
       if temp[1]=='' and temp[2]=='':
          continue
       desc=temp[2]
       titleInfo=temp[1]
       collection=''
       v=0
       num=str(num)
       if num!='0':
         num=num[0:num.find('.')]
       num=int(num)
       if num>=2 and num<=3:
                 v=1
       elif (num>3 and num < 11):
                 v=2
       elif (num > 10):
                 v=3
       if   group=='GCL':
          collection='GIOVANNA COLLECTION'
       elif group=='GIO':
          collection='GIOVANNA SIGNATURE'
       elif group=='EYS':
          print ('EYS skipped:',style,color,cate,group)
          continue
       if style[0]==mode:
             urlStyle=style+'-'+color
             if 'W'not in style:
                title=style
             else:
                title=style.replace('W','')
             if title not in wrote:
                if len(style)<=3:
                   style = '0'+style
                wrote[title]=1
                if style in urlStack:
                 for itemURL in urlStack[style]:
                  index=itemURL[itemURL.find('@')+1:]
                  url=itemURL[:itemURL.find('@')]
                  if index =='0' or index == '1':
                    URLlink=url
                    urlStack[style].remove(itemURL)
                    break
                if title[0]=='0':
                  title='#'+title
                print ('Loading parent',style,color,size,cate,collection,URLlink)
                writer.writerow({'Variant Grams':'1360','Body (HTML)':desc,'Variant Price':'0','Image Src':URLlink,'Handle':title,'Title':title+' '+titleInfo,'Vendor':'GIOVANNA APPAREL','Type':cate,'Tags':collection,'Published':'TRUE','Option1 Name':'COLOR','Option1 Value':color,'Option2 Name':'SIZE','Option2 Value':size,'Variant SKU':style+'-'+color+'-'+size,'Variant Inventory Tracker':'Shopify','Variant Inventory Qty':v,'Variant Inventory Policy':'deny','Variant Fulfillment Service':'manual','Variant Requires Shipping':'TRUE','Variant Taxable':'FALSE','Gift Card':'FALSE','Google Shopping / Age Group':'Adult','Google Shopping / Gender':'Female','Google Shopping / Google Product Category':'Apparel & Accessories > Clothing','Google Shopping / AdWords Grouping':'Women suits', 'Google Shopping / Condition':'new','Google Shopping / Custom Product':'FALSE','Variant Weight Unit':'lb'})
             else:
                urlList=[]
                if style in urlStack:
                 for itemURL in urlStack[style]:
                  index=itemURL[itemURL.find('@')+1:]
                  url=itemURL[:itemURL.find('@')]
                  urlList.append(itemURL)
                 urlList.sort(key=urlSort)
                 #print (urlList)
                 for itemURL in urlList:
                  index=itemURL[itemURL.find('@')+1:]
                  url=itemURL[:itemURL.find('@')]
                  URLlink=url
                  urlStack[style].remove(itemURL)
                  break
                if title[0]=='0':
                   title='#'+title
                print ('Loading child',index,style,color,size,cate,collection,URLlink)
                writer.writerow({'Variant Grams':'1360','Body (HTML)':'','Variant Price':'0','Image Src':URLlink,'Handle':title
				,'Option1 Name':'COLOR','Option1 Value':color,'Option2 Name':'SIZE','Option2 Value':size,'Variant SKU':style+'-'+color+'-'+size,'Variant Inventory Tracker':'Shopify','Variant Inventory Qty':v,'Variant Inventory Policy':'deny','Variant Fulfillment Service':'manual','Variant Requires Shipping':'TRUE','Variant Taxable':'FALSE'})


    fo.close()
    #addURLtoCVS()
    return

def addURLtoCVS():
  f= pd.read_csv('product_template.csv')
  for code,list in urlStack.items():

    for item in list:
      index=item[item.find('@')+1:]
      url=item[:item.find('@')]
      f.loc[(f["Handle"]==code),"Image Src"]=url
      f.to_csv('product_template.csv', index=False)
      print (code,'-url->',url)

       




URLdata=loadURL(URLdata)
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
        print("ATS: "+key+" <= "+Qty)
        if int(Qty)<0:
           negativeList[key]=Qty
        Alist=[]
        Alist.append(style)
        Alist.append(color)
        Alist.append(size[i])
        Alist.append(qty[i])
        Alist.append(cate)
        Alist.append(item[35])#group
        Alist.append(item[36])#warehouse
        ATS0.append(Alist)
        ATS[key]=Qty
        count+=1
      else:
        continue
	   
#print (ATS0,count)  
#UpdateOS(ATS)
#UpdateJCP(ATS)
shopify_import(ATS0)
if len(negativeList)>0:
  print ("############################################## Negative List Report ##################################################")
  for item,v in negativeList.items():
    print (item,": ",v)
else:
  print ('No neganative item')
f.close()
input(" exit")