#!/usr/bin/env python3

import cv2
import cv2
import os
import time
import threading
import numpy as np
from functions import get_config as mc


class FrameConsumerThread(threading.Thread):
    def __init__(self, threadID, name, workQueue, convertedQueue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.workQueue = workQueue
        self.convertedQueue = convertedQueue

    def run(self):
        print("Starting " + self.name)
        if not self.convertedQueue.full():
            print("Queue is not full, Extracting frames to be consumed.")
            ConvertToGrayscale(self.name, self.workQueue, self.convertedQueue)
        else:
            print("Queue is full. Sleeping for a 2 seconds")
            time.sleep(2)
        return


def ConvertToGrayscale(threadName, workQueue, convertedQueue):
    # read in config file
    config = mc.get_config()
    # globals
    outputDir = config["defaults"]["outputFramesDirectory"]

    # initialize frame count
    count = 0

    # get the next frame file name from our working queue
    in_file_name = workQueue.get()
    #inFileName = f'{outputDir}/frame_{count:04d}.bmp'

    print("{}: Converting file: {} to grayscale".format(threadName, in_file_name))
    # load the next file
    inputFrame = cv2.imread(in_file_name, cv2.IMREAD_COLOR)

    while inputFrame is not None and count < 72:
        print("{}: Converting frame {}".format(threadName, count))

        # convert the image to grayscale
        grayscale_frame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)

        # generate output file name
        out_file_name = f'{outputDir}/grayscale_{count:04d}.bmp'
        print(
            "{}: writing grayscale file and pushing to converted queue".format(threadName))
        # write output file
        cv2.imwrite(out_file_name, grayscale_frame)

        # add file to the converted queue to be consumed by the next extract processor
        convertedQueue.put(out_file_name)

        count += 1

        # generate input file name for the next frame
        in_file_name = workQueue.get()

        # load the next frame
        inputFrame = cv2.imread(in_file_name, cv2.IMREAD_COLOR)
