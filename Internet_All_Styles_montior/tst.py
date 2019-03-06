#Internet business all styles checker
import winfa
import csv

OSlink='Z:/Zoe/ATS/checkList.csv'
OSMlink='Z:/Zoe/ATS/OS_Market_Checklist.csv'
JCPlink='Z:/Zoe/ATS/JCP_checkList.csv'
AMZlink='Z:/Zoe/ATS/Amz_checkList.csv'
ATS0=[]
styleList=set()
OSdata={}
OSdata0={}
JCPdata={}
JCPdata0={}
OSMdata={}
OSMdata0={}
AMZdata={}
AMZdata0={}


def loadATSWIP():
    global ATS0
    ATS0=winfa.getATS0W()
    #print (ATS0)
    for item in ATS0:
       #print (item[0])
       if 'W' in item[0]:
          if item[0].replace('W','') not in styleList:
             styleList.add(item[0])
             print ('set+W',item[0])
          else:
             continue
       styleList.add(item[0])
       print ('set+',item[0])
    styleList0=sorted(styleList)


    return styleList0

def loadAMZ():
    f= open(AMZlink,"r")  
    look=csv.reader(f)
    for item in look:
        #print (item[0])
        Code=item[0]
        style=item[0][0:item[0].find('-')].replace('W','')
        if len(style)==3:
           style='0'+style
        code=item[1]
        #print (style)
        #if code=='':
         #  continue
        updateF='N/A'
        if code!='':
              updateF='Y'
        else:
              updateF='N'
        color=item[2]
        color0=item[0].split('-')
        if len(color0)>1:
           color0=color0[1]
        if style.replace('W','') not in AMZdata0:
           c0list=[]
           c0list.append(color0)
           AMZdata0[style.replace('W','')]=c0list
        else:
           if color0 not in AMZdata0[style.replace('W','')]:
              AMZdata0[style.replace('W','')].append(color0)
        size= item[0]
        n=size.find('-', 8)
        size=size[n+1:len(size)]
        if code=='WINFA CODE' or item[0]=='':
           print ('Skipped')
           continue

        #print ('@',style)
        if style not in AMZdata:
           cList=[]
           cList.append(updateF)

           cList.append(color)
           AMZdata[style]=cList
           print ('OS new:',style)
        else:
           if color not in AMZdata[style] and color!='':
              if AMZdata[style][0]=='N' and updateF=='Y':
                 AMZdata[style][0]='Y'
              AMZdata[style].append(color)
    f.close()
    return

def loadJCP():
    f= open(JCPlink,"r")  
    look=csv.reader(f)
    for item in look:
        #print (item[0])
        Code=item[0]
        style=item[0][0:item[0].find('-')].replace('W','')
        if len(style)==3:
           style='0'+style
        code=item[1]
        #print (style)
        #if code=='':
         #  continue
        updateF='N/A'
        if code!='':
              updateF='Y'
        else:
              updateF='N'
        color=item[2]
        color0=item[0].split('-')
        if len(color0)>1:
           color0=color0[1]
        if style.replace('W','') not in JCPdata0:
           c0list=[]
           c0list.append(color0)
           JCPdata0[style.replace('W','')]=c0list
        else:
           if color0 not in JCPdata0[style.replace('W','')]:
              JCPdata0[style.replace('W','')].append(color0)
        size= item[0]
        n=size.find('-', 8)
        size=size[n+1:len(size)]
        if code=='WINFA CODE' or item[0]=='':
           print ('Skipped')
           continue

        #print ('@',style)
        if style not in JCPdata:
           cList=[]
           cList.append(updateF)

           cList.append(color)
           JCPdata[style]=cList
           print ('OS new:',style)
        else:
           if color not in JCPdata[style] and color!='':
              if JCPdata[style][0]=='N' and updateF=='Y':
                 JCPdata[style][0]='Y'
              JCPdata[style].append(color)
    f.close()
    return
	
def loadOS():
    f= open(OSlink,"r")  
    look=csv.reader(f)
    for item in look:
        #print (item[0])
        osCode=item[0]
        style=item[0][0:item[0].find('-')].replace('W','')
        if len(style)==3:
           style='0'+style
        code=item[1]
        #print (style)
        #if code=='':
         #  continue
        updateF='N/A'
        if code!='':
              updateF='Y'
        else:
              updateF='N'
        color=item[2]
        color0=item[0].split('-')
        if len(color0)>1:
           color0=color0[1]
        if style.replace('W','') not in OSdata0:
           c0list=[]
           c0list.append(color0)
           OSdata0[style.replace('W','')]=c0list
        else:
           if color0 not in OSdata0[style.replace('W','')]:
              OSdata0[style.replace('W','')].append(color0)
              print ('@append color>',style,color0,OSdata0[style.replace('W','')])
        size= item[0]
        n=size.find('-', 8)
        size=size[n+1:len(size)]
        if code=='WINFA CODE' or item[0]=='':
           print ('Skipped')
           continue

        #print ('@',style)
        if style not in OSdata:
           cList=[]
           cList.append(updateF)

           cList.append(color)
           OSdata[style]=cList
           print ('OS new:',style)
        else:
           if color not in OSdata[style] and color!='':
              if OSdata[style][0]=='N' and updateF=='Y':
                 OSdata[style][0]='Y'
              OSdata[style].append(color)

    f.close()
    return
def loadOSM():
    f= open(OSMlink,"r")  
    look=csv.reader(f)
    for item in look:
        #print (item[0])
        osCode=item[0]
        style=item[0][0:item[0].find('-')].replace('W','')
        if len(style)==3:
           style='0'+style
        code=item[1]
        #print (style)
        #if code=='':
         #  continue
        updateF='N/A'
        if code!='':
              updateF='Y'
        else:
              updateF='N'
        color=item[2]
        color0=item[0].split('-')
        if len(color0)>1:
           color0=color0[1]
        if style.replace('W','') not in OSMdata0:
           c0list=[]
           c0list.append(color0)
           OSMdata0[style.replace('W','')]=c0list
        else:
           if color0 not in OSMdata0[style.replace('W','')]:
              OSMdata0[style.replace('W','')].append(color0)
              #print ('@append color>',style,color0,OSMdata0[style.replace('W','')])
        size= item[0]
        n=size.find('-', 8)
        size=size[n+1:len(size)]
        if code=='WINFA CODE' or item[0]=='':
           print ('Skipped')
           continue

        #print ('@',style)
        if style not in OSMdata:
           cList=[]
           cList.append(updateF)

           cList.append(color)
           OSMdata[style]=cList
           print ('OS new:',style)
        else:
           if color not in OSMdata[style] and color!='':
              if OSMdata[style][0]=='N' and updateF=='Y':
                 OSMdata[style][0]='Y'
              OSMdata[style].append(color)
    f.close()
    return
list=loadATSWIP()
loadOS()
loadOSM()
loadJCP()
loadAMZ()

fo= open('output.csv',"w",newline='')
fieldnames=['Style','UpdateOS','UpdateOSM','UpdateJCP','UpdataAMZ','Check','ATS','OS','OSM','JCP','AMZ']
writer=csv.DictWriter(fo,fieldnames=fieldnames)
writer.writeheader()
for item in list:
    style = item
    ATSc  =[]
    clist=[]
    osClist=[]
    osClist0=[]
    osmClist=[]
    osmClist0=[]
    jcpClist=[]
    jcpClist0=[]
    amzClist=[]
    amzClist0=[]
    ATSc =winfa.getBreakDown(style.replace('W',''))
    for c in ATSc:
        clist.append(c)
    #print (clist)
    coutlist=[]

    for color in clist:          #ATS
        if '#' in color:
           #print ('rm',color,clist)
           
           newColor = color[0:color.find('#')].strip()
           #print (newColor)
           if newColor not in coutlist:
              coutlist.append(newColor)
        else:
           if color not in coutlist:
              coutlist.append(color)
    if style.replace('W','') in OSdata:  #OS
       osClist=OSdata[style.replace('W','')]
    else:
       osClist=' N/A'
    if style.replace('W','') in OSdata0:  #OS
       osClist0=OSdata0[style.replace('W','')]
    else:
       osClist0=' N/A'
    if style.replace('W','') in OSMdata:  #OSM
       osmClist=OSMdata[style.replace('W','')]
    else:
       osmClist=' N/A'
    if style.replace('W','') in OSMdata0:  #OSM
       osmClist0=OSMdata0[style.replace('W','')]
    else:
       osmClist0=' N/A'
    if style.replace('W','') in JCPdata:  #jcp
       jcpClist=JCPdata[style.replace('W','')]
    else:
       jcpClist=' N/A'
    if style.replace('W','') in JCPdata0:  #jcp
       jcpClist0=JCPdata0[style.replace('W','')]
    else:
       jcpClist0=' N/A'
    if style.replace('W','') in AMZdata:  #AMZ
       amzClist=AMZdata[style.replace('W','')]
    else:
       jcpClist=' N/A'
    if style.replace('W','') in AMZdata0:  #AMZ
       amzClist0=AMZdata0[style.replace('W','')]
    else:
       amzClist0=' N/A'
######################Check colors
    for c in coutlist:
       checkMark='X'
       if c in osClist:
          checkMark='P'
       else:
          for cc in osClist:
             if winfa.colorMatch(c,cc)==1:
                checkMark='P'
                break
       if c in osmClist:
          checkMark='P'
       else:
          for cc in osmClist:
             if winfa.colorMatch(c,cc)==1:
                checkMark='P'
                break
       if c in jcpClist:
          checkMark='P'
       else:
          for cc in jcpClist:
             if winfa.colorMatch(c,cc)==1:
                checkMark='P'
                break
       if c in amzClist:
          checkMark='P'
       else:
          for cc in amzClist:
             if winfa.colorMatch(c,cc)==1:
                checkMark='P'
                break
    print (style,'ATS:',coutlist,'OS:',osClist[1:],'UpdateOSM:',osmClist[1:], 'ATS:',coutlist,'OS:',osClist0,'OSM:',osmClist0)
    writer.writerow({'Style':"'"+style,'UpdateOS':osClist[1:],'UpdateOSM':osmClist[1:],'UpdateJCP':jcpClist[1:],'Check':checkMark, 'ATS':coutlist,'OS':osClist0,'OSM':osmClist0,'JCP':jcpClist0})
for item in OSdata:
    print (item)

