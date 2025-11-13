import threading
import traceback
import logging
import time
from pynput.keyboard import Listener as keylistener, Key
from scripts import GUI
from scripts import imageprocessing
from scripts import actions


class Manager():
    def __init__(self):
        self.stop = False
        self.state = 1
        self.sleepTime = 0.1
        self.keylistener = keylistener(on_press=self.on_press)
        self.keylistener.start()
        self.doFight = True

    def __del__(self):
        self.stop = True
        self.mainthread.join()

    def Shutdown(self):
        self.__del__()
        self.gui.Kill()

    def setGUI(self, gui):
        self.gui = gui

    def RunThread(self):
        self.mainthread = threading.Thread(target=self.Hunt)
        self.mainthread.start()

    def on_press(self,key):
        if key == Key.esc :
            print("pressed")
            self.Shutdown()

#states: 
#0 : tp to hunt and launch it then tp to begining (and walk to it if needed)
#1 : do the hunt
#2 : fight
#3 : stop


    def Hunt(self):
        print("starting loop")
        firstIndice=True
        actions.focusDofusWindow()
        while True and not self.stop :
            
            if self.state == 1 :

                if not imageprocessing.isLastEtape():

                    try :
                        
                        indice=imageprocessing.findIndice()
                        print (indice)
                        
                        direction=imageprocessing.findDirection()
                        print(direction)

                        if(indice.split(' ')[0] == 'Phorreur'):
                            
                            print('Phorreur')
                            actions.reachPhorreur(direction)
                            firstIndice=True

                        else:

                            if firstIndice :
                                coords=imageprocessing.scrapCoord()
                                print(coords)
                                actions.enterCoord(coords)
                                firstIndice=False
                            actions.clickDirection(direction)
                            actions.enterIndice(indice)

                            #checkpoint if we have to kill the script
                            if self.stop : 
                                continue

                            actions.pasteTravel()
                            actions.clickOn("coordCenter")
                            actions.waitForArrival()
                        
                        if self.stop : 
                            continue

                        actions.clickOn("flag", confidence=0.99)
                        time.sleep(0.5)
                        try:
                            if imageprocessing.isElementOnScreen("flag", confidence = 0.99):
                                pass
                            else:
                                actions.clickOn("validerEtape")
                        except:
                            try:
                                actions.clickOn("validerEtape")
                            except Exception as e:
                                print("stopping")
                                self.stop=True
                                logging.error(traceback.format_exc())

                        time.sleep(1)


                            
                    except Exception as e:
                        print("stopping2")
                        self.stop=True
                        logging.error(traceback.format_exc())
                else :
                    actions.clickOn("combat")
                    self.clickOn("pret")
                    self.state=2
                    
            if self.state==2 and self.doFight:
                if(imageprocessing.isElementOnScreen("sorts")):
                    actions.takeCombatTurn()

        print("end of loop")   
        print(self.stop)      
        self.Shutdown()   
                    
                


#---------------MAIN----------------

if __name__ == "__main__":
    print("launch")
    m = Manager()
    m.RunThread()
    mainGUI = GUI.gui()
    m.setGUI(mainGUI)
    mainGUI.start()