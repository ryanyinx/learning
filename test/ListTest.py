#coding=utf-8

#tuple, once defined could not be changed
classmates = ('aaa', 'bbb')
print classmates
print classmates[0]
print classmates[-1]

tuple = (1)
print tuple
tuple = (1,)
print tuple
print tuple[0]

changeTuple = (1,2,[1,2])
changeTuple[2][0] = 3
changeTuple[2][1] = 4
print changeTuple

