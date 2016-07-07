#coding=utf-8

age = 8
if age==8:
    print age
elif age>8:
    print ">8"

#只要x是非零数值、非空字符串、非空list等，就判断为True，否则为False
x = 0
x = ['aaa']
if x:
    print "true"

names = [1,2,3]
for name in names:
    print name

for x in range(1,10):
    print x

# raw input 进来的数据永远是string，需要强制转化为int
birth = int(raw_input('birth: '))

