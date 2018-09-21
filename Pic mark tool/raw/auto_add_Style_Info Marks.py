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

def removeInfo(input_image_path,output_image_path,watermark_image_path,position):
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)
    output_image_path=output_image_path[0:len(output_image_path)-4]+' with watermark.jpg'
    # add watermark to your image
    base_image.paste(watermark, position)
    #base_image.show()
    base_image.save(output_image_path)

def watermark_with_photo(input_image_path,output_image_path,watermark_image_path,position):
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)
    output_image_path=output_image_path[0:len(output_image_path)-4]+' with watermark.jpg'
    # add watermark to your image
    base_image.paste(watermark, position, mask=watermark)
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

def getPC(style):
    if style[0]=='0':
       style=style[1:]
    n='not found'
    #print('Finding PCn.')
    f= open('STYLE DATA.csv',"r")  
    look=csv.reader(f)
    for item in look:
     PCn=item[7]
     code=item[0]
     if code=='0711A' or code=='711A':
        code='711'
     #print (code,"----------",style)
     if code==style:
      #print (code,PCn)
      if '1'in PCn:
        n='1 pc dress'
        #print ('1--->PC')
      elif '2' in PCn:
        n='2 pc set'
        #print ('2--->PC')
      elif '3' in PCn:
        n='3 pc set'
        #print ('3--->PC')
    #print ('return:',n)
    return n

def loadPC(data):
    f= open('STYLE DATA.csv',"r")  
    look=csv.reader(f)
    for item in look:
     PCn=item[7]
     code=item[0]
     if '1'in PCn:
        PCn='1 pc dress'
        #print ('1--->PC')
     elif '2' in PCn:
        PCn='2 pc set'
        #print ('2--->PC')
     elif '3' in PCn:
        PCn='3 pc set'
     if code=='0711A' or code=='711A':
        code='711'
     if code not in data:
        data[code]=PCn



for filename in os.listdir('.'):
   if '.jpg'in filename or '.JPG'in filename:
      watermark_with_photo(filename,filename.replace('.jpg','_wm.jpg'),'watermark.png',position=(0,0))

input('   ')