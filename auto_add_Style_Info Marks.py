from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import csv
import sys 
 
def watermark_text(input_image_path,output_image_path,text, pos):
    photo = Image.open(input_image_path)
 
    # make the image editable
    drawing = ImageDraw.Draw(photo)
 
    black = (3, 8, 12)
    font = ImageFont.truetype("calibrib.ttf", 55)
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
        n='1 PC'
        #print ('1--->PC')
      elif '2' in PCn:
        n='2 PCs'
        #print ('2--->PC')
      elif '3' in PCn:
        n='3 PCs'
        #print ('3--->PC')
    #print ('return:',n)
    return n


img = 'D1334 Navy.jpg'
outPath='./new/'+img
text='D1334\nNAVY\n2PCs'
#watermark_text(img, outPath ,text,pos=(60, 60))

for filename in os.listdir("./pics/"):
   if '.jpg'in filename:
      s0=filename.find(' ')
      style=filename[0:s0]
      name=filename[s0+1:]
      s1=name.find('with')
      color=name[0:s1]
      if '_'in color:
        s2=color.find('_')
        color=color[0:s2]
      PCn=getPC(style)
      print (style,color,PCn)
      if PCn=='not found':
        continue
      text=style+'\n'+color+'\n'+PCn
      watermark_text("./pics/"+filename, './new/'+filename ,text,pos=(60, 60))