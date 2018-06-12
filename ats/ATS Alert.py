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
		
        if code=='WINFA CODE' or code=='':
           continue
        if (code[0]=='H'):     #is hat
           name=code+"-"+color+"-"+"OS"
           name2=''
        else:
           name=code+"-"+color+"-"+size
           name2=code+"-"+color2+"-"+size
        if ('0'+name)in ATS:
           name='0'+name
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
           print (name+" does not exist!")
    f.close()
    fo.close()
    print ("Total wrote:",wcount,",and",addCount,"items added.")
    return  

def UpdateJCP(ATS):
    wcount=0
    addCount=0
    fo= open('output_JCP.csv',"w",newline='') 
    fieldnames=['Supplier Sku','Quantity','Decription','SKU']	
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
              writer.writerow({'Supplier Sku':jcpCode, 'Quantity':v,'Decription':dec,'SKU':SKU })
        else:
           print (name+" does not exist!!")
           writer.writerow({'Supplier Sku':jcpCode, 'Quantity':'0','Decription':dec,'SKU':SKU })
    f.close()
    fo.close()
    print ("Total wrote:",wcount,",and",addCount,"items added.")
    return  

def newATSscaner(ATS0):
    f= open('checkList.csv',"r")  
    look=csv.reader(f)
    for item in look:
        osCode=item[0]
        code=item[1]
        color=item[2]
        size= item[0]
        n=size.find('-', 8)
        size=size[n+1:len(size)]
        m=osCode.find('-', 1)
        osCode=osCode[0:m]
        if code=='WINFA CODE' or code=='':
           continue
        print (code,osCode,osCode[1:len(osCode)+1]+" "+str(osCode in ATS0),str(osCode[2:len(osCode)] in ATS0))
        if ((osCode in ATS0) or (osCode[1:len(osCode)+1] in ATS0))and (code==''):     #is hat
           print ('Need Check:',osCode)
        
    f.close()
    return
   
f= open('ATS.csv',"r")  
look=csv.reader(f)
ATS={}
ATS0={}

sf=0
for item in look:
    size=[]
    qty=[]
    style=(item[0])
    if style == 'code':
       continue
    color=(item[1])
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
        print(key+" = "+Qty)
        ATS0[style]=Qty
        ATS[key]=Qty
        count+=1
      else:
        continue
	   
print (ATS,count)
UpdateOS(ATS)
UpdateJCP(ATS)
#newATSscaner(ATS0)
f.close()