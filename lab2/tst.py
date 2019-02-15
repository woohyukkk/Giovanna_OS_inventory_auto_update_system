import csv

count=0

fo= open('output.csv',"w",newline='') 
fieldnames=['jcp','winfa']	
writer=csv.DictWriter(fo,fieldnames=fieldnames)
writer.writeheader()
JCP={}
key=[]
f= open('input2.csv',"r")  
look=csv.reader(f)

for item in look:
    if item[0] not in JCP:
       JCP[item[0]]=int(item[1])
    else:
       JCP[item[0]]+=int(item[1])
    #print ('key<==',item[0])

for item in JCP:
       writer.writerow({'jcp':item,'winfa':JCP[item]})