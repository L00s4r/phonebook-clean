"""for i in range(1, 4):
    for j in range(1, 6):
        print(f"i = {i}, j = {j}", end=" ")
    print()"""
#       ⬆        will print - 
#i = 1, j = 1 i = 1, j = 2 i = 1, j = 3 i = 1, j = 4 i = 1, j = 5 
#i = 2, j = 1 i = 2, j = 2 i = 2, j = 3 i = 2, j = 4 i = 2, j = 5 
#i = 3, j = 1 i = 3, j = 2 i = 3, j = 3 i = 3, j = 4 i = 3, j = 5 

#example:

"""a = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]] #nested list 

for row in a:
    for x in row:
        print(x, type(x), end=" ")
    print()""" 

#       ⬆        will print - 
#1 <class 'int'> 2 <class 'int'> 3 <class 'int'> 4 <class 'int'>
#2 <class 'int'> 3 <class 'int'> 4 <class 'int'> 5 <class 'int'>
#3 <class 'int'> 4 <class 'int'> 5 <class 'int'> 6 <class 'int'>

"""a = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]] #nested list 
b = [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]] #another nested list 
c = [] #list

for i, row in enumerate(a):
    r = []
    for j, x in enumerate(row):
        r.append(x + b[i][j])
    c.append(r)

print(c)"""

#       ⬆        will print - 
# [[2, 3, 4, 5], [4, 5, 6, 7], [6, 7, 8, 9]] 

"""t = ["— Скажи-ка, дядя,  ведь не даром",
    "Москва,  спаленная  пожаром",
    "Французу  отдана?",
    "Ведь  были  ж схватки боевые",
    "Да, говорят,  еще  какие!",
    "Недаром  помнит вся Россия",
    "Про день  Бородина!"
]

for i, line in enumerate(t):
    while line.count("  "):
        line = line.replace("  ", " ")
    t[i] = line

print(t)"""
#       ⬆        will print - 
# ['— Скажи-ка, дядя, ведь не даром', 'Москва, спаленная пожаром', 'Французу отдана?', 'Ведь были ж схватки боевые', 'Да, говорят, еще какие!', 'Недаром помнит вся Россия', 'Про день Бородина!']

"""M, N = list(map(int, input("Введите M и N: ").split()))

zeros = []
for i in range(M):
    zeros.append([0] * N)

print(zeros)

for i in range(M):
    for j in range(N):
        zeros[i][j] = 1

print(zeros)"""

#       ⬆        will print - 
#      [[0, 0, 0], [0, 0, 0]]
#      [[1, 1, 1], [1, 1, 1]]

A = "s"