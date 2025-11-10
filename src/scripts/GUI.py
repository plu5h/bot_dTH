from tkinter import *

class gui :
    def __init__(self):
        self.fen = Tk()
        self.fen.title("Treasure Hunt Autofarm")
        self.fen.geometry("300x50")
        self.mt = StringVar()
        self.mt.set("Farming...")
        self.txt = Label(self.fen, textvariable=self.mt)

        quitLabel = Label(self.fen, text="Press CTRL to kill")

        self.txt.pack()
        quitLabel.pack()

    def start(self) :
        self.fen.mainloop()
        
    def UpdateText(self, text):
        self.mt.set(text)
        self.SetTop()
    
    def SetTop(self):
        self.fen.attributes("-topmost", True)
        self.fen.attributes("-topmost", False)

    def Kill(self):
        self.fen.destroy()