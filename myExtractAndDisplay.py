#! /usr/bin/env python3
# Manuel Ruvalcaba
# April 20, 2021
# Theory of Operating Systems
# Dr. Freudenthal
# Video Player: This program extracts frames from a file, converts them to grayscale, and displays them on the screen, using Producer/Consumer threads and counting semaphores.

import myVideoHelper
from threading import *

threadNum = 0

class Extractor(Thread):
    def __init__(self, filename, maxFrames):
        global threadNum
        Thread.__init__(self, name="Thread-%d" % threadNum);
        threadNum += 1
        self.filename = filename
        self.maxFrames = maxFrames
    def run(self):
        myVideoHelper.extractFrames(self.filename, self.maxFrames)

class Grayscale(Thread):
    def __init__(self):
        global threadNum
        Thread.__init__(self, name="Thread-%d" % threadNum);
        threadNum += 1
    def run(self):
        myVideoHelper.convertFrames()
        
class Display(Thread):
    def __init__(self):
        global threadNum
        Thread.__init__(self, name="Thread-%d" % threadNum);
        threadNum += 1
    def run(self):
        myVideoHelper.displayFrames()

if __name__ == "__main__":
    
    # Thread to extract the frames
    Extractor('clip.mp4', 72).start()
    # Thread to convert the frames
    Grayscale().start()
    # Thread to display the frames
    Display().start()
