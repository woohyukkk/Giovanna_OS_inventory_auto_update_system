from PIL import Image
import os
from resizeimage import resizeimage

for filename in os.listdir('.'):
    if 'jpg'in filename or 'JPG'in filename :
       with open(filename, 'r+b') as f:
           with Image.open(f) as image:
               print ('Processing......',filename)
               cover = resizeimage.resize_cover(image, [1000, 1000])
               cover.save('./1k/'+filename, image.format)