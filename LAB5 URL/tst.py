import csv
import pandas as pd

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

urlLib={}
f=open('H styles url.csv','r')
look=csv.reader(f)
for item in look:
    style=item[0]
    color=item[1]
    url  =item[2]
    index=item[3]
    if style=='style':
      continue
    list=[]
    list.append(style)
    list.append(color)
    list.append(url)
    list.append(index)
    if style not in urlLib:
       urlLib[style+'-'+color+'-'+index]=list

fo= open('output.csv',"w",newline='')
fieldnames=['Supplier SKU','URL','URL-2','URL-3']
writer=csv.DictWriter(fo,fieldnames=fieldnames)
writer.writeheader()
f=open('DATA.csv','r')
look=csv.reader(f)

for item in look:
    style0=item[0]
    color0=item[6]
    #print (style0, color0)
    urlList=[]
    for sku,list in urlLib.items():
       style=list[0]
       color=list[1]
       url  =list[2]
       index=list[3]
       if style==style0 and (colorMatch(color0,list[1])==1 or colorMatch(list[1],color0)==1):
          #print ('@',style0,color0,index,url)
          urlList.append(url)
    #print ('@',style0,color0,len(urlList))
    if len(urlList)==0:
       urlList.append('0')
       urlList.append('0')
       urlList.append('0')
    elif len(urlList)==1:
       urlList.append('0')
       urlList.append('0')
    elif len(urlList)==2:
       urlList.append('0')
    print ('@',style0,color0,urlList)
    writer.writerow({'Supplier SKU':item[1],'URL':urlList[0], 'URL-2':urlList[1],'URL-3':urlList[2]})