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
import logging
import traceback
import unidecode
import pytesseract

#-----------VARS-----------------------


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


with open("./src/util/pics_dict.json") as json_file:
    pics_dict = json.load(json_file)

with open('./src/util/indicesDictionnary.json') as json_file:
    indicesDictionnary = json.load(json_file)


CONFIDENCE = 0.8

#-------------FUNCTIONS-----------------

def findDirection():
    sure = False
    while not sure:
        depart = pg.locateOnScreen(pics_dict["depart"])
        pos = pg.locateOnScreen(pics_dict["flag"], confidence = 0.99)
        cap = ImageGrab.grab(bbox=(depart.left-20, pos.top, depart.left, pos.top+pos.height)).convert('L')
        
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

def isElementOnScreen(elt, confidence = CONFIDENCE):
    seen = False
    try:
        if elt in ("flag", "flagChecked"):
            depart = pg.locateOnScreen(pics_dict["depart"])
            pos = pg.locateOnScreen(pics_dict[elt],confidence=confidence, region =(depart.left, depart.top,500, 500))
        else:
            pos = pg.locateOnScreen(pics_dict[elt],confidence=confidence)
        if(pos) :
            seen = True
    except:
        pass

    return seen

def isLastEtape():
    try:
        pos = pg.locateOnScreen(pics_dict["etape"])
        cap = ImageGrab.grab(bbox=(pos.left+pos.width, pos.top, pos.left+pos.width+100, pos.top+pos.height))
        txt = getText(cap).replace('\n',"").split('/')
        res = (int(txt[1])-int(txt[0])==0)
        return res
    except Exception as e:
        logging.error(traceback.format_exc())
    
    return

def findIndice():
    try:
        pos = pg.locateOnScreen(pics_dict["flag"], confidence=0.99)
        y1 = pos[1]
        y2 = pos[1]+pos[3]
        depart = pg.locateOnScreen(pics_dict["depart"])
        encours=pg.locateOnScreen(pics_dict["encours"])
        cap = ImageGrab.grab(bbox=(depart.left, y1, encours.left, y2))
        res = unidecode.unidecode(str(getText(cap))).replace("4","a")
        

        if res in indicesDictionnary:
            res = indicesDictionnary[res]
        return res
    except Exception as e:
        logging.error(traceback.format_exc())

def getText(cap):
    text = pytesseract.image_to_string(
        cv2.cvtColor(np.array(cap), cv2.COLOR_BGR2GRAY),
        config="--psm 10")
    return text

def scrapCoord():
    
    pos = pg.locateOnScreen(pics_dict["bonusXPLogo"], confidence=CONFIDENCE)
    cap = ImageGrab.grab(bbox=(0, pos.top, pos.left, pos.top+pos.height))
    cap.save("./res/tmp.png")
    txt = getText(cap)
    
    res=txt.split('- Niv')[0].replace(" ","").split(',')

    return res

def checkPhorreur():
    pos = pg.locateCenterOnScreen(pics_dict["YButton"])
    pg.moveTo(pos[0]+30, pos[1])
    pg.mouseDown(button='left')
    time.sleep(5)
    if isElementOnScreen("phorreurName"):
        res = True
    else :
        res = False
    pg.mouseUp(button='left')
    return res