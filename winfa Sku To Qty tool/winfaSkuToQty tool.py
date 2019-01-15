import csv
import winfa


f= open('input.csv',"r")  
look=csv.reader(f)
fo= open('output.csv',"w",newline='') 
fieldnames=['sku','qty']
writer=csv.DictWriter(fo,fieldnames=fieldnames)
writer.writeheader()

for item in look:
    QTY=-1
    sku=item[0]
    sku0=item[0]
    qty=0
    if 'W' in sku and sku.find('W',0,6)==-1:
       sku=sku.replace('-','W-',1)
   #print (sku,qty)
    qty=winfa.getQty(sku)
    #print (sku,qty)
    qty=int(qty)

    if qty<=3 and qty>0:
       QTY=1
    elif qty>3 and qty<=10:
       QTY=2
    elif qty>10:
       QTY=3
    elif qty==0:
       QTY=0
    elif qty==-1:
       Qty=-1
    print (sku,'------',qty,'---->',QTY)
    writer.writerow({'sku':sku0,'qty':QTY})