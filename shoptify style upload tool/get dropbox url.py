import dropbox
import csv


mode='D'

accessToken='g4xbkHKkKwAAAAAAAAACqwCjEAwcxfUzjS_kyjInXWmBR609R6AlRASjsWNNnogx'



dbx = dropbox.Dropbox(accessToken)
dbx.users_get_current_account()
list=[]

n1=0
n2=0
for entry in dbx.files_list_folder('/style library/'+mode+' Styles/watermark/').entries:
    #print(entry.path_lower)
    link=dbx.sharing_create_shared_link(entry.path_lower)
    URL=link.url
    filename=entry.name
    style=filename[0:filename.find(' ')]
    if '_'in filename:
      color=filename[filename.find(' '):filename.find('_')]
    else:
      color=filename[filename.find(' '):filename.find('.jpg')]

    if filename.count('_')>1:#if back pic
      s=filename.find('_')
      #print (s+1,filename.find('_wm'))
      index=filename[s+1:filename.find('_wm')]
    else:
      index='0'
    print (style,color,index,URL)
    sublist=[]
    sublist.append(style)
    sublist.append(color)
    sublist.append(URL.replace('https://www.dropbox.com','https://dl.dropboxusercontent.com'))
    sublist.append(index)
    list.append(sublist)

fo= open(mode+' styles url.csv',"w",newline='')
fieldnames=['style','color','url','index']
writer=csv.DictWriter(fo,fieldnames=fieldnames)

writer.writeheader()

for info in list:
    writer.writerow({'style':info[0],'color':info[1], 'url':info[2],'index':info[3]})
    print ("Report: ",info[0],info[1],info[2])






