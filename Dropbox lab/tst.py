import dropbox
import csv




accessToken='g4xbkHKkKwAAAAAAAAACqwCjEAwcxfUzjS_kyjInXWmBR609R6AlRASjsWNNnogx'



dbx = dropbox.Dropbox(accessToken)
dbx.users_get_current_account()
list=[]

n1=0
n2=0
for entry in dbx.files_list_folder('/style library/D Styles/watermark/').entries:
    #print(entry.path_lower)
    link=dbx.sharing_create_shared_link(entry.path_lower)
    URL=link.url
    filename=entry.name
    style=filename[0:filename.find(' ')]
    if '_'in filename:
      color=filename[filename.find(' '):filename.find('_')]
    else:
      color=filename[filename.find(' '):filename.find('.jpg')]
    print (style,color, URL)
    sublist=[]
    sublist.append(style)
    sublist.append(color)
    sublist.append(URL.replace('dl=0','dl=1'))
    list.append(sublist)

fo= open('D styles url.csv',"w",newline='')
fieldnames=['style','color','url']
writer=csv.DictWriter(fo,fieldnames=fieldnames)

writer.writeheader()

for info in list:
    writer.writerow({'style':info[0],'color':info[1], 'url':info[2]})
    print ("Report: ",info[0],info[1],info[2])






