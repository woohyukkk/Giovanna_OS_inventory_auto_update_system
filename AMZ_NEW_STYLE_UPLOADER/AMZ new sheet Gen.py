import csv
import winfa

style='0910'
newList={}
header={}
URL=[]
UPC=[]
OSM={}
def getSKU(style):
    ATS=winfa.getATSW()
    for item in ATS:
        if style in item:
           print (item)
           newList[item]=ATS[item]
    fo= open(style+' upload file.csv',"w",newline='') 
    f=open('header.csv','r')
    look=csv.reader(f)
    for item in look:
        if len(item)>1:
           if item[1]!='':
              header[item[0]]=item[1]
           else:
              if len(item)>2:
                header[item[0]]=item[2] 
        elif len(item)==1:
           header[item[0]]=''
    print (header)
    writer=csv.DictWriter(fo,fieldnames=header)
    writer.writeheader()
###################write parent
    title=''
    dec  =''
    price=''
    brand=''
    outCol={}
    brand=getBrand(style)    #GC GIO
    if style in OSM:
       title=OSM[style][1]
       dec  =OSM[style][2]
       brand=OSM[style][3]
       price=OSM[style][4]
    for item in header:
        if item=='item_sku':
           outCol[item]=style
        elif item=='brand_name':
           outCol[item]=brand
        elif item=='item_name':
           outCol[item]=title     #Product name
        elif item=='external_product_id':
           outCol[item]=''     #UPC
        elif item=='color_name':
           outCol[item]=''
        elif item=='color_map':
           outCol[item]=''
        elif item=='size_name':
           outCol[item]=''
        elif item=='size_map':
           outCol[item]=''
        elif item=='standard_price':
           outCol[item]= price
        elif item=='main_image_url':
           outCol[item]=getURL(style)
        elif item=='other_image_url1':
           outCol[item]=''
        elif item=='other_image_url2':
           outCol[item]='https://www.dropbox.com/s/ki9w9lr1f60ndez/Giovanna%20Size%20Chart_Jacket.JPG?dl=0'
        elif item=='other_image_url3':
           outCol[item]='https://www.dropbox.com/s/lr0wjgl5iesz8aq/Giovanna%20Size%20Chart_Skirt.JPG?dl=0'
        elif item=='parent_child':
           outCol[item]='parent'
        elif item=='parent_sku':
           outCol[item]=''
        elif item=='relationship_type':
           outCol[item]=''
        elif item=='product_description':
           outCol[item]=dec
        elif item=='model':
           outCol[item]=style
        elif item=='part_number':
           outCol[item]=style
        elif item=='item_length':
           outCol[item]=''
        elif item=='item_width':
           outCol[item]=''
        elif item=='item_height':
           outCol[item]=''
        elif item=='item_dimensions_unit_of_measure':
           outCol[item]=''
        elif item=='fulfillment_center_id':
           outCol[item]=''
        else:
           outCol[item]=header[item]
        print('W:',item,'------>',outCol[item])
    writer.writerow(outCol)
####################write Children
    for sku in newList:
        #style=sku.split('-')[0]
        color0=sku.split('-')[1]
        size = sku.split('-')[2]
        qty  =newList[sku]
        color=winfa.findC(color0)
        print (style,color,size)
        outCol={}
        for item in header:
          if item=='item_sku':
           outCol[item]=sku
          elif item=='brand_name':
           outCol[item]=brand
          elif item=='item_name':
           outCol[item]=title     #Product name
          elif item=='external_product_id':
           outCol[item]=getUPC(style,color,size)     #UPC
           if outCol[item]==-1:
              outCol[item]=getUPC(style,color0,size)
          elif item=='color_name':
           outCol[item]=color
          elif item=='color_map':
           outCol[item]=''
          elif item=='size_name':
           outCol[item]=size
          elif item=='size_map':
           outCol[item]= mapSize(size)
          elif item=='standard_price':
           outCol[item]= price
          elif item=='quantity':
           outCol[item]=getQty(qty)
          elif item=='main_image_url':
           outCol[item]=getURL(style,color)
           if outCol[item]==-1:
              outCol[item]=getURL(style,color0)
          elif item=='other_image_url1':
              outCol[item]=getURL(style,color,1)
              if outCol[item]==-1:
                 outCol[item]=getURL(style,color0,1)
          elif item=='other_image_url2':
           outCol[item]='https://www.dropbox.com/s/ki9w9lr1f60ndez/Giovanna%20Size%20Chart_Jacket.JPG?dl=0'
          elif item=='other_image_url3':
           outCol[item]='https://www.dropbox.com/s/lr0wjgl5iesz8aq/Giovanna%20Size%20Chart_Skirt.JPG?dl=0'
          elif item=='parent_child':
           outCol[item]='Child'
          elif item=='parent_sku':
           outCol[item]=style
          elif item=='relationship_type':
           outCol[item]='Variation'
          elif item=='product_description':
           outCol[item]=dec
          elif item=='model':
           outCol[item]=style
          elif item=='part_number':
           outCol[item]=style
          else:
           outCol[item]=header[item]
        writer.writerow(outCol)

def mapSize(size):
    size=str(size)
    if 'W' not in size:
       size=int(size)
       if size<12:
          return 'Medium'
       elif size<16:
          return 'Large'
       elif size<=18:
          return 'X-large'
    else:
       if '14' in size:
          return 'X-Large'
       elif '16' in size or '18' in size:
          return 'XX-Large'
       elif '22' in size or '20' in size:
          return 'XXX-large'
       elif '26' in size or '24' in size:
          return 'XXXX-Large'
       elif '28' in size or '30' in size or '32' in size:
          return 'XXXXX-Large'
    return -1

def getBrand(style):
    if style[0]=='0':
       return 'Giovanna Signature'
    elif style[0]=='G':
       return 'Giovanna Collection'

def getQty(num):
    num=str(num)
    num=int(num)
    v=0
    if num>=1 and num<=3:
       v=1
    elif (num>3 and num < 11):
       v=2
    elif (num > 10):
       v=3
    return v

def getURL(style,color='*',index=0):
    if style[0]=='0':
       style=style[1:]
    for item in URL:
        if style == item[0] and winfa.colorMatch(color,item[1])==1:
           if index==0 and '0' in item[3]: 
              return item[2]
           elif index!=0 and '0' not in item[3]:
              return item[2]
        elif style == item[0] and color=='*':
           if index==0 and '0' in item[3]: 
              return item[2]
    print ('URL not found:',style,color,index)
    return -1

def getUPC(style,color,size):
    for item in UPC:
        #print (style,item[0])
        if style==item[0].replace('W','') and winfa.colorMatch(color,item[1])==1 and size == item[2]:
           #print ('UPC\n', item)
           #print (style,color,size,item[3])
           return item[3]
    return -1

def loadURL():
    f=open('./All styles url.csv','r')
    look=csv.reader(f)
    for item in look:
        list=[]
        for n in range(4):
          list.append(item[n].lstrip().rstrip().replace('-','/'))
        #print ('URL:',list)
        URL.append(list)

def loadUPC():
    f=open('./UPC data.csv','r')
    look=csv.reader(f)
    for item in look:
        list=[]
        sku=item[0]
        if '-' in sku and 'H' not in sku[0]:
          style=sku.split('-')[0]
          color=sku.split('-')[1]
          size = sku.split('-')[2]
        else:
          if sku[0]=='H' and '-' in sku:
              style=sku.split('-')[0]
              color=sku.split('-')[1]
              size = 'OS'
          else:
              continue
        list.append(style)
        list.append(color)
        list.append(size)
        list.append(item[1])
        UPC.append(list)
        #print (list)

def loadOSM():
    f=open('./OSM_DATA.csv','r')
    look=csv.reader(f)
    for item in look:
        list=[]
        style=item[0][0:item[0].find('-')]
        title=item[1]
        dec  =item[2]
        brand=item[3]
        price=item[4]
        list.append(style)
        list.append(title)
        list.append(dec)
        list.append(brand)
        list.append(price)
        OSM[style]=list

loadOSM()
loadUPC()
loadURL()
getSKU(style)
#print (getUPC('G1083','LAVENDER','12'))
