import csv

mode='0'

def searchURL(style0,color0): #ATS style color
   f=open(mode+'_ATS_URL.csv')
   look=csv.reader(f)
   for item in look:
      style=item[0]
      color=item[1]
      url=item[4]
      index=item[5]
      if (style==style0 or style==style0+'W') and color==color0 and (index =='0' or index=='1'):
        return url
   return 'NO URL'

f=open('input.csv')
look=csv.reader(f)

collection={}
for item in look:
  style=item[0]
  if mode=='0' and style[0]!='0':
    style='0'+style
  if style=='Handle':
    continue
  color=item[8]
  name=style+'-'+color
  if name not in collection:
    url = searchURL(style,color)
    collection[name]=url
    print (name, url)
f.close()
f=open('input.csv')
look=csv.reader(f)
for item in look:
  style=item[0]
  if mode=='0' and style[0]!='0':
    style='0'+style
  if style=='Handle':
    continue
  color=item[8]
  name=style+'-'+color
  if item[1]!='':
    del collection[name]
    print ('removing.....',name)

for item in collection:
  print (item)
  
fo= open(mode+'_product_template_extra.csv',"w",newline='') 
fieldnames=['Handle','Title','Body (HTML)','Vendor','Type','Tags','Published','Option1 Name','Option1 Value','Option2 Name','Option2 Value','Option3 Name','Option3 Value','Variant SKU','Variant Grams','Variant Inventory Tracker','Variant Inventory Qty','Variant Inventory Policy','Variant Fulfillment Service','Variant Price','Variant Compare At Price','Variant Requires Shipping','Variant Taxable','Variant Barcode','Image Src','Image Alt Text','Gift Card','Google Shopping / MPN','Google Shopping / Age Group','Google Shopping / Gender','Google Shopping / Google Product Category','SEO Title,SEO Description','Google Shopping / AdWords Grouping','Google Shopping / AdWords Labels','Google Shopping / Condition','Google Shopping / Custom Product','Google Shopping / Custom Label 0','Google Shopping / Custom Label 1','Google Shopping / Custom Label 2','Google Shopping / Custom Label 3','Google Shopping / Custom Label 4','Variant Image','Variant Weight Unit']	
writer=csv.DictWriter(fo,fieldnames=fieldnames)
writer.writeheader()
for name,url in collection.items():
  style=name

  title=style
  color=name[name.find('-')+1:]
  size='0'
  cate='SUIT'
  collection='GIOVANNA COLLECTION'
  URLlink=url
  print ('Loading parent',style,color,size,cate,collection,URLlink)
  writer.writerow({'Body (HTML)':'','Variant Price':'0','Image Src':URLlink,'Handle':title,'Title':title,'Vendor':'GIOVANNA APPAREL','Type':cate,'Tags':collection,'Published':'TRUE','Option1 Name':'COLOR','Option1 Value':color,'Option2 Name':'SIZE','Option2 Value':size,'Variant SKU':style,'Variant Inventory Tracker':'','Variant Inventory Qty':'0','Variant Inventory Policy':'deny','Variant Fulfillment Service':'manual','Variant Requires Shipping':'TRUE','Variant Taxable':'FALSE','Gift Card':'FALSE','Google Shopping / Age Group':'Adult','Google Shopping / Gender':'Female','Google Shopping / Google Product Category':'Apparel & Accessories > Clothing','Google Shopping / AdWords Grouping':'Women suits', 'Google Shopping / Condition':'new','Google Shopping / Custom Product':'FALSE','Variant Weight Unit':'lb'})
