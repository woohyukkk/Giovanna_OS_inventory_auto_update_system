#get break down qty infomation from input.csv
#input:  input.csv
#output: output.csv

import csv
import winfa as winfa


f= open('./input.csv',"r")	
look=csv.reader(f)
fo= open('./output.csv',"w",newline='') 
fieldnames=['Style','Color','6', '8', '10','12','14','16','18','14w','16w','18w','20w','22w','24w','26w','28w','30w','32w','S','M','L','XL','1X','2X','3X']
writer=csv.DictWriter(fo,fieldnames=fieldnames)
writer.writeheader()
for item in look:
    style=item[0]
    if len(style)<4:
       style='0'+style
    outlist=winfa.getBreakDown(style,1)
    for color,line in outlist.items():
       for i in range(1,len(line)):
           if line[i] !='' and line[i] !=0 and line[i]!='0':
              line[i]=str(line[i])
              if int(line[i]) >= 8:
                 line[i] = ''
           else:
              line[i]=''
       if style[0]=='0':
          style=style.replace('0',"'0",1)
       writer.writerow({'Style':style,'Color':winfa.findC(color),'6':line[0], '8':line[1], '10':line[2],'12':line[3],'14':line[4],'16':line[5],'18':line[6],'14w':line[7],'16w':line[8],'18w':line[9],'20w':line[10],'22w':line[11],'24w':line[12],'26w':line[13],'28w':line[14],'30w':line[15],'32w':line[16],'S':line[16],'M':line[17],'L':line[18],'XL':line[19],'1X':line[20],'2X':line[21],'3X':line[22]})
       print('Output:',style,winfa.findC(color))
fo.close()
input('EXIT')