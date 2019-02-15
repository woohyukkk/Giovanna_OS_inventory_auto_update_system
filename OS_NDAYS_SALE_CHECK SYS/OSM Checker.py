import csv
import pymongo
from datetime import datetime
from datetime import timedelta
os_data_link='Z:/Zoe/OSM_Sale.csv'
OSM_list_link='Z:/Zoe/ATS/OS_Market_Checklist.csv'
OSM_FOS_link='Z:/Zoe/OSM/OSM_FOS.csv'
OSMlist=[]
OSMsale={}   # in N days
OSMsale0={}  # total days
OSMfos ={}
OSMlastSale={}
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
        style=style.replace('W','')
        if len(style)<4:
           style='0'+style
        color=item[3]
        date =item[24][0:8]
        date= '20'+date[6:8]+date[:5].replace('/','')
        if style not in OSMlastSale:
           OSMlastSale[style]=date
           print ('Last sale new',style,date)
        else:
           if date > OSMlastSale[style]:
              print ('Last sale updated',OSMlastSale[style],'=>',date,)
              OSMlastSale[style]=date
        for n in range (4,16):
           if '.' in item[n]:
              num=item[n][0:item[n].find('.')]
           if item[n] == '0' or item[n] == 0:
              num =0
           else:
              num=item[n]
           #print ('++',item[n],num)
           sum=sum+int(num)
        if style not in OSMsale0:
           OSMsale0[style]=1
           print ('OSMsale0:',date,style,color,'------>',OSMsale0[style])
        else:
           OSMsale0[style]+=sum
           print (date,style,color,'+',sum,'=',OSMsale0[style],)
        if int(date) < int(dateTest):
           print (style,date,'<',dateTest,'Skipped')
           continue
        if style not in OSMsale:
           OSMsale[style]=1
           print (date,style,color,'------>',OSMsale[style])
        else:
           OSMsale[style]+=sum
           print (date,style,color,'+',sum,'=',OSMsale[style],)


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
    print ('OSM sale data')
    for item,n in OSMsale.items():
       print (item,'===>',n)
    print ('OSM first on site data')
    for item,n in OSMfos.items():
       print (item,'===>',n)
    print ('OSM last sale data')
    for item,n in OSMlastSale.items():
       print (item,'===>',n)

def outputReport():
    fo= open(str(today)+'_OSM_Sale_Report_in_'+str(TstDays)+'days.csv',"w",newline='')
    #fo= open('out.csv',"w",newline='')
    fieldnames=['Style','Sale in '+TstDays+' days','Total Sale','Sale Months','Sale/Month','First on site','Last sale']
    writer=csv.DictWriter(fo,fieldnames=fieldnames)
    writer.writeheader()
    for style,qty in reportList.items():
        fos = 'N/A'
        lastSale='N/A'
        qtyTotal='0'
        SPM='0'
        saleMonth=0
        if style in OSMfos:
           fos = OSMfos[style]
           saleMonth=checkDays(today,fos)
        if style in OSMlastSale:
           lastSale=OSMlastSale[style]
        if style in OSMsale0:
           qtyTotal=OSMsale0[style]
           SPM=int(qtyTotal)/saleMonth
           SPM=round(SPM,2)
           
        writer.writerow({'Style':"'"+style,'Sale':qty,'Total Sale':qtyTotal,'Sale Months':saleMonth,'Sale/Month':SPM,'First on site':fos,'Last sale':lastSale})

def checkDays(d1,d2): #20190131
    out='0'
    if len(str(d1))!=8 or len(str(d2))!=8:
       print ('ERR: Wrong date format:',d1,d2)
       return -1
    if int(d1)>int(d2):
       d1,d2=d2,d1
    date1=str(d1)
    date2=str(d2)
    y1=int(date1[:4])
    y2=int(date2[:4])
    m1=int(date1[4:6])
    m2=int(date2[4:6])
    d1=int(date1[6:])
    d2=int(date2[6:])
    #print (y1,m1,d1)
    #print (y2,m2,d2)
    Dy=y2-y1
    Dm=m2-m1
    if Dm<0:
       Dm=Dm+12
       Dy=Dy-1
    Dd=d2-d1
    if Dd<0:
       Dd=Dd+30
       Dm=Dm-1
    #print(Dy,Dm,Dd)
    out = Dy*12+Dm+Dd/30
    #print(out)
    return round(out,2)

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
#outputList()
checkOSMsale()
outputReport()
print (dateTest)
print (today)
checkDays(today,dateTest)
