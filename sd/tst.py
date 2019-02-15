


input=[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]

def sudo(input):
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
           print ('Pos.',i,j,'Area:',a,'PV:',pv0)
           if len(pv0)==1:
              print (i,j,input[i][j],'------->',pv0[0])
              input[i][j]=pv0[0]
              sudo(input)
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
sudo(input)
print ('Ans:')
for item in input:
    print (item)