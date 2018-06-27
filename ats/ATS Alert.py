#v1.0 check for ATS and Alert
import csv
import smtplib
import sys
#!/usr/bin/python
# -*- coding: UTF-8 -*-
outputList=['Quantity']
#mode = input("Search for :") 
count=0

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
    wcount=0
    addCount=0
    skip=0
    noMatch=0
    fo= open('output.csv',"w",newline='') 
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
              if num>0 and num<3:
                 v=1
              elif (num>2 and num < 11):
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
    print ("Total wrote:",wcount,"skipped:",skip,"Ats no match:",noMatch, "and",addCount,"items added.\n\n")
    return  

def UpdateJCP(ATS):
    wcount=0
    addCount=0
    fo= open('output_JCP.csv',"w",newline='') 
    fieldnames=['IN','Supplier Sku','YES','Quantity','Blank','Blank','Blank','Blank','Decription','Blank','Blank','Blank','Blank','Blank','Blank','Blank','Blank','Blank','Blank','Blank','Blank','Blank','SKU','JCPENNEY']	
    writer=csv.DictWriter(fo,fieldnames=fieldnames)
    writer.writeheader()
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
    print ("Total wrote:",wcount, "and",addCount,"items added.\n\n")
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
	   
print (ATS0,count)  
UpdateOS(ATS)
UpdateJCP(ATS)
#shopify_import(ATS0)
if len(negativeList)>0:
  print ("############################################## Negative List Report ##################################################")
  for item,v in negativeList.items():
    print (item,": ",v)
else:
  print ('No neganative item')
f.close()