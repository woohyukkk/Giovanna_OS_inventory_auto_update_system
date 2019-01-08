import csv
import winfaColorMatch as winfa


f= open('./input.csv',"r")	
look=csv.reader(f)
fo= open('./output.csv',"w",newline='') 
fieldnames=['Style','Color','6', '8', '10','12','14','16','18','14w','16w','18w','20w','22w','24w','26w','28w','30w','32w']
writer=csv.DictWriter(fo,fieldnames=fieldnames)
writer.writeheader()
for item in look:
    style=item[0]
    outlist=winfa.getBreakDown(style)
    for color,line in outlist.items():
       if style[0]=='0':
          style=style.replace('0',"'0")
       writer.writerow({'Style':style,'Color':color,'6':line[0], '8':line[1], '10':line[2],'12':line[3],'14':line[4],'16':line[5],'18':line[6],'14w':line[7],'16w':line[8],'18w':line[9],'20w':line[10],'22w':line[11],'24w':line[12],'26w':line[13],'28w':line[14],'30w':line[15],'32w':line[16]})