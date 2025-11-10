import pip
import time
import json
import numpy as np
import pyautogui as pg
import cv2
import imagehash
import hashlib
from PIL import ImageGrab
from PIL import Image
from PIL import ImageChops
import unidecode
import pytesseract

#-----------VARS-----------------------

pg.FAILSAFE = False
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


with open("./src/util/pics_dict.json") as json_file:
    pics_dict = json.load(json_file)

with open('./src/util/indicesDictionnary.json') as json_file:
    indicesDictionnary = json.load(json_file)

#I use "Départ" and "en cours" to find the x axis value at which the indice is starting and ending
try:
    indiceX1=pg.locateOnScreen(pics_dict["depart"]).left
    indiceX2=pg.locateOnScreen(pics_dict["encours"]).left
except:
    print("Départ or En Cours can't be found")
    
CONFIDENCE = 0.8

#-------------FUNCTIONS-----------------

def findDirection():
    sure = False
    while not sure:
        pos = pg.locateOnScreen(pics_dict["flag"])
        cap = ImageGrab.grab(bbox=(indiceX1-20, pos.top, indiceX1, pos.top+pos.height)).convert('L')
        
        hashCap = imagehash.average_hash(cap)
        hashes =  {
            "Up": hashCap-imagehash.average_hash(Image.open(pics_dict["arrowUp"])),
            "Down": hashCap-imagehash.average_hash(Image.open(pics_dict["arrowDown"])),
            "Right": hashCap-imagehash.average_hash(Image.open(pics_dict["arrowRight"])),
            "Left": hashCap-imagehash.average_hash(Image.open(pics_dict["arrowLeft"]))
        }

        if min(hashes.values()) <=1:
            res= min(hashes, key=hashes.get)
            sure=True
    

    return res


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

def scrapCoord():
    pos = pg.locateOnScreen(pics_dict["depart"], confidence=CONFIDENCE)
    cap = ImageGrab.grab(bbox=(pos.left+pos.width, pos.top, pos.left+pos.width+100, pos.top+pos.height))
    res = getText(cap).replace("[","").replace("]","").replace("\n","").split(',')[:2]
    return res