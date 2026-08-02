"""d = ["svo", 5, 7]

it = iter(d)

try:
    for i in range(len(d) + 1):
        print(next(it))
except StopIteration:
    print("все")"""
#       ⬆        will print - 
#                                  svo   
#                                   5
#                                   7
#                                  все


# ---------------------------------


"""s="svo"

it = iter(s)

try:
    for i in range(len(s) + 1):
        print(next(it))
except StopIteration:
    print("все")"""
#       ⬆        will print - 
#                                  s 
#                                  v
#                                  o
#                                  все


# ---------------------------------


"""s=range(0, 5)

it = iter(s)

try:
    for i in range(len(s) + 1):
        print(next(it))
except StopIteration:
    print("все")"""
#       ⬆        will print - 
#                                  0 
#                                  1
#                                  2
#                                  3
#                                  4
#                                  все