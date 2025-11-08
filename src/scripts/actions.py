import pyautogui as pg
import time
import pytesseract
import numpy as np
import cv2
import random
import imagehash
import json
import unidecode
from PIL import ImageGrab
from PIL import Image

pg.FAILSAFE = False
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

MOVESPEED = 0.3
CONFIDENCE = 0.8
flag = "res/flag.png"
flag2 = "res/flag2.png"
coordX = "res/coordX.png"
coordY = "res/coordY.png"
indiceField = "res/indice.png"
nextIndice = "res/nextIndice.png"
buttonUp = "res/buttonUp.png"
buttonDown = "res/buttonDown.png"
buttonLeft = "res/buttonLeft.png"
buttonRight = "res/buttonRight.png"

with open('indicesDictionnary.json') as json_file:
    indicesDictionnary = json.load(json_file)


curLine = 1
curPos = [0, 0]


def getText(cap):
    text = pytesseract.image_to_string(
        cv2.cvtColor(np.array(cap), cv2.COLOR_BGR2GRAY),
        config="--psm 10")
    return text


def clickOn(name):
    pos = pg.locateCenterOnScreen(name, confidence=CONFIDENCE)
    pg.moveTo(pos[0], pos[1], duration=MOVESPEED)
    pg.click()


def moveHeroDir(dir):
    if dir == 'left':
        pg.moveTo(1, random.randint(650, 750))
    elif dir == 'right':
        pg.moveTo(2559, random.randint(650, 750))
    elif dir == 'up':
        pg.moveTo(random.randint(1200, 1300), 1)
    elif dir == 'down':
        pg.moveTo(random.randint(1200, 1300), 1270)
    pg.click()


def altTab():
    pg.keyDown('alt')
    pg.press('tab')
    pg.keyUp('alt')


def findDirection():
    try:
        line = 0
        pos = pg.locateOnScreen(flag, confidence=CONFIDENCE)
        x1 = pos[0]-380
        y1 = pos[1]
        x2 = pos[0]-340
        y2 = pos[1]+pos[3]
        cap = ImageGrab.grab(bbox=(x1, y1, x2, y2)).convert('L')
        if (-10 < y1-199 < 10):
            line = 1
        if (-10 < y1-240 < 10):
            line = 2
        if (-10 < y1-281 < 10):
            line = 3
        if (-10 < y1-321 < 10):
            line = 4
        if (-10 < y1-363 < 10):
            line = 5
    except:
        pos = pg.locateOnScreen(flag2, confidence=CONFIDENCE)
        x1 = pos[0]-380
        y1 = pos[1]
        x2 = pos[0]-345
        y2 = pos[1]+pos[3]
        cap = ImageGrab.grab(bbox=(x1, y1, x2, y2)).convert('L')
        cap.save("6right.png")
        line = 6
    

    
    up = "res/"+str(line)+"up.png"
    down = "res/"+str(line)+"down.png"
    right = "res/"+str(line)+"right.png"
    left = "res/"+str(line)+"left.png"


    hashCap = imagehash.average_hash(cap)
    hashes = {
        "up": hashCap-imagehash.average_hash(Image.open(up)),
        "down": hashCap-imagehash.average_hash(Image.open(down)),
        "right": hashCap-imagehash.average_hash(Image.open(right)),
        "left": hashCap-imagehash.average_hash(Image.open(left))}


    res = min(hashes, key=hashes.get)
    return res


def clickDirection(dir):
    if (dir == "up"):
        clickOn(buttonUp)
    if (dir == "down"):
        clickOn(buttonDown)
    if (dir == "right"):
        clickOn(buttonRight)
    if (dir == "left"):
        clickOn(buttonLeft)


def findIndice():
    try:
        pos = pg.locateOnScreen(flag, confidence=CONFIDENCE)
        x1 = pos[0]-343
        y1 = pos[1]
        x2 = pos[0]
        y2 = pos[1]+pos[3]
        cap = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        res = unidecode.unidecode(str(getText(cap)))

        if res in indicesDictionnary:
            print("crottteeeee")
            res = indicesDictionnary[res]
        return res
    except:
        # flag en bas de la page different logo
        try:
            pos = pg.locateOnScreen(flag2, confidence=CONFIDENCE)
            x1 = pos[0]-343
            y1 = pos[1]
            x2 = pos[0]
            y2 = pos[1]+pos[3]
            cap = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            res = unidecode.unidecode(str(getText(cap)))
            if res in indicesDictionnary:
                res = indicesDictionnary[res]
            return res
        except:
            try:
                clickOn(nextIndice)
                time.sleep(2)
                return findIndice()
            except:
                return "proute"


def enterIndice(indiceName):
    clickOn(indiceField)
    pressText(indiceName)
    pg.move(0, 25)
    time.sleep(1)
    pg.click()


def findDistance():
    time.sleep(1)
    cap = ImageGrab.grab(bbox=(1287, 646, 1346, 690))
    goal = getText(cap)
    return goal


def scrapCoord():
    cap = ImageGrab.grab(bbox=(19, 65, 145, 112))
    res = getText(cap).split(',')[:2]
    return res


def enterCoord(coords):
    try:
        clickOn(coordX)
        pg.keyDown('ctrl')
        pg.press('a')
        pg.keyUp('ctrl')
        pressText(coords[0])
        clickOn(coordY)
        pg.keyDown('ctrl')
        pg.press('a')
        pg.keyUp('ctrl')
        pressText(coords[1])
    except:
        print("no coords")


def pressText(s):
    for i in s:
        pg.press(i)


def waitUntil(somepredicate, timeout, period=0.1, *args, **kwargs):
    mustend = time.time() + timeout
    while time.time() < mustend:
        if somepredicate(*args, **kwargs):
            return True
        time.sleep(period)
    return False


def comparePos(pos1, pos2):
    for i in range(0, len(pos1)):
        if (pos1[i] != pos2[i]):
            return False
    return True
