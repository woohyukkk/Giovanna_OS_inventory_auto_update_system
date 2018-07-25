from xml.dom.minidom import parse
import xml.dom.minidom
import csv
import sys


f= open('ATS.csv',"r")  
look=csv.reader(f)
ATSlist=set()
Weblist=set()

for item in look:
    style=(item[0])
    if style == 'code':
      continue
    ATSlist.add(style)


print (ATSlist)

# 使用minidom解析器打开 XML 文档
DOMTree = xml.dom.minidom.parse("data.xml")
collection = DOMTree.documentElement


# 在集合中获取所有电影
styles = collection.getElementsByTagName("item")

notfoundN=0
totalN=0
# 打印每部电影的详细信息
for style in styles:
   #print (style)
      #print('found style')
      code = style.getElementsByTagName('title')[0]
      if len(code.childNodes)>0:
       totalN+=1
       styleCode=code.childNodes[0].data
       if '#'in styleCode:
         styleCode=styleCode[1:]
       if " " in styleCode:
         styleCode=styleCode[0:styleCode.find(' ')]
       if styleCode=='0711' or styleCode=='711':
         styleCode='0711A'
       Weblist.add(styleCode)
      if styleCode not in ATSlist and styleCode+'W' not in ATSlist:
        notfoundN+=1
        print (styleCode)
print ('Total processed:',totalN,'Not found:',notfoundN)

n=0
for item in ATSlist:
   if 'W' in item:
      item=item.replace('W','')
   if item not in Weblist:
     n+=1
     print (item)
print ('Total Web 0 Winfa 1:',n)
