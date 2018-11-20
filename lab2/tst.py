import csv

count=0

fo= open('output.csv',"w",newline='') 
fieldnames=['style','color','size']	
writer=csv.DictWriter(fo,fieldnames=fieldnames)
writer.writeheader()

f= open('DATA.csv',"r")  
look=csv.reader(f)
data={}
for item in look:
    c=0
    if item[0]=='' or item[0]=='style':
       continue
    style = item[0]
    color = item[1]
    color=color.replace('-','/')
    if len(style)==3:
       style='#0'+style
    list=[]
    list.append(color.upper())
    if style not in data:
       data[style]=list
    else:
       data[style].append(color.upper().replace(' ',''))


for style,list in data.items():
    colors=''
    f=0
    for item in list:
        colors=colors+item+', '
    colors=colors[0:len(colors)-2]
    for item in list:
        f1= open('input.csv',"r")  
        look=csv.reader(f1)
        for item in look:
            if item[0] == style or '#'+item[0] == style :
               print('match',item[0],style)
               f=1
        if f==1:
           print (style, colors)
           writer.writerow({'style':style,'color':colors})



       