import os
import shutil

addon1='_wm'
addon2='_wms'
s=input('MODE(1 for wm,2 for wms''):')
if s=='1':
  addon = addon1
  path='./wm/'
elif s=='2':
  addon = addon2
  path='./wm+info/'
for filename in os.listdir(path):
    if 'jpg'in filename or 'JPG'in filename :

         os.rename(path+filename,path+filename[0:len(filename)-4]+addon+'.jpg')
         print ("processed",filename)

		 
input(' ')