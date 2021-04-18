#! /usr/bin/env python3

"""  
FileName: server.py
Author: John Delgado
Created Date: 3/6/2021
Version: 1.0 Initial Development

This is the main executeable file for the server
"""
from functions import get_config as gc
from functions import extract_frames as ef
from os import write
import sys
import os
import threading
import queue


if __name__ == '__main__':
    print("Starting Video Player.....")
    print("Reading configuration file...")

    config = gc.get_config()
    print("Configuration file successfully read")

    # inialize variables from config file
    buffer_size = config["bufferSettings"]["size"]

    # initialize queue
    work_queue = queue.Queue(buffer_size)

    # initialize thread counters
    producer_thread_counter = 1

    # while 1:
    print("Starting Producer Thread")
    thread_name = "Producer-thread-{}".format(producer_thread_counter)
    frame_producer_thread = ef.FrameProducerThread(
        producer_thread_counter, thread_name, work_queue)
    frame_producer_thread.start()

    # wait for the queue to empty
    # while not work_queue.empty():
    #    pass

    # Wait for all threads to complete
    # for thread in in_transfer_threads:
    #    thread.join()

    print("all threads completed!")

    # process_message(in_transfer_threads,conn,addr)
