import os
import csv



store={}
f=open('Church NY.txt','r')
for line in f:
  #print (line)
  s0=line.find('bizname=')
  if s0!=-1:
    s1=line.find(';',s0)
    name=line[s0+8:s1]
    name=name.replace('&amp','')
    print ('Name:',name)
    s2=line.find('address=',s1)
    s3=line.find(';',s2)
    address=line[s2+8:s3]
    address=address.replace('&amp','')
    s4=line.find('city=',s3)
    s5=line.find(';',s4)
    city=line[s4+5:s5]
    city=city.replace('&amp','')
    s6=line.find('state=',s5)
    s7=line.find(';',s6)
    state=line[s6+6:s7]
    state=state.replace('&amp','')
    s8=line.find('zip=',s7)
    s9=line.find(';',s8)
    zip=line[s8+4:s9]
    zip=zip.replace('&amp','')
    addr={}
    addr['address']=address
    addr['city']=city
    addr['state']=state
    addr['zip']=zip
    store[name]=addr
    #print ('Address:',address,city,state,zip)


fo= open(state+' church.csv',"w",newline='')
fieldnames=['Name','Address','City','State','Zip']
writer=csv.DictWriter(fo,fieldnames=fieldnames)

writer.writeheader()

for name,add in store.items():
    writer.writerow({'Name':name,'Address':add['address'],'City':add['city'],'State':add['state'],'Zip':add['zip']})
    print (name,add['address'],add['city'],add['state'],add['zip'])
