#!/usr/bin/env python3
"""  
FileName: custom_queue.py
Author: John Delgado
Created Date: 5/4/2021
Version: 1.0 Initial Development

This is our custom queue using semaphores!! 
Also, May the 4th be with you. 
"""

from threading import *


class CustomQueue:
    def __init__(self):
        self.buff = list()
        # starts at 0 since buff is empty
        self.full = Semaphore(0)
        # starts at 10 since we only want to hold 10 frames
        self.empty = Semaphore(10)

    # insert into end of the "queue", will block if buff has 10 frames
    def put(self, item):
        # decrement empty semaphore since we are filling buff
        self.empty.acquire()
        # append frame to the end of the buffer
        self.buff.append(item)
        # increment full since we just took a spot
        self.full.release()
     # remove from the front of the "queue", will block while empty

    def get(self):
        # decrement full semaphore since we are removing from buff
        self.full.acquire()
        # remove frame from the front of buff
        item = self.buff.pop(0)
        # increment empty since we just opened a spot
        self.empty.release()
        return item
