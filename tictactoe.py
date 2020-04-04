board=[[' ',' ',' '],
       [' ',' ',' '],
       [' ',' ',' ']]

point = [[['a', 0], ['b', 0], ['c', 0]],
         [['d', 0], ['e', 0], ['f', 0]],
         [['g', 0], ['h', 0], ['i', 0]]]

points = [[['a', 0], ['b', 0], ['c', 0]],
         [['d', 0], ['e', 0], ['f', 0]],
         [['g', 0], ['h', 0], ['i', 0]]]

def table():
    print('--------')
    print('' + board[0][0], '|' + board[0][1], '|' + board[0][2])
    print('--------')
    print('' + board[1][0], '|' + board[1][1], '|' + board[1][2])
    print('--------')
    print('' + board[2][0], '|' + board[2][1], '|' + board[2][2])
    print('--------')

def board_full(board):
    fu=0
    for i in range(3):
        for j in range(3):
            if  board[i][j]==' ':
                fu+=1
    if fu>0:
        return False
    else:
        return True

def win(bo,le):
    if ((bo[0][0] == le and bo[0][1] ==le and bo[0][2] == le ) or
        (bo[1][0] == le and bo[1][1] ==le and bo[1][2] == le ) or
        (bo[2][0] == le and bo[2][1] ==le and bo[2][2] == le ) or
        (bo[0][0] == le and bo[1][0] ==le and bo[2][0] == le ) or
        (bo[0][1] == le and bo[1][1] ==le and bo[2][1] == le ) or
        (bo[0][2] == le and bo[1][2] ==le and bo[2][2] == le ) or
        (bo[0][0] == le and bo[1][1] ==le and bo[2][2] == le ) or
        (bo[0][2] == le and bo[1][1] ==le and bo[2][0] == le)):
         return True
    else:
        return False

def user(boa):
    run=True
    while run:
        u = input('Enter b/w 1-9 : ')
        try:
            u = int(u)
            u=u-1
            if u >= 0 and u < 9:
                x=int(u / 3)
                y=int(u % 3)
                if (boa[x][y] == ' '):
                    boa[x][y] = 'X'
                    run = False

                else:
                    print('Already Entered')
        except:
           print("Enter a number")
    table()

def check1(boa,x,y):
    a=0
    b=0
    c=0
    d=0
    e=0
    for i in range(3):
        for j in range(3):
            if not boa[x][y]==' ':
                return -1
            elif x==i and not y==j:
                if boa[i][j]=='O':
                    b+=1
                    if b == 2:
                        a = 90
                        return a
            elif y==j  and not x==i:
                if boa[i][j]=='O':
                    e+=1
                    if e== 2:
                        a = 90
                        return a
            elif x==y and i==j:
                if boa[i][j]=='O':
                    c+=1
                    if c == 2:
                        a = 90
                        return a
            elif (x==j and y==i) or i+j==2:
                if boa[i][j]=='O':
                    d+=1
                    if d == 2:
                        a = 90
                        return a
    return(b+c+d+e)

def check(boa,x,y):
    a=0
    b=0
    c=0
    d=0
    e=0
    for i in range(3):
        for j in range(3):
            #print(i,j)
            if not boa[x][y]==' ':
                return -1
            elif x==i and not y==j:
                if boa[i][j]=='X':
                    b+=1
                    if b == 2:
                        a = 90
                        return a
            elif y==j  and not x==i:
                if boa[i][j]=='X':
                    e+=1
                    if e== 2:
                        a = 90
                        return a
            elif x==y and i==j:
                if boa[i][j]=='X':
                    c+=1
                    if c == 2:
                        a = 90
                        return a
            elif ((i==0 and j==2) or (i==1 and j==1) or(i==2 and j==0)) and((x==0 and y==2) or (x==1 and y==1) or(x==2 and y==0))  and not i==x and not j==y :
                if boa[i][j]=='X':
                    d+=1
                    if d == 2:
                        a = 90
                        return a
    return(b+c+d+e)

def sort(p):
    for i in range(3):
        for j in range(3):
            for x in range(3):
                for y in range(3):
                    if p[i][j][1] > p[x][y][1]:
                        temp = p[i][j]
                        p[i][j] = p[x][y]
                        p[x][y] = temp
    return p

def fin(p,q,b):
    if q[0][0][1]>=p[0][0][1]:
        n=q[0][0][0]
    else:
        n = p[0][0][0]
    if n=='a' and b[0][0] ==' ':
        b[0][0]='O'
    elif n=='b' and b[0][1] ==' ':
        b[0][1]='O'
    elif n=='c' and b[0][2] ==' ':
        b[0][2]='O'
    elif n=='d' and b[1][0] ==' ':
        b[1][0]='O'
    elif n=='e' and b[1][1] ==' ':
        b[1][1]='O'
    elif n=='f' and b[1][2] ==' ':
        b[1][2]='O'
    elif n=='g' and b[2][0]==' ':
        b[2][0]='O'
    elif n=='h' and b[2][1]==' ':
        b[2][1]='O'
    elif n=='i' and b[2][2]==' ':
        b[2][2]='O'
    print(n)
    table()

def comp(boa):
    point = [[['a', 0], ['b', 0], ['c', 0]],
           [['d', 0], ['e', 0], ['f', 0]],
           [['g', 0], ['h', 0], ['i', 0]]]
    points = [[['a', 0], ['b', 0], ['c', 0]],
           [['d', 0], ['e', 0], ['f', 0]],
           [['g', 0], ['h', 0], ['i', 0]]]
    for x in range(3):
        for y in range(3):
            point[x][y][1]= check(boa,x,y)      #X
            points[x][y][1] = check1(boa, x, y) #O
    print(point)
    print(points)
    sort(point)
    sort(points)
    fin(point,points,boa)

def main():
    while not (board_full(board)):
        if not (win(board,'X')) :
            user(board)
        if (win(board, 'X')):
            print('You won the match')
            exit()
        if not (win(board, 'O')) :
            comp(board)
        if (win(board, 'O')):
            print('You lost the match')
            exit()
    if board_full(board):
        print('Tie')
        exit()

main()