#!/usr/bin/env python 
from threading import Timer
import time

timer_interval = 1


def delayrun():
    print 'running'

while True:
    time.sleep(5)
    print 'main running'
    delayrun()
