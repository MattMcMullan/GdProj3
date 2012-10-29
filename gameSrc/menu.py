from direct.gui.DirectGui import *
import sys

class Menu():
    global gameStart
    def __init__(self, parent):
        
        self.parent = parent
        
        self.startButton = DirectButton(image = "start_on.png", image_scale = (.8, 1, .14), image_pos = (0, 0, .4), relief = None, command = self.startClicked)
        self.rulesButton = DirectButton(image = "rules_on.png", image_scale = (.8, 1, .14), image_pos = (0, 0, 0), relief = None, command = self.rulesClicked)
        self.optButton = DirectButton(image = "opt_on.png", image_scale = (.8, 1, .14), image_pos = (0, 0, -.4), relief = None, command = self.optClicked)
        self.exitButton = DirectButton(image = "exit_on.png", image_scale = (.8, 1, .14), image_pos = (0, 0, -.8), relief = None, command = self.exitClicked)

    def startClicked(self):
        self.startButton.destroy()
        self.rulesButton.destroy()
        self.optButton.destroy()
        self.exitButton.destroy()
        self.parent.beginGame()
        
    def rulesClicked(self):
        self.startButton.destroy()
        self.rulesButton.destroy()
        self.optButton.destroy()
        self.exitButton.destroy()
        
    def optClicked(self):
        print "options click!"
        
    def exitClicked(self):
        sys.exit()
        