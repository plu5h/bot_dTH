import threading
from scripts import GUI
from scripts import imageprocessing
from scripts import actions


class Manager():
    def __init__(self, controller):
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
        while True and not self.stop :
            if self.State == 1 :
                try :
                    indice=imageprocessing.findIndice()
                    if(indice.split(' ')[0] == 'Phorreur'):
                        #TODO hold z to check phorreur name while going forward

                        self.State=3
                        print('Phorreur')
                        self.gui.UpdateText("Phorreur detected, take control")
                        continue
                    direction=imageprocessing.findDirection()
                    if self.firstIndice:
                        coords=actions.scrapCoord()
                        actions.enterCoord(coords)
                        self.firstIndice=False
                    actions.clickDirection(direction)
                    actions.enterIndice(indice)
                    actions.pasteTravel()
                    actions.clickOn(actions.pics_dict["coordCenter"])
                    actions.waitForArrival()


                        
                except:
                    pass
                

    def RunLoop(self):
        return (self.c.State == 2)
    