from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
import sys

#This is the start menu.
class Menu():
    def __init__(self, parent):
        self.parent = parent
        
        self.whichfrom = "" #For telling backClicked which menu it came from
        self.font = loader.loadFont("../assets/font/Orbitron Light.otf")
        self.back = OnscreenImage(image = "../assets/2d/title_bg01.png", pos = (0, 0, 0), scale=(1.4,1,1))
        self.startButton = DirectButton(image = "../assets/2d/buttons/start_on.png", image_scale = (.8, 1, .14), image_pos = (0, 0, .3), relief = None, command = self.startClicked)
        self.rulesButton = DirectButton(image = "../assets/2d/buttons/rules_on.png", image_scale = (.8, 1, .14), image_pos = (0, 0, -.05), relief = None, command = self.rulesClicked)
        self.optButton = DirectButton(image = "../assets/2d/buttons/opt_on.png", image_scale = (.8, 1, .14), image_pos = (0, 0, -.4), relief = None, command = self.optClicked)
        self.exitButton = DirectButton(image = "../assets/2d/buttons/exit_on.png", image_scale = (.8, 1, .14), image_pos = (0, 0, -.75), relief = None, command = self.exitClicked)

    def startClicked(self):
        self.startButton.destroy()
        self.rulesButton.destroy()
        self.optButton.destroy()
        self.exitButton.destroy()
        self.back.destroy()
        self.parent.beginGame() #This will make the rest of the game happen!
        
    def rulesClicked(self):
        self.startButton.destroy()
        self.rulesButton.destroy()
        self.optButton.destroy()
        self.exitButton.destroy()
        self.back.destroy()
        self.back = OnscreenImage(image = "../assets/2d/title_bg02.png", pos = (0, 0, 0), scale=(1.4,1,1))
        self.line1 = OnscreenText(text = "Defeat enemy players by pushing them into the arena wall!", fg = (0,1,1,1), pos = (0, .8), scale = .07, font = self.font)
        self.line2 = OnscreenText(text = "Use traps to snag them, and throw balls to push them!", fg = (0,1,1,1), pos = (0, .6), scale = .07, font = self.font)
        self.line3 = OnscreenText(text = "Controls:", fg = (0,1,1,1), pos = (0, .4), scale = .1, font = self.font)
        self.line4 = OnscreenText(text = "Left Click: Throw Ball/Place Trap", fg = (0,1,1,1), pos = (0, .2), scale = .07, font = self.font)
        self.line5 = OnscreenText(text = "Scroll: Select Item", fg = (0,1,1,1), pos = (0, 0), scale = .07, font = self.font)
        self.line6 = OnscreenText(text = "W/S: Jet Forward/Backward", fg = (0,1,1,1), pos = (0, -.2), scale = .07, font = self.font)
        self.line7 = OnscreenText(text = "The more hits you take, the greater your momentum!", fg = (0,1,1,1), pos = (0, -.6), scale = .07, font = self.font)
        self.whichfrom = "rules"
        self.backButton = DirectButton(image = "../assets/2d/buttons/back_on.png", image_scale = (.4,1,.1), image_pos = (-.9, 0, -.87), relief = None, command = self.backClicked)
        
    def optClicked(self):
        print "options click!"
        
    def backClicked(self):
        self.backButton.destroy()
        self.back.destroy()
        if self.whichfrom == "rules":
            self.line1.destroy()
            self.line2.destroy()
            self.line3.destroy()
            self.line4.destroy()
            self.line5.destroy()
            self.line6.destroy()
            self.line7.destroy()
        self.__init__(self.parent) #Redoes the menu
        
    def exitClicked(self):
        sys.exit()