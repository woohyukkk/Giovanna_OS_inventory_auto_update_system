import csv
import os
def colorMatch(color1,color2):# color1 for ATS color(short)
    existC=0
    color1=color1.upper()
    color2=color2.upper()
    color2=color2.replace('-','/')
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
        Alist={}
        Alist['Style']=style
        Alist['Color']=color
        Alist['Size']=size[i]
        Alist['Qty']=qty[i]
        Alist['Category']=cate
        Alist['Descript']=item[2]
        Alist['Price']=item[4]
        ATS0.append(Alist)
        ATS[key]=Qty
        count+=1
      else:
        continue

for item in ATS0:
  f=0
  for filename in os.listdir("./pic/"):
   s=filename.find(' ')
   style=filename[0:s]
   if '_'in filename:
     color2=filename[s:filename.find("_")] 
   else:
     color2=filename[s:filename.find('.')]
   if style==item['Style'] or style+'W'==item['Style']:
     result=colorMatch(item['Color'],color2)
     if result==1:
        f=1
        print (item['Style'],item['Color'],"==",color2)
  if f==0 and item['Style'][0]=='D':
    print(item['Style'],item['Color'],'<-----------------------------------------not found!')

