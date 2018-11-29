#!/usr/bin/python
#v3.1 check for ATS, OS JCP, OS Marketing, Shopify Online Store inventory updating
# auto detect ATS sizeN,atsN
# auto detect WIP and use qtyN from atsN

import csv
import smtplib
import sys
import pandas as pd
#!/usr/bin/python
# -*- coding: UTF-8 -*-
outputList=['Quantity']
#mode = input("Search for :") 
count=0
OS_inv={}
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
        n=size.rfind('-',0,len(size))
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
              if osCode not in OS_inv:
                   OS_inv[osCode]=v
        else:
           print (osCode+" cant find in ATS: 0 -----> 0",name)
           noMatch+=1
           writer.writerow({'Supplier Sku':osCode, 'Quantity':'0','Warehouse Name':'Waitex' })
           if osCode not in OS_inv:
              OS_inv[osCode]=0
    f.close()
    fo.close()
    print ("OS total wrote:",wcount,"skipped:",skip,"Ats no match:",noMatch, "and",addCount,"items added.\n\n")
    return  

def UpdateShopify(ATS):
    print ('####################SHOPIFY file updating####################')
    f= pd.read_csv('./upload/output_Shopify.csv')
    f["Waitex Warehouse C/O Giovanna Apparel"]='0'
    for style,num in ATS.items():
      v=0
      num=int(num)
      if num>=2 and num<=3:
                 v=1
      elif (num>3 and num < 11):
                 v=2
      elif (num > 10):
                 v=3
      f.loc[f["SKU"]==style,"Waitex Warehouse C/O Giovanna Apparel"]=v
      print ('SKU',style,"V=>",v)
    f.to_csv('./upload/output_Shopify.csv', index=False)
    return  

def UpdateOS_Market(ATS):
    print ('####################OS file updating####################')
    wcount=0
    addCount=0
    skip=0
    noMatch=0
    fo= open('./upload/output_OS_Market.csv',"w",newline='') 
    fieldnames=['Supplier Sku','Quantity','Warehouse Name']	
    writer=csv.DictWriter(fo,fieldnames=fieldnames)
    writer.writeheader()
    f= open('OS_Market_Checklist.csv',"r")  
    look=csv.reader(f)
    for item in look:
        osCode=item[0]
        code=item[1]
        color=item[2]
        color2=item[3]
        size= item[0]
        n=size.rfind('-',0,len(size))
        size=size[n+1:len(size)]
		
        if code=='WINFA CODE':
           continue
        elif code=='':
           print (osCode+" skiped: 0 -----> 0")
           skip+=1
           writer.writerow({'Supplier Sku':osCode, 'Quantity':'0','Warehouse Name':'Waitex Warehouse' })
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
              writer.writerow({'Supplier Sku':osCode, 'Quantity':v,'Warehouse Name':'Waitex Warehouse' })
        else:
           print (osCode+" cant find in ATS: 0 -----> 0",name)
           noMatch+=1
           writer.writerow({'Supplier Sku':osCode, 'Quantity':'0','Warehouse Name':'Waitex Warehouse' })
    f.close()
    fo.close()
    print ("OS total wrote:",wcount,"skipped:",skip,"Ats no match:",noMatch, "and",addCount,"items added.\n\n")
    return  

def UpdateAMZ(ATS):
    print ('####################AMAZON file updating####################')
    wcount=0
    addCount=0
    skip=0
    noMatch=0
    fo= open('./upload/output_AMZ.csv',"w",newline='') 
    fieldnames=['Seller SKU','Product ID','Item name (aka Title)','Standard Price','Quantity','Condition Type','Offer Condition Note']	
    writer=csv.DictWriter(fo,fieldnames=fieldnames)
    writer.writeheader()
    f= open('Amz_checklist.csv',"r")  
    look=csv.reader(f)
    for item in look:
        osCode=item[0]
        code=item[1]
        color=item[2]
        color2=item[3]
        id    =item[4]
        size= item[0]
        n=size.rfind('-',0,len(size))
        size=size[n+1:len(size)]
		
        if code=='WINFA CODE':
           continue
        elif code=='':
           print (osCode+" skiped: 0 -----> 0")
           skip+=1
           writer.writerow({'Seller SKU':osCode, 'Quantity':'0','Product ID':id })
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
        if (name in ATS) :
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
              if num>=1 and num<=3:
                 v=1
              elif (num>3 and num < 11):
                 v=2
              elif (num > 10):
                 v=3
              print (name+": ",num,"----->"+str(v))
              wcount+=1
              addCount=addCount+v
              writer.writerow({'Seller SKU':osCode, 'Quantity':v,'Product ID':id  })
        elif (name2 in ATS) :
              num=ATS[name2]
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
              writer.writerow({'Seller SKU':osCode, 'Quantity':v,'Product ID':id  })
        else:
           print (osCode+" cant find in ATS: 0 -----> 0",name)
           noMatch+=1
           writer.writerow({'Seller SKU':osCode, 'Quantity':'0','Product ID':id })
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
        name2=''
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
    fo= open('product_template.csv',"w",newline='') 
    fieldnames=['Handle','Title','Body (HTML)','Vendor','Type','Tags','Published','Option1 Name','Option1 Value','Option2 Name','Option2 Value','Option3 Name','Option3 Value','Variant SKU','Variant Grams','Variant Inventory Tracker','Variant Inventory Qty','Variant Inventory Policy','Variant Fulfillment Service','Variant Price','Variant Compare At Price','Variant Requires Shipping','Variant Taxable','Variant Barcode','Image Src','Image Alt Text','Gift Card','Google Shopping / MPN','Google Shopping / Age Group','Google Shopping / Gender','Google Shopping / Google Product Category','SEO Title,SEO Description','Google Shopping / AdWords Grouping','Google Shopping / AdWords Labels','Google Shopping / Condition','Google Shopping / Custom Product','Google Shopping / Custom Label 0','Google Shopping / Custom Label 1','Google Shopping / Custom Label 2','Google Shopping / Custom Label 3','Google Shopping / Custom Label 4','Variant Image','Variant Weight Unit']	
    writer=csv.DictWriter(fo,fieldnames=fieldnames)
    writer.writeheader()
    print ('shopify import start',checkList)
    for list in ATS0: #list: color,size,qty,cate
       print (list)
       style=list[0]
       color=list[1]
       size=list[2]
       qty=list[3]
       cate=list[4]
       if style[0]=='G':
          collection='GIOVANNA COLLECTION'
       else:
          collection='GIOVANNA SIGNATURE'
       for item in checkList:
          if item==style or item+'W'==style:
             if item+'W'==style:
                title=item
             else:
                title=style
             if item not in wrote:
                if len(style)<=3:
                   style = '0'+style
                print ('Loading parent',style,color,size)
                wrote[item]=1
                writer.writerow({'Handle':title,'Title':title,'Vendor':'GIOVANNA APPAREL','Type':cate,'Tags':collection,'Published':'TRUE','Option1 Name':'COLOR','Option1 Value':color,'Option2 Name':'SIZE','Option2 Value':size,'Variant SKU':style+'-'+color+'-'+size,'Variant Inventory Tracker':'shopify','Variant Inventory Qty':'0','Variant Inventory Policy':'deny','Variant Fulfillment Service':'manual','Variant Requires Shipping':'TRUE','Variant Taxable':'FALSE','Gift Card':'FALSE','Google Shopping / Age Group':'Adult','Google Shopping / Gender':'Female','Google Shopping / Google Product Category':'Apparel & Accessories > Clothing','Google Shopping / AdWords Grouping':'Women suits', 'Google Shopping / Condition':'new','Google Shopping / Custom Product':'FALSE','Variant Weight Unit':'lb'})
             else:
                print ('Loading child',style,color,size)
                writer.writerow({'Handle':title,'Option1 Name':'COLOR','Option1 Value':color,'Option2 Name':'SIZE','Option2 Value':size,'Variant SKU':style+'-'+color+'-'+size,'Variant Inventory Tracker':'shopify','Variant Inventory Qty':'0','Variant Inventory Policy':'deny','Variant Fulfillment Service':'manual','Variant Requires Shipping':'TRUE','Variant Taxable':'FALSE'})

    

    return
   
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
    color=(item[1])
    for n in range(len(item)):
       if item[n]=='size1':
          sizeN=n
       if item[n]=='ats1':
          atsN=n
       if item[n]=='qty1':
          qtyN=n
       if item[n]=='wip':
          wipN=n
       if item[n]=='nowip_ats1':
          nwipATS=n
    if style == 'code':
       continue
    elif '0825' in style: # FOR JCP 0825
       nwipATS=qtyN
    if item[wipN]!='0':
       wipNum=item[wipN][0:item[wipN].find('.')]
    else:
       wipNum='0'
    if int(wipNum)>0:
       print ('WIP--->',wipNum,style,color)
       atsN=qtyN

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

    qty.append(item[nwipATS])
    qty.append(item[nwipATS+1])
    qty.append(item[nwipATS+2])
    qty.append(item[nwipATS+3])
    qty.append(item[nwipATS+4])
    qty.append(item[nwipATS+5])
    qty.append(item[nwipATS+6])
    qty.append(item[nwipATS+7])
    qty.append(item[nwipATS+8])
    qty.append(item[nwipATS+9])
    qty.append(item[nwipATS+10])
    qty.append(item[nwipATS+11])


    #print (style,color,size)
    for i in range(12):
      #print (i)
      if size[i]!='':
        key = style+"-"+color+"-"+str(size[i])
        Qty = qty[i]
        #print (Qty,Qty.find('.'),Qty[0:Qty.find('.')])

        if Qty!='0' and '.' in Qty:
           #print (Qty)
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
        ATS0.append(Alist)
        ATS[key]=Qty
        count+=1
      else:
        continue
	   
#print (ATS0,count)  
UpdateOS(ATS)
UpdateOS_Market(ATS)
UpdateJCP(ATS)
#shopify_import(ATS0)
#UpdateShopify(ATS)
UpdateAMZ(ATS)
if len(negativeList)>0:
  print ("############################################## Negative List Report ##################################################")
  for item,v in negativeList.items():
    print (item,": ",v)
else:
  print ('No neganative item')
f.close()
input(" exit")