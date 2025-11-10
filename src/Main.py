import threading
import traceback
import logging
import time
from scripts import GUI
from scripts import imageprocessing
from scripts import actions


class Manager():
    def __init__(self):
        self.stop = False
        self.state = 1
        self.sleepTime = 0.1
        self.firstIndice = True

    def __del__(self):
        self.stop = True
        self.mainthread.join()

    def Shutdown(self):
        self.c.__del__()
        self.__del__()
        self.gui.Kill()

    def setGUI(self, gui):
        self.gui = gui

    def RunThread(self):
        self.mainthread = threading.Thread(target=self.Hunt)
        self.mainthread.start()

#states: 
#0 : tp to hunt and launch it then tp to begining (and walk to it if needed)
#1 : do the hunt
#2 : fight
#3 : stop


    def Hunt(self):
        print("starting loop")
        while True and not self.stop :
            if self.state == 1 :
                
                try :
                    indice=imageprocessing.findIndice()
                    print (indice)
                    if(indice.split(' ')[0] == 'Phorreur'):
                        #TODO hold z to check phorreur name while going forward

                        self.State=3
                        print('Phorreur')
                        self.gui.UpdateText("Phorreur detected, take control")
                        continue
                    direction=imageprocessing.findDirection()
                    print(direction)
                    if self.firstIndice :
                        coords=imageprocessing.scrapCoord()
                        actions.enterCoord(coords)
                        self.firstIndice=False
                    actions.clickDirection(direction)
                    actions.enterIndice(indice)
                    actions.pasteTravel()
                    actions.clickOn("coordCenter")
                    actions.waitForArrival()
                    
                    actions.clickOn("flag", confidence=0.99)
                    time.sleep(0.5)
                    try:
                        if imageprocessing.isElementOnScreen("flag", confidence = 0.99):
                            print("tjrs un flag")
                            pass
                        else:
                            print("noflag")
                            actions.clickOn("validerEtape")
                    except:
                        try:
                            actions.clickOn("validerEtape")
                        except Exception as e:
                            self.stop=True
                            logging.error(traceback.format_exc())

                    time.sleep(1)


                        
                except Exception as e:
                    self.stop=True
                    logging.error(traceback.format_exc())
                    
                    
                


#---------------MAIN----------------

if __name__ == "__main__":
    print("launch")
    m = Manager()
    m.RunThread()
    mainGUI = GUI.gui()
    m.setGUI(mainGUI)
    mainGUI.start()