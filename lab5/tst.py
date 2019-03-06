import winfa
import csv
c=0
t=0
f=open('input.txt','r')
ATS=winfa.getATS0()
fo= open('output.csv',"w",newline='')
fieldnames=['Style','Color']
writer=csv.DictWriter(fo,fieldnames=fieldnames)

for line in f:
    if 'title' in line:
       t+=1
       sku=line[line.find('title=')+7:line.find('class=',line.find('title='))-2]
       style=sku.split('-')[0]
       r=winfa.getBreakDown(style)

       if r=={}:
          print (style)
          writer.writerow({'Style':style})
       else:
          print (sku,'<-------------------')


print (c,'in',t)