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


with open("./src/util/pics_dict.json") as json_file:
    pics_dict = json.load(json_file)

with open('./src/util/indicesDictionnary.json') as json_file:
    indicesDictionnary = json.load(json_file)


curLine = 1
curPos = [0, 0]





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



def clickDirection(dir):
    if (dir == "up"):
        clickOn(buttonUp)
    if (dir == "down"):
        clickOn(buttonDown)
    if (dir == "right"):
        clickOn(buttonRight)
    if (dir == "left"):
        clickOn(buttonLeft)



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
