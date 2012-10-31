from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.DirectObject import DirectObject
from panda3d.core import TransparencyAttrib
from direct.task.Task import Task
import sys

class Overlay():
    def __init__(self, parent):
        taskMgr.add(self.guiLoop, "guiLoop")
        
        #HUD
        self.font = loader.loadFont("../assets/font/Orbitron Light.otf")
        self.momPercent = 100
        self.wepCounter = 0
        self.wepAmmo = [30, 5, 2]
        self.lefthudback = OnscreenImage(image = "../assets/2d/icons/hudback.png", pos = (-1.05, 0, -.9), scale=(.3,1,.2))
        self.righthudback = OnscreenImage(image = "../assets/2d/icons/hudbackR.png", pos = (1.05, 0, -.9), scale=(.3,1,.2))
        self.percentDisplay = OnscreenText(text = "%s %s" % (self.momPercent, "%"), fg = (0,1,1,1), pos = (-1.05, -.9), scale = .125, font = self.font)
        self.wepDisplay = OnscreenText(text = "%s" % (self.wepAmmo[self.wepCounter]), fg = (0,1,1,1), pos = (.95, -.9), scale = .125, font = self.font)
        self.wepIcon = OnscreenImage(image = "../assets/2d/icons/weapon%s.png" % (self.wepCounter), pos = (1.19, 0, -.875), scale=(.1,1,.1))
        self.wepIcon.setTransparency(TransparencyAttrib.MAlpha)

        #Define controls
        self.keys = {"swap-up": 0, "swap-down": 0}
        parent.accept("wheel_up", self.setKey, ["swap-up", 1])
        parent.accept("wheel_down", self.setKey, ["swap-down", 1])
    
    def setKey(self, key, val): self.keys[key] = val
    
    #Called to add or remove ammo
    def changeAmmo(self, counter, val):
        self.wepAmmo[counter] += val
        if self.wepCounter == counter:
            self.wepDisplay.remove()
            self.wepDisplay = OnscreenText(text = "%s" % (self.wepAmmo[counter]), fg = (0,1,1,1), pos = (.95, -.9), scale = .125, font = self.font)
    
    def guiLoop(self, task):
    
        #Scroll up and down to scroll through weapons
        if self.keys["swap-up"]:
            if self.wepCounter < 2:
                self.wepCounter += 1
            else:
                self.wepCounter = 0
            self.wepDisplay.remove()
            self.wepDisplay = OnscreenText(text = "%s" % (self.wepAmmo[self.wepCounter]), fg = (0,1,1,1), pos = (.95, -.9), scale = .125, font = self.font)
            self.wepIcon.remove()
            self.wepIcon = OnscreenImage(image = "../assets/2d/icons/weapon%s.png" % (self.wepCounter), pos = (1.19, 0, -.875), scale=(.1,1,.1))
            self.wepIcon.setTransparency(TransparencyAttrib.MAlpha)
            self.keys["swap-up"] = 0
        if self.keys["swap-down"]:
            if self.wepCounter > 0:
                self.wepCounter -= 1
            else:
                self.wepCounter = 2
            self.wepDisplay.remove()
            self.wepDisplay = OnscreenText(text = "%s" % (self.wepAmmo[self.wepCounter]), fg = (0,1,1,1), pos = (.95, -.9), scale = .125, font = self.font)
            self.wepIcon.remove()
            self.wepIcon = OnscreenImage(image = "../assets/2d/icons/weapon%s.png" % (self.wepCounter), pos = (1.19, 0, -.875), scale=(.1,1,.1))
            self.wepIcon.setTransparency(TransparencyAttrib.MAlpha)
            self.keys["swap-down"] = 0

        return Task.cont