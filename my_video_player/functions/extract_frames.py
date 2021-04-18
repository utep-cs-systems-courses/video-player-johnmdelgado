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
        if not self.queue.full():
            print("Queue is not full, Extracting frames to be consumed.")
            extractFrames(self.name, self.queue)
        else:
            print("Queue is full. Sleeping for a 2 seconds")
            time.sleep(2)
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

    print("reading frame")
    # read one frame
    success, frame = vidcap.read()
    print("success is: {}".format(success))
    print("frame is: {}".format(frame))

    print(f'Reading frame {count} {success}')
    while success and count < 72:

        # write the current frame out as a jpeg image
        output_file = f"{outputDir}/frame_{count:04d}.bmp", frame
        cv2.imwrite(output_file)
        print("Adding frame to the queue to be consumed")
        queue.put(output_file)

    success, frame = vidcap.read()
    print(f'Reading frame {count}')
    count += 1
