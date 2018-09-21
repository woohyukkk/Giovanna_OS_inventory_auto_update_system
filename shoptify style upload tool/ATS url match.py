import csv
import os

mode='D'
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

def loadURL(list):
    f=open(mode+' styles url.csv')
    look=csv.reader(f)
    for item in look:
       style=item[0]
       color=item[1]
       url  =item[2]
       index=item[3]
       if '-'in style:
         style=style.replace('-','/')
       if style=='style':
          continue
       subList={}
       subList['Style']=style
       subList['Color']=color
       subList['URL']=url
       subList['Index']=index
       list.append(subList)
    f.close()
    return list
report=[]
URLlist=[]
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

f.close()

URLlist=loadURL(URLlist)
#print(URLlist)

#print (ATS0)
for item in ATS0:
  f=0
  if '0711A' in item['Style']:
    item['Style']=item['Style'].replace('A','')
  for item1 in URLlist:
    #print (item1)
    style=item1['Style']
    color2=item1['Color']
    url  =item1['URL']
    index=item1['Index']
    #print (item['Style'],item['Color'],"??",color2,url)
    if style==item['Style'] or style+'W'==item['Style']:
       if '#' in item['Color']:
          item['Color']=item['Color'][0:item['Color'].find('#')]
          item['Color']=item['Color'].replace(' ','')
       #print ('#['+item['Color']+']')
       #print ('mathing',item['Color'],color2)
       result=colorMatch(item['Color'],color2)
       if result==1:
         f=1
         sbuList=[]
         sbuList.append(item['Style'])
         sbuList.append(item['Color'])
         sbuList.append(color2)
         sbuList.append(item['Size'])
         sbuList.append(url)
         sbuList.append(index)
         report.append(sbuList)
         #print (item['Style'],item['Color'],item['Size'],color2,url)
        
  if f==0 and item['Style'][0]==mode:
    print(item['Style'],item['Color'],'<-----------------------------------------not found!')



fo= open('./URL DATA/'+mode+'_ATS_URL.csv',"w",newline='')
fieldnames=['Style','ATS COLOR','COLOR','SIZE','URL','INDEX']
writer=csv.DictWriter(fo,fieldnames=fieldnames)

writer.writeheader()

for list in report:
    writer.writerow({'Style':list[0],'ATS COLOR':list[1], 'COLOR':list[2],'SIZE':list[3],'URL':list[4],'INDEX':list[5]})
    print ("Report: ",list[0],list[1],list[2],list[3],list[4])




fo.close()
input("Enter to exit")