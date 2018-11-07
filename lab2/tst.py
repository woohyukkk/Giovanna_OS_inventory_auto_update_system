import csv

count=0
q=[0,0,0,0,0,0,0]
s=[0,0,0,0,0,0,'26W']
fo= open('output.csv',"w",newline='') 
fieldnames=['style','color','size']	
writer=csv.DictWriter(fo,fieldnames=fieldnames)
writer.writeheader()

f= open('input.csv',"r")  
look=csv.reader(f)
mode=0   # 1 for W style
for item in look:
    c=0
    if item[0]=='' or item[0]=='STYLE NO':
       continue
    style = item[0]
    color = item[1]
    q[0] = item[2]   # 8 14W
    q[1] = item[3]   #10 16W
    q[2] = item[4]   #12 18W
    q[3] = item[5]   #14 20W
    q[4] = item[6]   #16 22W
    q[5] = item[7]   #18 24W
    q[6] = item[8]   #26W
    if 'W' not in style:
       mode = 0
    else:
       mode = 1
    if mode == 0:
      s[0]='8'
      s[1]='10'
      s[2]='12'
      s[3]='14'
      s[4]='16'
      s[5]='18'
      for i in range(7):
        if q[i]!='':
           for n in range(int(q[i])):
              print (style,color,s[i])
              writer.writerow({'style':style, 'color':color,'size':s[i]})
              count+=1

    else:
      s[0]='14W'
      s[1]='16W'
      s[2]='18W'
      s[3]='20W'
      s[4]='22W'
      s[5]='24W'
      for i in range(7):
        if q[i]!='':
           for n in range(int(q[i])):
              print (style,color,s[i])
              writer.writerow({'style':style, 'color':color,'size':s[i]})
              count+=1

print ('Total:', count)