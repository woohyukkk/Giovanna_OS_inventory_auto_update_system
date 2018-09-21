# auto generate jpg from csv list
#File input: ATS.csv, Closeouts.csv
#File output: ./pic/ for mark info, ./out/ for BOOKs
#Process: 0.Build ATS dataBase 1.Load list for pick 2.Locate full color name and pic path from Style Lib 3.watermark info 4.generate 8pics*9pages(total 72 items)
import csv
import smtplib
import sys
import pandas as pd
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
font1="arial.ttf"
#!/usr/bin/python
# -*- coding: UTF-8 -*-
outputList=['Quantity']
#mode = input("Search for :") 

mode='H'
count=0
URLdata=[]
urlStack={}
closeoutList={}
PathList={}
def colorMatch(color1,color2):# color1 for ATS color(short)
    existC=0
    if '.'in color1:
      color1=color1[color1.find('.')+1:]
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
          return 0
       else:
          existC+=1
          color2=color2[s+1:]
       if existC==len(color1):
              return 1


def loadCloseout():
   f= open('Closeouts.csv',"r")
   look=csv.reader(f)
   for item in look:
      style=(item[0])
      price=(item[1])
      if style not in closeoutList:
        closeoutList[style]=price
        #print (style,price)
   return

def findFullColor(style,colorATS):
   mode=style[0]
   if mode =='T':
     return
   PATH="Z:/Style Library/"+mode+" Styles/Watermark"
   for filename in os.listdir(PATH):
    style0=filename[0:filename.find(' ')]
    if '_'in filename:
      color0=filename[filename.find(' '):filename.find('_')]
    else:
      color0=filename[filename.find(' '):filename.find('.jpg')]

    if filename.count('_')>1:#if back pic
      s=filename.find('_')
      #print (s+1,filename.find('_wm'))
      index=filename[s+1:filename.find('_wm')]
    else:
      index='0'
    #print (style0,color0,index)
    if style==style0:
       s=colorMatch(colorATS,color0)
       if s==1:
         #print (colorATS,'====match====',color0)
         return color0
   print (colorATS,'COLOR not found<=================================XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
   return color0

def findPicPath(style,color):
   mode=style[0]

   PATH="Z:/Style Library/"+mode+" Styles/Watermark/"
   if style=='T7006':
       path='Z:/Style Library/T Styles/T7006 Dk. Citron.jpg'
       return path
   elif style=='T5443':
       path='Z:/Style Library/T Styles/T5443 Gold.jpg'
       return path
   for filename in os.listdir(PATH):
    style0=filename[0:filename.find(' ')]
    if '_'in filename:
      color0=filename[filename.find(' '):filename.find('_')]
    else:
      color0=filename[filename.find(' '):filename.find('.jpg')]

    if filename.count('_')>1:#if back pic
      s=filename.find('_')
      #print (s+1,filename.find('_wm'))
      index=filename[s+1:filename.find('_wm')]
    else:
      index='0'
    #print (style0,color0,index)
    picPath=PATH+filename
    if style==style0 and color == color0 and (index=='0' or index=='1'):
       #print (style,color,'PATH found:',picPath)
       return picPath
   return 0
 
def watermark_text(input_image_path,output_image_path,text, pos):
    photo = Image.open(input_image_path)
    #output_image_path=output_image_path[0:len(output_image_path)-4]+' with watermark.jpg'
    # make the image editable
    drawing = ImageDraw.Draw(photo)
 
    black = (3, 8, 12)
    font = ImageFont.truetype(font1, 55) #hat 35 other 55
    drawing.text(pos, text, fill=black, font=font)
    #photo.show()
    photo.save(output_image_path)



f= open('ATS.csv',"r")
look=csv.reader(f)
ATS={}
ATS0=[]
finalList={}
negativeList={}
sf=0
for item in look:
    size=[]
    qty=[]
    style=(item[0])
    if style == 'code':
       continue
    color=(item[1])
    cate=item[7]
    group=item[36]
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
        if Qty =='':
           Qty=0
        #print("ATS: "+key+" <= "+Qty)
        if int(Qty)<0:
           negativeList[key]=Qty
        Alist=[]
        Alist.append(style)
        Alist.append(color)
        Alist.append(size[i])
        Alist.append(qty[i])
        Alist.append(cate)
        Alist.append(item[35])
        Alist.append(item[36])
        Alist.append(item[3]) # descrpition
        ATS0.append(Alist)
        ATS[key]=Qty
        count+=1
      else:
        continue

#shopify_import(ATS0)
loadCloseout()


for style,price in closeoutList.items():
   #print (style, price)
   flag=0
   for list in ATS0:
     if (list[0]==style or list[0]==style+'W') and int(list[3])>0:
        flag=1
        print (style,'--in stock-->',list[1])
        if style not in finalList:
           tempList={}
           colorList=set()
           colorList.add(list[1])
           tempList['color']=colorList
           tempList['price']=price
           finalList[style]=tempList
        else:
           finalList[style]['color'].add(list[1])
   if flag==0:
      print(style,'not found in ATS<-------------------------------------------')
count=0
nColorSet=set()
for style,List in finalList.items():
   for color in List['color']:
     fullColor=findFullColor(style,color)
     nColorSet.add(fullColor)
   List['color']=nColorSet
   print (count,style, List['color'],List['price'])
   for color in List['color']:
      s=findPicPath(style,color)
      if s!=0:
         PathList[style]=s
         print(style,'PATH=',s)
         if style[0]=='T':
            s=''
            break
         colorText=''
         for color in List['color']:
             colorText=colorText+color+'\n'
         text=style+'\nPrice:'+List['price']+'\nColor:\n'+colorText
         watermark_text(s,'./pic/'+style+'.jpg',text,pos=(16,16))
         PathList[style]='./pic/'+style+'.jpg'
         break
      else:
         print(style,color,'Not found<-------------------------')

   count+=1
   nColorSet.clear()




    # add watermark to your image
count=0

fileList=[]


f= open('Closeouts.csv',"r",newline='')
look = csv.reader(f)
for item in look:
     style=item[0]
     path=PathList[style]
     if style=='T7006':
       path='Z:/Style Library/T Styles/T7006 Dk. Citron.jpg'
     elif style=='T5443':
       path='Z:/Style Library/T Styles/T5443 Gold.jpg'
     if path!=None:
        fileList.append(path)
     else:
        print (style,'<-----------------------------------------------------------------NO PATH')

c=0
for n in range (0,9):
  base_image=Image.new('RGB',(5308,4096))
  x=0
  y=0
  for num in range(0,8):
   print (num,x,y)
   if num==4:
     x=0
     y+=2048
   if count > len(fileList)-1:
     break
   file=fileList[count]
   p=file
   addPic = Image.open(p)
   base_image.paste(addPic, (x,y))
   count+=1
   x+=1327


  base_image=base_image.resize((int(5308*0.8),int(4096*0.8)),Image.ANTIALIAS)

  base_image.save('./out/Book'+str(c)+'.jpg')
  c+=1
f.close()
input(" exit")