#! /usr/bin/env python3

import cv2
import numpy as np
import base64
import queue
from threading import *

class Queue:
    def __init__(self):
        self.buff = []
        self.lock = Lock()
        self.empty = Semaphore(24)
        self.full = Semaphore(0)

    def insert(self, i):
        self.empty.acquire()
        self.lock.acquire()
        self.buff.append(i)
        self.lock.release()
        self.full.release()

    def remove(self):
        self.full.acquire()
        self.lock.acquire()
        i = self.buff.pop(0)
        self.lock.release()
        self.empty.release()
        return i
    
# extraction and conversion queue
extract_convert = Queue()
# conversion and display queue
convert_display = Queue()
    
def extractFrames(filename, maxFrames):
    global extract_convert
    # Initialize frame count 
    count = 0
    # open video file
    vidcap = cv2.VideoCapture(filename)
    # read first image
    success,image = vidcap.read()
    while success and count < maxFrames:
        # add the frame to the buffer
        extract_convert.insert(image)
        success,image = vidcap.read()
        print(f'Reading frame {count} {success}')
        count += 1
    extract_convert.insert(None)
    print('Frame extraction complete')

def convertFrames():
    global extract_convert
    global convert_display
    # initialize frame count
    count = 0
    # go through each frame in the buffer until the buffer is empty
    while True:
        # get the next frame
        frame = extract_convert.remove()
        if(frame is None):
            convert_display.insert(None)
            break
        grayscaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        print(f'Converting to grayscale {count}')
        convert_display.insert(grayscaleFrame)
        count += 1
    print('Grayscale conversion complete')

def displayFrames():
    global convert_display
    # initialize frame count
    count = 0
    # go through each frame in the buffer until the buffer is empty
    while True:
        # get the next frame
        frame = convert_display.remove()
        if(frame is None):
            break
        print(f'Displaying frame {count}')        
        # display the image in a window called "video" and wait 42ms
        cv2.imshow('Video', frame)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break
        count += 1
    print('Finished displaying all frames')
    cv2.destroyAllWindows()
