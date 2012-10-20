import direct.directbase.DirectStart
from pandac.PandaModules import *
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
        self.font = loader.loadFont("Orbitron Light.otf")
        self.momPercent = 100
        self.wepCounter = 0
        self.wepAmmo = [5, 1, 0]
        self.percentDisplay = OnscreenText(text = "%s %s" % (self.momPercent, "%"), fg = (0,1,1,1), pos = (-1.05, -.9), scale = .125, font = self.font)
        self.wepDisplay = OnscreenText(text = "%s" % (self.wepAmmo[self.wepCounter]), fg = (0,1,1,1), pos = (1, -.9), scale = .125, font = self.font)
        self.wepIcon = OnscreenImage(image = "weapon%s.png" % (self.wepCounter), pos = (1.19, 0, -.875), scale=(.1,1,.1))
        self.wepIcon.setTransparency(TransparencyAttrib.MAlpha)
        
        #self.wepIcon.setTag("myObjectTag", '1')

        #Define controls
        self.keys = {"swap-up": 0, "swap-down": 0, "m1": 0}
        parent.accept("escape", sys.exit)
        parent.accept("mouse1", self.setKey, ["m1", 1])
        parent.accept("wheel_up", self.setKey, ["swap-up", 1])
        parent.accept("wheel_down", self.setKey, ["swap-down", 1])
    
    def setKey(self, key, val): self.keys[key] = val
    
    def guiLoop(self, task):
        
        #Adds 10% each click
        if self.keys["m1"]:
            self.momPercent += 10
            self.percentDisplay.remove()
            self.percentDisplay = OnscreenText(text = "%s %s" % (self.momPercent, "%"), fg=(0,1,1,1), pos=(-1.05,-.9), scale = .125, font = self.font)
            self.keys["m1"] = 0

        #Scroll up and down to scroll through weapons
        if self.keys["swap-up"]:
            if self.wepCounter < 2:
                self.wepCounter += 1
            else:
                self.wepCounter = 0
            self.wepDisplay.remove()
            self.wepDisplay = OnscreenText(text = "%s" % (self.wepAmmo[self.wepCounter]), fg = (0,1,1,1), pos = (1, -.9), scale = .125, font = self.font)
            self.wepIcon.remove()
            self.wepIcon = OnscreenImage(image = "weapon%s.png" % (self.wepCounter), pos = (1.19, 0, -.875), scale=(.1,1,.1))
            self.wepIcon.setTransparency(TransparencyAttrib.MAlpha)
            #self.wepIcon.setTag("myObjectTag", '1')
            self.keys["swap-up"] = 0
        if self.keys["swap-down"]:
            if self.wepCounter > 0:
                self.wepCounter -= 1
            else:
                self.wepCounter = 2
            self.wepDisplay.remove()
            self.wepDisplay = OnscreenText(text = "%s" % (self.wepAmmo[self.wepCounter]), fg = (0,1,1,1), pos = (1, -.9), scale = .125, font = self.font)
            self.wepIcon.remove()
            self.wepIcon = OnscreenImage(image = "weapon%s.png" % (self.wepCounter), pos = (1.19, 0, -.875), scale=(.1,1,.1))
            self.wepIcon.setTransparency(TransparencyAttrib.MAlpha)
            #self.wepIcon.setTag("myObjectTag", '1')
            self.keys["swap-down"] = 0

        return Task.cont