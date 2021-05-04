#!/usr/bin/env python3

import cv2
import os
import time
import threading
import numpy as np
from functions import get_config as mc


class FrameProducerThread(threading.Thread):
    def __init__(self, threadID, name, queue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.queue = queue

    def run(self):
        print("Starting " + self.name)
        extractFrames(self.name, self.queue)
        return


def extractFrames(threadName, queue):
    # read in config file
    config = mc.get_config()
    # set globals
    outputDir = config["defaults"]["outputFramesDirectory"]
    clipFilePath = config["defaults"]["clipFilePath"]
    debug = config["debugging"]["debug"]

    # initialize frame count
    count = 0

    print("opening the video clip from: {}".format(clipFilePath))
    # open the video clip
    vidcap = cv2.VideoCapture(clipFilePath)

    # create the output directory if it doesn't exist
    if not os.path.exists(outputDir):
        print(f"Output directory {outputDir} didn't exist, creating")
        os.makedirs(outputDir)

    print("{}: reading frame".format(threadName))
    # read one frame
    success, frame = vidcap.read()
    print("{}: success is: {}".format(threadName, success))

    print(f'Reading frame {count} {success}')
    while success:  # and count < 72:

        # write the current frame out as a jpeg image
        output_file = f"{outputDir}/frame_{count:04d}.bmp"
        cv2.imwrite(output_file, frame)
        print("{}: Adding frame to the queue to be consumed".format(threadName))
        queue.put(output_file)
        success, frame = vidcap.read()
        print("{}: Reading frame {}".format(threadName, count))
        count += 1
