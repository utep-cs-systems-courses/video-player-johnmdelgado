#!/usr/bin/env python3
"""  
FileName: display_frames.py
Author: John Delgado
Created Date: 4/17/2021
Version: 1.0 Initial Development

This is going handle displaying the frames
"""

import cv2
import os
import time
import threading
import numpy as np
from functions import get_config as mc


class GrayscaleFrameConsumerThread(threading.Thread):
    def __init__(self, threadID, name, grayscaleQueue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.grayscaleQueue = grayscaleQueue

    def run(self):
        print("Starting " + self.name)
        if not self.grayscaleQueue.full():
            print("Queue is not full, Extracting frames to be displayed.")
            displayFrames(self.name, self.grayscaleQueue)
        else:
            print("Queue is full. Sleeping for a 2 seconds")
            time.sleep(2)
        return


def displayFrames(threadName, grayscaleQueue):
    # read in config file
    config = mc.get_config()
    # globals
    outputDir = config["defaults"]["outputFramesDirectory"]
    frameDelay = config["playback"]["frameDelay"]
    debug = config["debugging"]["debug"]

    # initialize frame count
    count = 0

    # get the next frame file name from our working queue
    in_file_name = grayscaleQueue.get()

    # load the frame
    frame = cv2.imread(in_file_name)

    while frame is not None:

        print(f'{threadName}: Displaying frame {count}')
        # Display the frame in a window called "Video"
        cv2.imshow('Video', frame)

        # Wait for 42 ms and check if the user wants to quit
        if cv2.waitKey(frameDelay) and 0xFF == ord("q"):
            break

        # get the next frame filename
        count += 1
        in_file_name = grayscaleQueue.get()

        # Read the next frame file
        frame = cv2.imread(in_file_name)

    # make sure we cleanup the windows, otherwise we might end up with a mess
    cv2.destroyAllWindows()
