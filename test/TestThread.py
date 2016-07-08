#encoding=utf-8

import time
import threading
import multiprocessing

def loop():
    print 'thread %s is running...' % threading.current_thread().name
    n = 0
    while n < 5:
        n = n + 1
        print 'thread %s >>> %s' % (threading.current_thread().name, n)
        time.sleep(1)
    print 'thread %s ended.' % threading.current_thread().name

balance = 0
def changeBalance(a):
    global balance
    balance

def deadCycle():
    x = 0
    while True:
        print threading.current_thread().name
        x = x^1

print 'thread %s is running...' % threading.current_thread().name
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print 'thread %s ended.' % threading.current_thread().name
