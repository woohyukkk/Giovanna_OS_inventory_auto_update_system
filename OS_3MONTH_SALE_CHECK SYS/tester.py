import csv
import pymongo
from datetime import datetime
from datetime import timedelta
os_data_link='Z:/Zoe/OSM_Sale.csv'
OSM_list_link='Z:/Zoe/ATS/OS_Market_Checklist.csv'
OSM_FOS_link='Z:/Zoe/OSM/OSM_FOS.csv'
OSMlist=[]
OSMsale={}
OSMfos ={}
reportList={}
TstDays=60
dateTest=datetime.now()-timedelta(days=TstDays)  #DEFAULT = 60  
dateTest=dateTest.strftime('%Y%m%d')
dateTest=str(dateTest)
today=int(datetime.now().strftime('%Y%m%d'))

def loadOSdata():
    f= open(os_data_link,"r")  
    look=csv.reader(f)
    for item in look:
        sum=0
        num=0
        if item[2]=='style':
           continue
        style=item[2]
        color=item[3]
        date =item[24][0:8]
        date= '20'+date[6:8]+date[:5].replace('/','')
        if int(date) < int(dateTest):
           continue
        for n in range (4,16):
           if '.' in item[n]:
              num=item[n][0:item[n].find('.')]
           if item[n] == '0' or item[n] == 0:
              num =0
           #print ('++',item[n])
           sum=sum+int(num)
        if style not in OSMsale:
           OSMsale[style]=1
           print (date,style,color,'------>',OSMsale[style])
        else:
           OSMsale[style]+=sum


def loadOSMlist():
    f= open(OSM_list_link,"r")  
    look=csv.reader(f)
    for item in look:
        if 'OS' in item[0]:
            continue
        style=item[0][0:item[0].find('-')]
        color=item[2]
        style=style.replace('W','')
        if style not in OSMlist:
           OSMlist.append(style)
           #print (style)
    OSMlist.sort()

def checkOSMsale():
    for item in OSMlist:
      if item in OSMsale:
        reportList[item]=OSMsale[item]
        if OSMsale[item]<1:
           print (item,'--------> No Sale!!!')
        else:
           print (item,'-------->',OSMsale[item])

      else:
         r=checkFOS(item)
         if (r == 1):
             print ('ERR:',item,'not found in OSMsale, FOS =',OSMfos[item])
             reportList[item]='-1' #not sale in test days
         elif r==-1:
             print ('ERR:',item,'FOS shorter than',TstDays,'days. FOS =',OSMfos[item],'<-----------------------')
             reportList[item]='N/A just on site'
         else:
             print ('ERR:',item,'not in FOS data.')
             reportList[item]='N/A FOS not updated'

def checkFOS( style ):
    style=style.replace('W','')
    if style in OSMfos:
       if OSMfos[style]<int(dateTest):
          return 1
       else:
          return -1
    else:
       return 0

def outputList():
    print ('OSM list:')
    for item in OSMlist:
       print (item)
    print ('OS sale data')
    for item,n in OSMsale.items():
       print (item,'===>',n)
    print ('OS first on site data')
    for item,n in OSMfos.items():
       print (item,'===>',n)

def outputReport():
    fo= open(str(today)+'_OSM_Sale_Report_in_'+str(TstDays)+'days.csv',"w",newline='')
    #fo= open('out.csv',"w",newline='')
    fieldnames=['Style','Sale','First on site']
    writer=csv.DictWriter(fo,fieldnames=fieldnames)
    writer.writeheader()
    for style,qty in reportList.items():
        fos = 'N/A'
        if style in OSMfos:
           fos = OSMfos[style]
        writer.writerow({'Style':style,'Sale':qty,'First on site':fos})

def loadOSM_FOS(): # first on site date
    f= open(OSM_FOS_link,"r")  
    look=csv.reader(f)
    for item in look:
       if 'SKU' in item[0]:
          continue
       #print (item[0])
       style = item[4][:item[4].find('-')]
       FOS   = item[20]
       if len(FOS)< 3:
          continue
       FOS= '20'+FOS[6:8]+FOS[:5].replace('/','')
       #print (style, FOS)
       if style.replace('W','') not in OSMfos:
          OSMfos[style]=int(FOS)

loadOSdata()
loadOSMlist()
loadOSM_FOS()
outputList()
checkOSMsale()
outputReport()
#print (dateTest)
#print (today)