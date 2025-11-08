import pip
import time

try :
    import numpy as np
except :
    print("numpy not found, importing ...")
    pip.main(['install', 'numpy'])
    import numpy as np

try :
    import pyautogui as pg
except :
    print("pyautogui not found, importing ...")
    pip.main(['install', 'pyautogui'])
    import pyautogui as pg

try :
    import cv2
except :
    print("cv2 not found, importing ...")
    pip.main(['install', 'cv2'])
    import cv2



