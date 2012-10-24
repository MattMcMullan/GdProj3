from direct.gui.DirectGui import *
import sys

class Menu():
    def __init__(self, parent):
        
        self.startButton = DirectButton(image = "start01 - on.png", image_scale = (.8, 1, .14), image_pos = (0, 0, .6), relief = None, command = self.clicked)
        self.gameStart = 0
        
    def clicked(self):
        print "click!"
        self.gameStart = 1