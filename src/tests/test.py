import pyautogui as pg
import time
import pytesseract
import numpy as np
import cv2
from PIL import ImageGrab

from src.scripts.actions import *

flag="res/flag.png"
coordX="res/coordX.png"
coordY="res/coordY.png"



def findTruc():
    cap = ImageGrab.grab(bbox =(1287, 646, 1346, 690))
    goal=getText(cap)
    return goal

#print(findTruc())
#print(Main.findRoute("right"))
#print(pg.position())
print(findIndice())
print(findDirection())