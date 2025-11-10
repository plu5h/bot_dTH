from PIL import ImageGrab
from PIL import Image
import json
import pyautogui as pg
import pytesseract
import cv2
import unidecode
import time
import numpy as np

import imageprocessing
import actions



pg.FAILSAFE = False
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

CONFIDENCE = 0.8

with open("./src/util/pics_dict.json") as json_file:
    pics_dict = json.load(json_file)

with open('./src/util/indicesDictionnary.json') as json_file:  

    
    indicesDictionnary = json.load(json_file)


#actions.pasteTravel()
#actions.clickOn(actions.pics_dict["coordCenter"])
actions.waitForArrival()



