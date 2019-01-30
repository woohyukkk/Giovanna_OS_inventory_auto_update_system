import csv

count=0

fo= open('output.csv',"w",newline='') 
fieldnames=['style']	
writer=csv.DictWriter(fo,fieldnames=fieldnames)
writer.writeheader()

key=[]
f= open('key.csv',"r")  
look=csv.reader(f)

for item in look:
    key.append(item[0])
    #print ('key<==',item[0])

f= open('input.csv',"r")  
look=csv.reader(f)
n=0
for item in look:
    code=item[2]
    if code in key:
       n+=1
       writer.writerow({'style':'DEL'})
       print (code,'found')
    else:
       writer.writerow({'style':code})
print ('Total found:',n)