from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import csv
import sys 

rawPath='./raw/'
waterMarkPath='./wm/'
removeMaskPath='./rm mark.jpg'
WaterAndInfoPath='./wm+info/'
styleOnlyPath='./type#/'
font1="arial.ttf"
maskPath='./watermark.png'
maskPath_HAT='./Hat watermark.png'
def removeInfo(input_image_path,output_image_path,watermark_image_path,position):
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)
    # add watermark to your image
    base_image.paste(watermark, position)
    #base_image.show()
    base_image.save(output_image_path)

def watermark_with_photo(input_image_path,output_image_path,watermark_image_path,position):
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)

    # add watermark to your image
    base_image.paste(watermark, position ,mask=watermark)
    #base_image.show()
    base_image.save(output_image_path)

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


def loadPC(data):
    data['0921']='2 pc\n long coat+dress'
    data['D1351']='2 pc top+dress'
    f= open('STYLE DATA.csv',"r")  
    look=csv.reader(f)
    for item in look:
     jkt=0
     PCn=item[7].upper()
     type=item[8].upper()
     code=item[0]
     if 'JK' in PCn or 'JK' in type:
        jkt=1
     if '1'in PCn[0:8]:
         if code[0]=='P':
           PCn='1 pc skirt'
         else:
           PCn='1 pc dress'
        #print ('1--->PC')
     elif '2' in PCn[0:8]:
        PCn='2 pc set'
        #print ('2--->PC')
     elif '3' in PCn[0:8]:
        PCn='3 pc set'
     if code=='0711A' or code=='711A':
        code='0711'
     if jkt==1:
        print ('jkt<-------------')
        PCn = PCn.replace('set','jkt dress')
     if code not in data:
        data[code]=PCn

#watermark_text(img, outPath ,text,pos=(60, 60))
n=0
nf=0
count=0
StyleData={}
loadPC(StyleData)
print (StyleData)
PCn='not found'

######add watermark
for filename in os.listdir(rawPath):
   if '.jpg'in filename or '.JPG'in filename:
     if filename[0]!='H':
        watermark_with_photo(rawPath+filename, waterMarkPath+filename,maskPath,position=(0,0))
     else:
        watermark_with_photo(rawPath+filename, waterMarkPath+filename,maskPath_HAT,position=(0,0))
######add info 
for filename in os.listdir(waterMarkPath):
   if '.jpg'in filename or '.JPG'in filename:
      count+=1
      #print (count,filename)

      s0=filename.find(' ')
      style=filename[0:s0]
      name=filename[s0+1:]
      s1=name.find('.jpg')
      color=name[0:s1]
      if '_'in color:
        s2=color.find('_')
        color=color[0:s2]
      #PCn=getPC(style)


      if style in StyleData:
        PCn=StyleData[style]
      else:
        PCn='not found'
        print (style,'not found <-----------------------------------------------')

      if PCn=='not found' or PCn=='':
        print (style,'not found <-----------------------------------------------')
        nf+=1
        #continue
        if 'H' not in style:
         PCn=input('Enter PC number:')
        #print ('enter PC....1')
        #PCn='1'
        print ('@',style)
        if '1'in PCn:
         if style[0]=='P':
           PCn='1 pc skirt'
         else:
           PCn='1 pc dress'
         #print ('1--->PC')
        elif '2' in PCn:
         PCn='2 pc set'
         #print ('2--->PC')
        elif '3' in PCn:
         PCn='3 pc set'
        elif 'JK' in PCn:
         PCn='2 pc jkt dress'
        if style[0]!='H':
          StyleData[style]=PCn
      print (count,style,color,PCn)
      text=style+'\n'+color+'\n'+PCn
      if style[0]=='H':
          text=style+'\n'+color
      #watermark_with_photo(rawPath+filename, waterMarkPath+filename,maskPath, position=(0,0))
      #removeInfo(styleOnlyPath+filename, './tst/'+filename,removeMaskPath, position=(0,0))
      watermark_text(waterMarkPath+filename, WaterAndInfoPath+filename ,text,pos=(60, 60))
      n+=1
print ('Total processed:',n,'Total not found style:',nf)

######change name 
addon1='_wm'
addon2='_wms'
for s in range(1,3): 
 if s==1:
  addon = addon1
  path='./wm/'
 elif s==2:
  addon = addon2
  path='./wm+info/'
 else:
  print ('path not found')
 for filename in os.listdir(path):
    if 'jpg'in filename or 'JPG'in filename :

         os.rename(path+filename,path+filename[0:len(filename)-4]+addon+'.jpg')
         print ("processed ",addon,filename)


input('   ')