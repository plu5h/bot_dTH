from PIL import ImageGrab
from PIL import Image
import json
import pyautogui as pg
import pytesseract
import cv2
import unidecode
import time
import numpy as np
import win32clipboard


from pynput.keyboard import Key, Controller
from scripts import imageprocessing
from scripts import actions


keyboard=Controller()

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

CONFIDENCE = 0.8

with open("./src/util/pics_dict.json") as json_file:
    pics_dict = json.load(json_file)

with open('./src/util/indicesDictionnary.json') as json_file:  

    
    indicesDictionnary = json.load(json_file)


print(imageprocessing.scrapCoord())