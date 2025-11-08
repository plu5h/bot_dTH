from PIL import ImageGrab
from PIL import Image
import json
import pyautogui as pg
import pytesseract
import cv2
import unidecode
import time
import numpy as np

pg.FAILSAFE = False
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

CONFIDENCE = 0.8

with open("./src/util/pics_dict.json") as json_file:
    pics_dict = json.load(json_file)

with open('./src/util/indicesDictionnary.json') as json_file:
    indicesDictionnary = json.load(json_file)

#I use "Départ" and "en cours" to find the x axis value at which the indice is starting and ending
indiceX1=pg.locateOnScreen(pics_dict["depart"]).left
indiceX2=pg.locateOnScreen(pics_dict["encours"]).left

def findIndice():
    try:
        pos = pg.locateOnScreen(pics_dict["flag"])
        y1 = pos[1]
        y2 = pos[1]+pos[3]
        cap = ImageGrab.grab(bbox=(indiceX1, y1, indiceX2, y2))
        res = unidecode.unidecode(str(getText(cap)))
        

        if res in indicesDictionnary:
            res = indicesDictionnary[res]
        return res
    except: pass

def getText(cap):
    text = pytesseract.image_to_string(
        cv2.cvtColor(np.array(cap), cv2.COLOR_BGR2GRAY),
        config="--psm 10")
    return text


print(findIndice())