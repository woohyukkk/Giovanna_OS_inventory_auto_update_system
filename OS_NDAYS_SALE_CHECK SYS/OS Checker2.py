import csv
import pymongo
from datetime import datetime
from datetime import timedelta
import winfa
os_data_link='Z:/Zoe/OS_Sale.csv'
OS_list_link='Z:/Zoe/ATS/Checklist.csv'
OS_FOS_link='Z:/Zoe/OSM/OS_FOS.csv'
OSlist={}
OSsale={}   # in N days
OSsale0={}  # total days
OSfos ={}
OSlastSale={}
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
        if style not in OSlastSale:
           OSlastSale[style]=date
           print ('Last sale new',style,date)
        else:
           if date > OSlastSale[style]:
              print ('Last sale updated',OSlastSale[style],'=>',date,)
              OSlastSale[style]=date
        for n in range (4,16):
           item[n]=str(item[n])
           #print (item[n],type(item[n]))
           if '.' in item[n]: 
              #print ('dot found',item[n].find('.'))
              num=item[n][0:item[n].find('.')]
              #print ('after dot',num)
           if item[n] == '0' or item[n] == 0:
              num =0
           #print ('++',item[n],num,type(num))
           sum=sum+int(num)
        if style not in OSsale0:
           OSsale0[style]=1
           print ('OSsale0:',date,style,color,'------>',OSsale0[style])
        else:
           OSsale0[style]+=sum
           print (date,style,color,'+',sum,'=',OSsale0[style],)
        if int(date) < int(dateTest):
           print (style,date,'<',dateTest,'Skipped')
           continue
        if style not in OSsale:
           OSsale[style]=1
           print (date,style,color,'------>',OSsale[style])
        else:
           OSsale[style]+=sum
           print (date,style,color,'+',sum,'=',OSsale[style],)


def loadOSlist():
    f= open(OS_list_link,"r")  
    look=csv.reader(f)
    for item in look:
        if 'OS' in item[0]:
            continue
        style=item[0][0:item[0].find('-')]
        color=item[2]
        update=item[1]
        style=style.replace('W','')
        if style not in OSlist:
           if update!='':
              OSlist[style]='Y'
           else:
              OSlist[style]='N'
        else:
           if OSlist[style]=='N' and update!='':
              OSlist[style]='Y'


def checkOSsale():
    for item in OSlist:
      if item in OSsale:
        reportList[item]=OSsale[item]
        if OSsale[item]<1:
           print (item,'--------> No Sale!!!')
        else:
           print (item,'-------->',OSsale[item])

      else:
         r=checkFOS(item)
         if (r == 1):
             print ('ERR:',item,'not found in OSsale, FOS =',OSfos[item])
             reportList[item]='-1' #not sale in test days
         elif r==-1:
             print ('ERR:',item,'FOS shorter than',TstDays,'days. FOS =',OSfos[item],'<-----------------------')
             reportList[item]='N/A just on site'
         else:
             print ('ERR:',item,'not in FOS data.')
             reportList[item]='N/A FOS not updated'

def checkFOS( style ):
    style=style.replace('W','')
    if style in OSfos:
       if OSfos[style]<int(dateTest):
          return 1
       else:
          return -1
    else:
       return 0

def outputList():
    print ('OS list:')
    for item,n in OSlist.items():
       print (item,'===>',n)
    print ('OS sale data')
    for item,n in OSsale.items():
       print (item,'===>',n)
    print ('OS sale data0<----------')
    for item,n in OSsale.items():
       print (item,'===>',n)
    print ('OS first on site data')
    for item,n in OSfos.items():
       print (item,'===>',n)
    print ('OS last sale data')
    for item,n in OSlastSale.items():
       print (item,'===>',n)
    print ('OS output report list')
    for item,n in reportList.items():
       print (item,'===>',n)

def outputReport():
    fo= open(str(today)+'_OS_Sale_Report_in_'+str(TstDays)+'days.csv',"w",newline='')
    #fo= open('out.csv',"w",newline='')
    fieldnames=['Style','Sale in '+str(TstDays)+' days','Total Sale','Sale Months','Sale/Month','First on site','Last sale','Update Invt.','ATS']
    writer=csv.DictWriter(fo,fieldnames=fieldnames)
    writer.writeheader()
    for style,qty in reportList.items():
        fos = 'N/A'
        lastSale='N/A'
        qtyTotal='0'
        SPM='0'
        saleMonth=0
        up='N/A'
        if style in OSfos:
           fos = OSfos[style]
           saleMonth=checkDays(today,fos)
        if style in OSlastSale:
           lastSale=OSlastSale[style]
        if style in OSsale0:
           qtyTotal=OSsale0[style]
           if saleMonth!=0:
             SPM=int(qtyTotal)/saleMonth
             SPM=round(SPM,2)
             saleMonth=round(saleMonth)
        print ('OUT>',style)
        if style in OSlist:
           up=OSlist[style]
        if winfa.getBreakDown(style)== -1 or winfa.getBreakDown(style)=={}:
           ATS = 'N'
        else:
           ATS = 'Y'
        writer.writerow({'Style':"'"+style,'Sale in '+str(TstDays)+' days':qty,'Total Sale':qtyTotal,'Sale Months':saleMonth,'Sale/Month':SPM,'First on site':fos,'Last sale':lastSale,'Update Invt.':up,'ATS':ATS})
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
    return out

def loadOS_FOS(): # first on site date
    f= open(OS_FOS_link,"r")  
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
       if style.replace('W','') not in OSfos:
          OSfos[style]=int(FOS)

loadOSdata()
loadOSlist()
loadOS_FOS()
checkOSsale()
outputList()
outputReport()
print (dateTest)
print (today)

