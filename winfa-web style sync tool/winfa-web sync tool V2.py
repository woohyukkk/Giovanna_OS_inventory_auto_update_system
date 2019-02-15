import csv
import sys 
import winfa

#input: Z:/Zoe/ATS/ATS.csv, Z:/Zoe/ATS/products_export.csv

ATSpath='Z:/Zoe/ATS/ATSWIP.csv'
webInfoPath='Z:/Zoe/ATS/products_export.csv'
decSearchLen=30

def load_ATS(ATS): #get all style and colors info from ATS
    f= open(ATSpath,"r") 
    look=csv.reader(f)
    for item in look:
        if item[0]=='code':
           continue
        style=item[0]
        color=item[1]
        style=style.replace('W','')
        style=style.replace('0711A','0711')
        color=color.replace(' ','')
        if '#' in color:
           color=color[0:color.find('#')]
        code= style+'-'+color
        if code not in ATS:
           ATS.append(code)
           print ('ATS <---',code)


def count_ATS(ATS):
    print ('ATS color counting.....')

    for item in ATS:
        clist=[]
        style=item[0:item.find('-')]
        color=item[item.find('-')+1:]
        if style not in ATS_color_count:
           #print ('Creating',style,'--->',color)
           clist.append(color)
           ATS_color_count[style]=clist
        else:
           #print ('Adding',style,'-',color,'->',ATS_color_count[style])
           ATS_color_count[style].append(color)
    return


def load_webStyle(webStyle):
    f= open(webInfoPath,"r") 
    look=csv.reader(f)
    for item in look:
        if item[1]=='Title' or item[1]=='':
           continue
        title=item[1]
        dec  =item[2]
        publish=item[6]
        publish=publish.lower()
        if publish !='true':
           print ('Publish:',publish,title)
           continue
        code='N/A'
        title.replace('#','')
        code=title
        if len(dec)<decSearchLen:
           #print ('No decription:',code)
           noDecList.append(code)
        if code not in webStyle:
           r=getSC(code)
           #print ('processing...',code)
           if r==1:
             print ('webStyle <---> ATS',code)
           elif r==-1:
             print ('webStyle <----------------x ATS',code)



def match_ATS_WEB(ATS_color_count,web_color_count):
    snycDict={}
    noEqList=[]
    snycDict.update(ATS_color_count)
    snycDict.update(web_color_count)
    print ('\n SNYC total:', len(snycDict))
    for item in snycDict:
        if (item in ATS_color_count and item not in web_color_count) :
           print ('@Not in Web:',item)
        elif (item not in ATS_color_count and item in web_color_count):
           print ('@Not in ATS:',item)
        else:
           #print ('ATS color count:',item,ATS_color_count[item])
           #print ('Web color count:',item,web_color_count[item])
           if ATS_color_count[item] != web_color_count[item]:
              noEqList.append(item)
              #print ('Check',item,'ATS:',ATS_color_count[item],'Web:',web_color_count[item])
    for item in noEqList:
        print ('Check',item,'ATS:',ATS_color_count[item],'Web:',web_color_count[item])

    return

def getSC(item):
    result=[]
    s0=item.find(' ')
    s1=item.find(' ',s0+1)
    if s0!=-1 and s1!=-1:
       style=item[0:s0]
       color=item[s0+1:s1]
    elif s0!=-1 and s1==-1:
       style=item[0:s0]
       color=item[s0+1:]
    else:
       print ('SC not found',item)
       return -1
    result=winfa.Aloc(style,color)
    if result!=[]:
       return 1

def print_Nodec():
    noDecList.sort()
    for item in noDecList:
        code=getSC(item)
        print ('NO decription:',item,code)

        #print (ATS_color_count,len(ATS_color_count))
        #print (web_color_count,len(web_color_count))

noDecList=[]
ATS=[]   #item= style-color
ATS_color_count={}  # key = style, value = colors count number
webStyle=[]
web_color_count={}  # key = style, value = colors count number

#load_ATS(ATS)     #load all from ATS
#count_ATS(ATS) #count colors for style for winfa end
#print (ATS_color_count)

load_webStyle(webStyle)   #load all web styles(title)
#count_web(webStyle) #count colors for style for web end
#match_ATS_WEB(ATS_color_count,web_color_count) #match color numbers, print different
#print_Nodec()

input('Enter to exit')

