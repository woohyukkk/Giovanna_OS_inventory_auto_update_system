#WINFA TOOL
#.Aloc(style, color) -- find all related Winfa UPC
#.findC( color )  --find color full name or short name.
#.getATS()           --return ATS data
#.getBreakDown(style)     -- get style breakdown qty
#.getQty(sku)             -- get qty from sku(xxxx-xxxx-xxxx)
import csv
from timeit import Timer

colorLib0={}  #BLK -> BlACK
colorLib1={}  #BLACK -> BLK
multicolorLib0={}
multicolorLib1={}
ATS={}
ATS0=[]
initialFlag=0
def colorMatch(color1,color2):# color1 for ATS color(short)
    if (' 'in color1 and ' ' not in color2) or (' 'not in color1 and ' ' in color2):
        return -1
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


def initialLoad():
    global initialFlag
    if initialFlag==0:
       load_winfa_color()
       load_ATS()
       initialFlag=1


def load_winfa_color():
   f=open('Z:/Zoe/ATS/ColorData.csv','r')
   look=csv.reader(f)
   for item in look:
       dotColorFlag=0
       multiColorFlag=0
       if item[0]=='code' or '#' in item[0] or '0' in item[0]:
          continue
       colorList=[]
       winfaColor=item[0]
       dec       =item[1]
       winfaColor=winfaColor.upper()
       dec=dec.upper()
       if '.' in winfaColor:
          dotColorFlag=1
       if '/' in winfaColor:
          multiColorFlag=1
       if '.' in dec:
         dec=dec.replace('DK.','DARK')
         dec=dec.replace('LT.','LIGHT')
         dec=dec.replace('A.','APPLE')
         dec=dec.replace('S.','SOFT')
         dec=dec.replace('O.','OCEAN')
         dec=dec.strip()
       if multiColorFlag==1:
          colorList=dec.replace(' ','').split('/')
       if multiColorFlag==0:
          #print (winfaColor,'<-----',dec)
          colorLib0[winfaColor]=dec
          colorLib1[dec]=winfaColor
   f.close()
   f=open('Z:/Zoe/ATS/ColorData.csv','r')
   look=csv.reader(f)
   for item in look:
       result=''
       dotColorFlag=0
       multiColorFlag=0
       if item[0]=='code' or '#' in item[0] or '0' in item[0]:
          continue
       colorList=[]
       winfaColor=item[0]
       dec       =item[1]
       winfaColor=winfaColor.upper()
       dec=dec.upper()
       if '.' in winfaColor:
          dotColorFlag=1
       if '/' in winfaColor:
          multiColorFlag=1
       if '.' in dec:
         dec=dec.replace('DK.','DARK')
         dec=dec.replace('LT.','LIGHT')
         dec=dec.replace('A.','APPLE')
         dec=dec.replace('S.','SOFT')
         dec=dec.replace('O.','OCEAN')
         dec=dec.replace('M.','MUSTARD')
       if multiColorFlag==1:
          dec=dec.replace('/ ','/')
          colorList=dec.split('/')
          newList=[]
          for item in colorList:
              if ' ' in item:
                 temp=''
                 subItem=item.split(' ')
                 for sub in subItem:
                    if sub in colorLib0:
                       temp=temp+colorLib0[sub]
                    else:
                       temp=temp+sub
                    temp=temp+' '
                 item=temp.rstrip()
              if item in colorLib0:
                 newList.append(colorLib0[item])
              else:
                 newList.append(item)
          #print ('@Multi color:',winfaColor,'----->',newList)
          for color in newList:
              result=result+'/'+color
          multicolorLib0[winfaColor]=result[1:]

def load_ATS():
  f= open('Z:Zoe/ATS/ATS.csv',"r")  
  look=csv.reader(f)
  for item in look:
    size=[]
    qty=[]
    style=(item[0])
    color=(item[1])
    color=color.upper()
    for n in range(len(item)):
       if item[n]=='size1':
          sizeN=n
       if item[n]=='ats1':
          atsN=n
       if item[n]=='qty1':
          qtyN=n
       if item[n]=='wip':
          wipN=n
       if item[n]=='nowip_ats1':
          nwipATS=n
    if style == 'code':
       continue
    if item[wipN]!='0':
       wipNum=item[wipN][0:item[wipN].find('.')]
    else:
       wipNum='0'
    if int(wipNum)>0:
       #print ('WIP--->',wipNum,style,color)
       atsN=qtyN

    cate=item[6]
    des=item[2]
    size.append(item[sizeN])
    size.append(item[sizeN+1])
    size.append(item[sizeN+2])
    size.append(item[sizeN+3])
    size.append(item[sizeN+4])
    size.append(item[sizeN+5])
    size.append(item[sizeN+6])
    size.append(item[sizeN+7])
    size.append(item[sizeN+8])
    size.append(item[sizeN+9])
    size.append(item[sizeN+10])
    size.append(item[sizeN+11])
    #print ('nwipATS<-------------------------------------------------',nwipATS)
    qty.append(item[nwipATS])
    qty.append(item[nwipATS+1])
    qty.append(item[nwipATS+2])
    qty.append(item[nwipATS+3])
    qty.append(item[nwipATS+4])
    qty.append(item[nwipATS+5])
    qty.append(item[nwipATS+6])
    qty.append(item[nwipATS+7])
    qty.append(item[nwipATS+8])
    qty.append(item[nwipATS+9])
    qty.append(item[nwipATS+10])
    qty.append(item[nwipATS+11])


    #print (style,color,size)
    for i in range(12):
      #print (i)
      if size[i]!='':
        key = style+"-"+color+"-"+str(size[i])
        Qty = qty[i]
        #print (Qty,Qty.find('.'),Qty[0:Qty.find('.')])

        if Qty!='0' and '.' in Qty:
           #print (Qty)
           Qty=Qty[0:Qty.find('.')]
        #print("ATS: "+key+" <= "+Qty)
        Alist=[]
        Alist.append(style)
        Alist.append(color)
        Alist.append(size[i])
        Alist.append(qty[i])
        Alist.append(cate)
        ATS0.append(Alist)
        ATS[key]=Qty

      else:
        continue
  ATS_comboLot(ATS)

def findC(color):
    Cflag=0
    mark=''
    result='N/A'
    if '#' in color:
      Cflag=1
      mark =color[color.find('#'):]
      color=color[0:color.find('#')]

    initialLoad()
    #print (colorLib0)
    #print (colorLib1)
    color=color.upper()
    color=color.lstrip()
    color=color.rstrip()
    if color in colorLib0:
       result= colorLib0[color]
    elif color in colorLib1:
       result= colorLib1[color]
    elif color in multicolorLib0:
       result= multicolorLib0[color]
    else:
       print ('ERR:',color,'not found')
    if Cflag==1:
       result=result+' '+mark
    return result

def Aloc(style,color):
    output=[]
    tempList2=[]
    initialLoad(initialFlag)
    result=[]
    color=color.upper()
    color=color.lstrip()
    color=color.rstrip()
    #print ('Aloc...........................',style,color)
    if '/' in color:
       tempList=color.split('/')
       for item in tempList:
           #print ('tempList-',item)
           if item in colorLib0:
              tempList2.append(colorLib0[item])
           else:
              tempList2.append(item)
       #print ('templist:',tempList2)
       for Clist in multicolorLib0:
           count = 0
           #print (Clist)
           for color in tempList2:
              if color in multicolorLib0[Clist]:
                 count+=1
           if count == len(multicolorLib0[Clist]):
              #print ('Multi Color:',tempList2,'in',Clist)
              result.append(style+'-'+Clist)
              result.append(style+'W-'+Clist)
    else:
       if color in colorLib0:
          color = colorLib0[color]
       #print ('1 color:',color)
       if color in colorLib1:
          result.append(style+'-'+colorLib1[color])
          result.append(style+'W-'+colorLib1[color])
       else:
          print ('ERR: Color not found in Lib:',color)
          return -1
    #print ('result:',result)
    for item in ATS: 
      for it in result:
       if it in item:
          if int(ATS[item])>0:
             #print (result,'--->',item)
             output.append(item)
    return output

def getBreakDown(style):
    initialLoad()
    outputList={}
    existF=0
    for item in ATS0:
        style0=item[0]
        color0=item[1]
        size0 =item[2]
        qty   =item[3]
        if style0=='0711A':
           style0='0711'
        if style == style0 or style+'W'==style0:
           #color0=findC(color0)
           existF=1
           if color0 not in outputList:
                 #index:0, 1,  2, 3, 4, 5, 6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,17,18,19, 20, 21, 22, 23
                  #size:6, 8, 10,12,14,16,18,14w,16w,18w,20w,22w,24w,26w,28w,30w,32w, S, M, L, XL, 1X, 2X, 3X
              sizelist=['','','','','','','','' ,'' ,'' ,'' ,'' ,'' ,'' ,'' ,'' ,'' ,'','','', '', '', '', '']
              if size0=='6':
                 sizelist[0]=qty
              elif size0=='8':
                 sizelist[1]=qty
              elif size0=='10':
                 sizelist[2]=qty
              elif size0=='12':
                 sizelist[3]=qty
              elif size0=='14':
                 sizelist[4]=qty
              elif size0=='16':
                 sizelist[5]=qty
              elif size0=='18':
                 sizelist[6]=qty
              elif size0=='14W':
                 sizelist[7]=qty
              elif size0=='16W':
                 sizelist[8]=qty
              elif size0=='18W':
                 sizelist[9]=qty
              elif size0=='20W':
                 sizelist[10]=qty
              elif size0=='22W':
                 sizelist[11]=qty
              elif size0=='24W':
                 sizelist[12]=qty
              elif size0=='26W':
                 sizelist[13]=qty
              elif size0=='28W':
                 sizelist[14]=qty
              elif size0=='30W':
                 sizelist[15]=qty
              elif size0=='32W':
                 sizelist[16]=qty
              elif size0=='S':
                 sizelist[17]=qty
              elif size0=='M':
                 sizelist[18]=qty
              elif size0=='L':
                 sizelist[19]=qty
              elif size0=='XL':
                 sizelist[20]=qty
              elif size0=='1X':
                 sizelist[21]=qty
              elif size0=='2X':
                 sizelist[22]=qty
              elif size0=='3X':
                 sizelist[23]=qty
              outputList[color0]=sizelist
           else:
              if size0=='6':
                 outputList[color0][0]=qty
              elif size0=='8':
                 outputList[color0][1]=qty
              elif size0=='10':
                 outputList[color0][2]=qty
              elif size0=='12':
                 outputList[color0][3]=qty
              elif size0=='14':
                 outputList[color0][4]=qty
              elif size0=='16':
                 outputList[color0][5]=qty
              elif size0=='18':
                 outputList[color0][6]=qty
              elif size0=='14W':
                 outputList[color0][7]=qty
              elif size0=='16W':
                 outputList[color0][8]=qty
              elif size0=='18W':
                 outputList[color0][9]=qty
              elif size0=='20W':
                 outputList[color0][10]=qty
              elif size0=='22W':
                 outputList[color0][11]=qty
              elif size0=='24W':
                 outputList[color0][12]=qty
              elif size0=='26W':
                 outputList[color0][13]=qty
              elif size0=='28W':
                 outputList[color0][14]=qty
              elif size0=='30W':
                 outputList[color0][15]=qty
              elif size0=='32W':
                 outputList[color0][16]=qty
              elif size0=='S':
                 outputList[color0][17]=qty
              elif size0=='M':
                 outputList[color0][18]=qty
              elif size0=='L':
                 outputList[color0][19]=qty
              elif size0=='XL':
                 outputList[color0][20]=qty
              elif size0=='1X':
                 outputList[color0][21]=qty
              elif size0=='2X':
                 outputList[color0][22]=qty
              elif size0=='3X':
                 outputList[color0][23]=qty
              outputList[color0]
    if (existF==0):
       print ('ERR:',style,'not found')
       return -1
    return outputList

def getATS():
   load_ATS()
   for list in ATS0:
       print ('ATS:',list)
   return ATS0


def getQty(sku): #SKU: xxxx-xxx-xxx
    initialLoad()
    style=sku[0:sku.find('-')]
    color=sku[sku.find('-')+1:sku.find('-',sku.find('-')+1)]
    size =sku[sku.rfind('-')+1:]
    if 'W' not in style and 'W' in size:
       style=style+'W'
    if color not in colorLib0:
       color=findC(color)
    #print ('|',style,'|',color,'|',size,'|')
    sku2=style+'-'+color+'-'+size
    if sku2 in ATS:
       return (ATS[sku2])
    else:
       color=findC(color)
       sku2=style+'-'+color+'-'+size
       if sku2 in ATS:
          return (ATS[sku2])
       else:
          print ('ERR:',sku,'not found.')
          return -1

def ATS_comboLot(ATS):
    for item in ATS:
       lotN='N/A'
       qty=0
       s1=item.find('-',0)
       s2=item.find('-',s1+1)
       if s1!=-1 and s2!=-1:
          style = item[0:s1]
          color = item[s1+1:s2]
          size  = item[s2+1:]
          qty   = ATS[item]
       else:
          print ("Error: '-' missing",item,s1,s2)
          continue
       if '#' in color:
          lotN=color[color.find('#'):]
          color=color.replace(' ','')
          color=color[0:color.find('#')]
          code = style+'-'+color+'-'+size
          if code in ATS:
             #print ('Root:',code,ATS[code])
             #print ('*',code,'=',ATS[code],'+',qty)
             ATS[code]=int(ATS[code])+int(qty)
             #print (code,ATS[code])
          else:
             #print (item,'Root not found<---------------------------------------------')
             #print ('Creating',code,'<--',item)
             ATS[code]=ATS[item]
             del ATS[item]
    delist=[]
    for item in ATS:
        if '#' in item:
           delist.append(item)
    for item in delist:
       del ATS[item]
       #print ('DEL',item)
if __name__ == '__main__':
   print ('HW')
   print (getBreakDown('0301'))


