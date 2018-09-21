from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import csv
import sys 
font1="arial.ttf"
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



watermark_text('sample.jpg','sample.jpg','D14XX\nPrice: xx$\nColor:\nxxxxx\nxxxxxx\nxxxxx\nxxxxx\nxxxxx\n',pos=(16,16))

base_image=Image.new('RGB',(5308,4096))
addPic = Image.open('sample.jpg')

    # add watermark to your image
x=0
y=0
for num in range(0,8):
   print (num,x,y)
   if num==4:
     x=0
     y+=2048
   base_image.paste(addPic, (x,y) )
 
   x+=1327


base_image=base_image.resize((int(5308*0.8),int(4096*0.8)),Image.ANTIALIAS)
base_image.show()
input('   ')