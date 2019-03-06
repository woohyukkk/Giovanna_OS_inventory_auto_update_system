


#input=[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
#input=[[".",".","9","7","4","8",".",".","."],["7",".",".",".",".",".",".",".","."],[".","2",".","1",".","9",".",".","."],[".",".","7",".",".",".","2","4","."],[".","6","4",".","1",".","5","9","."],[".","9","8",".",".",".","3",".","."],[".",".",".","8",".","3",".","2","."],[".",".",".",".",".",".",".",".","6"],[".",".",".","2","7","5","9",".","."]]
input=[['.', '.', '9', '7', '4', '8', '.', '.', '.'],['7', '.', '.', '6', '.', '2', '.', '.', '.'],['.', '2', '.', '1', '.', '9', '.', '.', '.'],['.', '.', '7', '9', '8', '6', '2', '4', '1'],['2', '6', '4', '3', '1', '7', '5', '9', '8'],['1', '9', '8', '5', '2', '4', '3', '6', '7'],['.', '.', '.', '8', '6', '3', '.', '2', '.'],['.', '.', '.', '4', '9', '1', '.', '.', '6'],['.', '.', '.', '2', '7', '5', '9', '.', '.']]
#input=[[".",".","9","7","4","8",".",".","."],["7",".",".",".",".",".",".",".","."],[".","2",".","1",".","9",".",".","."],[".",".","7",".",".",".","2","4","."],[".","6","4",".","1",".","5","9","."],[".","9","8",".",".",".","3",".","."],[".",".",".","8",".","3",".","2","."],[".",".",".",".",".",".",".",".","6"],[".",".",".","2","7","5","9",".","."]]
def sudo(input,mode=1):
  r=checkEnd(input)
  print('------------------input------------------')
  for item in input:
    print (item)
  print('------------------input------------------')
  if r==1:
     print ('END<---------------------------------------------------------')
     return 0
  for i in range(len(input)):
    print (input[i])
    for j in range (len(input[i])):
        if (input[i][j]=='.'):
           pv0=['1','2','3','4','5','6','7','8','9']
           a=0
           for n in range (9):
               x=input[i][n]
               if x in pv0:   #check x
                  pv0.remove(x)
               y=input[n][j]
               if y in pv0:   #check y
                  pv0.remove(y)
           # check area
           if   i<=2 and j<=2:   #A
               a='A'
               pv0=checkArea(a,pv0,input)
           elif i<=2 and j>=3 and j<=5:#B
               a='B'
               pv0=checkArea(a,pv0,input)
           elif i<=2 and j>=6 and j<=8:#C
               a='C'
               pv0=checkArea(a,pv0,input)
           elif i>=3 and i<=5 and j<=2:   #D
               a='D'
               pv0=checkArea(a,pv0,input)
           elif i>=3 and i<=5 and j>=3 and j<=5:#E
               a='E'
               pv0=checkArea(a,pv0,input)
           elif i>=3 and i<=5  and j>=6 and j<=8:#F
               a='F'
               pv0=checkArea(a,pv0,input)
           elif i>=6 and i<=8 and j<=2:   #G
               a='G'
               pv0=checkArea(a,pv0,input)
           elif i>=6 and i<=8 and j>=3 and j<=5:#H
               a='H'
               pv0=checkArea(a,pv0,input)
           elif i>=6 and i<=8  and j>=6 and j<=8:#I
               a='I'
               pv0=checkArea(a,pv0,input)
           if pv0==[]:
              print ('ERR: no possible PV.',i,j)
              #print ('Return',i0,j0,'-->',save0)
              #input[i0][j0]=save0
              return -1
           else:
              print ('Pos.',i,j,'Area:',a,'PV:',pv0)
           if len(pv0)==1:
              save=input[i][j]
              print (i,j,input[i][j],'------->',pv0[0])
              input[i][j]=pv0[0]
              r=sudo(input)
              if r==0:
                 #print ('break@')
                 return 0
              elif r==-1:
                 pv0.remove(input[i][j])
                 input[i][j]=save
                 print ('back->',i,j,save)
                 return -1
           elif len(pv0)==2 and mode==2:
              save=input[i][j]
              print ('@-1',i,j,input[i][j],'------->',pv0[0])
              input[i][j]=pv0[0]
              r=sudo(input,2)
              if r==0:
                 #print ('break@')
                 return 0
              elif r==-1:
                   #pv0.remove(input[i][j])
                   input[i][j]=save
              print ('@-2',i,j,input[i][j],'------->',pv0[1])
              input[i][j]=pv0[1]
              r=sudo(input,2)
              if r==0:
                 #print ('break@')
                 return 0
              elif r==-1:
                   #pv0.remove(input[i][j])
                   input[i][j]=save
              return -1
def checkArea(a,pv0,input):
    if a=='A':
       for i in range(0,3):
          for j in range(0,3):
             #print (i,j,input[i][j])
             if input[i][j] in pv0:
                #print ('A: remove',input[i][j])
                pv0.remove(input[i][j])
    elif a=='B':
       for i in range(0,3):
          for j in range(3,6):
             #print (i,j,input[i][j])
             if input[i][j] in pv0:
                #print ('A: remove',input[i][j])
                pv0.remove(input[i][j])
    elif a=='C':
       for i in range(0,3):
          for j in range(6,9):
             #print (i,j,input[i][j])
             if input[i][j] in pv0:
                #print ('A: remove',input[i][j])
                pv0.remove(input[i][j])
    if a=='D':
       for i in range(3,6):
          for j in range(0,3):
             #print (i,j,input[i][j])
             if input[i][j] in pv0:
                #print ('A: remove',input[i][j])
                pv0.remove(input[i][j])
    elif a=='E':
       for i in range(3,6):
          for j in range(3,6):
             #print (i,j,input[i][j])
             if input[i][j] in pv0:
                #print ('A: remove',input[i][j])
                pv0.remove(input[i][j])
    elif a=='F':
       for i in range(3,6):
          for j in range(6,9):
             #print (i,j,input[i][j])
             if input[i][j] in pv0:
                #print ('A: remove',input[i][j])
                pv0.remove(input[i][j])
    if a=='G':
       for i in range(6,9):
          for j in range(0,3):
             #print (i,j,input[i][j])
             if input[i][j] in pv0:
                #print ('A: remove',input[i][j])
                pv0.remove(input[i][j])
    elif a=='H':
       for i in range(6,9):
          for j in range(3,6):
             #print (i,j,input[i][j])
             if input[i][j] in pv0:
                #print ('A: remove',input[i][j])
                pv0.remove(input[i][j])
    elif a=='I':
       for i in range(6,9):
          for j in range(6,9):
             #print (i,j,input[i][j])
             if input[i][j] in pv0:
                #print ('A: remove',input[i][j])
                pv0.remove(input[i][j])
    return pv0
def checkEnd(input):
    for item in input:
        for n in item:
            if n=='.':
               return -1
    return 1
#sudo(input)
sudo(input,2)
print ('Ans:')
for item in input:
    print (item)