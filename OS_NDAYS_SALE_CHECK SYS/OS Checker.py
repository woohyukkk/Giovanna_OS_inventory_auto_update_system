import csv
import pymongo
from datetime import datetime
from datetime import timedelta
os_data_link='Z:/Zoe/OS_Sale.csv'
OS_list_link='Z:/Zoe/ATS/Checklist.csv'
OS_FOS_link=''
OSlist=[]
OSsale={}
OSlastSale={}
OSfos ={}
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
        else:
           if date > OSlastSale[style]:
              OSlastSale[style]=date
        if int(date) < int(dateTest):
           print (style,date,'<',dateTest,'Skipped')
           continue
        for n in range (4,16):
           num=item[n]
           #print ('start:',num)
           if num=='' or num==0 or num=='0':
              num=0
              #print ('int: 0')
           else:
              num=str(num)
              if '.' in num:
                #print ('. found',num )
                num=num[0:num.find('.')]
                num=int(num)
              else:
                num=int(num)
                print ('int:',num)
           #print ('@',sum,num,type(num))
           sum=sum+num
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
        style=style.replace('W','')
        if style not in OSlist:
           OSlist.append(style)
           #print (style)
    OSlist.sort()

def checkOSsale():
    for item in OSlist:
      if item in OSsale:
        reportList[item]=OSsale[item]
        if OSsale[item]<1:
           print (item,'--------> No Sale!!!')
        else:
           print (item,'-------->',OSsale[item])

      else:
         r=1
         if (r == 1):
             print ('ERR:',item,'not found in OSsale.')
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
    for item in OSlist:
       print (item)
    print ('OS sale data')
    for item,n in OSsale.items():
       print (item,'===>',n)
    print ('OS first on site data')
    for item,n in OSfos.items():
       print (item,'===>',n)
    print ('OS last sale data')
    for item,n in OSlastSale.items():
       print (item,'===>',n)

def outputReport():
    fo= open(str(today)+'_OS_Sale_Report_in_'+str(TstDays)+'days.csv',"w",newline='')
    #fo= open('out.csv',"w",newline='')
    fieldnames=['Style','Sale','First on site','Last sale']
    writer=csv.DictWriter(fo,fieldnames=fieldnames)
    writer.writeheader()
    for style,qty in reportList.items():
        fos = 'N/A'
        lastSale='N/A'
        if style in OSfos:
           fos = OSfos[style]
        if style in OSlastSale:
           lastSale=OSlastSale[style]
        writer.writerow({'Style':"'"+style,'Sale':qty,'First on site':fos,'Last sale':lastSale})

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
#loadOS_FOS()
outputList()
checkOSsale()
outputReport()
print (dateTest)
print (today)