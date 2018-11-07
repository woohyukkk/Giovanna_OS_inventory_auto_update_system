#!/usr/bin/python
#v1.0 check for ATS and Alert
import csv
import smtplib
import sys
#!/usr/bin/python
# -*- coding: UTF-8 -*-
outputList=['Quantity']
#mode = input("Search for :") 
count=0
OSdate={}
OSsetY=set()
OSsetN=set()
def CheckList(ATS):
    f= open('Z:/Zoe/ATS/checkList.csv',"r")  
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
    fo= open('./upload/output.csv',"w",newline='') 
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
           #print (osCode+" skiped: 0 -----> 0")
           skip+=1
           #writer.writerow({'Supplier Sku':osCode, 'Quantity':'0','Warehouse Name':'Waitex' })

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
                  #print ('*'+name+" + "+color2+"----->" ,num, " + " ,num2)
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
              #print (name+": ",num,"----->"+str(v))
              if name not in OSdate:
                print('OSdate<----------------------',name)
                OSdate[name]='Y'
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

def func():
    fo= open('output.csv',"w",newline='')
    fieldnames=['Style#','Color','On OS ']
    writer=csv.DictWriter(fo,fieldnames=fieldnames)
    writer.writeheader()

    for list in ATS0:
       style=list[0]
       color=list[1]
       size=list[2]
       qty=list[3]
       cate=list[4]
       if style+'-'+color+'-'+size in OSdate:

          if style in OSsetY:
             continue
          else:
             OSsetY.add(style+'-'+color)
             print (style,'YES<---------------')
             #writer.writerow({'Style#':style.replace('W',''),'Color':color,'On OS ':'YES'})
       else:

          if style in OSsetN:
             continue
          else:
             OSsetN.add(style)
             print (style,'NO')
             #writer.writerow({'Style#':style.replace('W',''),'Color':color,'On OS ':'NO'})
    for style,v in ATS_Style.items():
        if style in OSsetY:
          color=style[style.find('-')+1:]
          style=style[0:style.find('-')]
          writer.writerow({'Style#':'#'+style.replace('W',''),'Color':color,'On OS ':'YES'})
        else:
          color=style[style.find('-')+1:]
          style=style[0:style.find('-')]
          writer.writerow({'Style#':'#'+style.replace('W',''),'Color':color,'On OS ':'NO'})


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
        key = style+"-"+color+"-"+size[i]
        Qty = qty[i]
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
        ATS0.append(Alist)
        ATS[key]=Qty
        ATS_Style[style+"-"+color]='Y'
        count+=1
      else:
        continue

UpdateOS(ATS)
print (OSdate)
func()


f.close()
input(" exit")