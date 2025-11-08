import pyautogui as pg
import time
import pytesseract
import numpy as np
import cv2
import random
from PIL import ImageGrab

from src.scripts.actions import *

keepGoing=True
first=True
coords:list[str]

while keepGoing:
    if first: 
        print('5 secondes pour AltTab sur Dofus')
        time.sleep(5)
    try:
        time.sleep(1)
        indice=findIndice()
        if(indice.split(' ')[0] == 'Phorreur'):
            keepGoing=False
            print('Phorreur')
            pg.keyDown('alt')
            pg.press('tab')
            pg.press('tab')
            pg.keyUp('alt')
            break
        direction=findDirection()
        if first:
            coords=scrapCoord()
            altTab()
            print("first")
            enterCoord(coords)
        else:altTab()
        clickDirection(direction)
        enterIndice(indice)
        distance=findDistance()
        altTab()
        for i in range(int(distance)):
            time.sleep(0.5)
            coords=scrapCoord()     
            moveHeroDir(direction)
            timeout=time.time()+30
            while(comparePos(coords,scrapCoord())):
                if(time.time()>timeout):
                    print("impossible de passer à la carte suivante")
                    raise Exception()
        try:
            clickOn(flag)
            time.sleep(1)
        except:
            try:
                time.sleep(1)
                clickOn(flag2)
            except:
                keepGoing=False
                print('proutezer')
                break
    except Exception as err:
        keepGoing=False
        print('General quit: ', err)
        pg.keyDown('alt')
        pg.press('tab')
        pg.press('tab')
        pg.keyUp('alt')
        break
    first=False
