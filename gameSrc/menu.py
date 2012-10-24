from direct.gui.DirectGui import *
import sys

class Menu():
    def __init__(self, parent):
        
        self.startButton = DirectButton(image = "start01 - off.png", image_scale = (1, 1, .2), relief = None, command = self.clicked)
        self.gameStart = 0
        
    def clicked(self):
        print "click!"
        self.gameStart = 1