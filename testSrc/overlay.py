import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from panda3d.core import CollisionRay,CollisionNode,GeomNode,CollisionTraverser,CollisionHandlerEvent
from direct.task.Task import Task
import sys

def loadObject(tex, x, y, depth, modelCounter, scale = 3, transparency = True):
    obj = loader.loadModel("Models/plane%s" % (modelCounter)) #Every object uses the plane model
    obj.reparentTo(camera) #Everything is parented to the camera so that it faces the screen
    obj.setPos(x, depth, y) #Set initial position
    obj.setScale(scale) #Set initial scale
    obj.setBin("unsorted", 0) #This tells Panda not to worry about the order this is drawn in. (it prevents an effect known as z-fighting)
    obj.setDepthTest(False) #Tells panda not to check if something has already drawn in front of it
    if transparency: obj.setTransparency(1) #All of our objects are transparent
    if tex:
        tex = loader.loadTexture(tex+".png") #Load the texture
        obj.setTexture(tex, 1) #Set the texture
    return obj
    
class Overlay(DirectObject):
    def __init__(self):
        #Tester Model
        camera.setPosHpr(0, -15, 7, 0, -15, 0)
        self.player = loader.loadModel("Models/player_temp")
        self.player.reparentTo(render)
        self.player.setPos(0,15,0)

        #HUD
        self.font = loader.loadFont("Fonts/Orbitron Light.otf")
        self.momPercent = 100
        self.wepCounter = 0
        self.wepAmmo = [5, 1, 0]
        self.percentDisplay = OnscreenText(text = "%s %s" % (self.momPercent, "%"), fg = (0,1,1,1), pos = (-1.05, -.9), scale = .125, font = self.font)
        self.wepDisplay = OnscreenText(text = "%s" % (self.wepAmmo[self.wepCounter]), fg = (0,1,1,1), pos = (1, -.9), scale = .125, font = self.font)
        self.wepIcon = loadObject("Sprites/weapon%s" %(self.wepCounter), 17.5, -12.75, 55, self.wepCounter)
        self.hudBack = loadObject("Sprites/hudback", -15, -15, 60, 0) #temporary framing thing, will make it better with proper sprites
        
        self.wepIcon.setTag("myObjectTag", '1')
        self.hudBack.setTag("myObjectTag", '2')

        #Define controls
        self.keys = {"swap-up": 0, "swap-down": 0, "m1": 0}
        self.accept("escape", sys.exit)
        self.accept("mouse1", self.setKey, ["m1", 1])
        self.accept("wheel_up", self.setKey, ["swap-up", 1])
        self.accept("wheel_down", self.setKey, ["swap-down", 1])

        self.gameTask = taskMgr.add(self.gameLoop, "gameLoop")
    
    def setKey(self, key, val): self.keys[key] = val
    
    def gameLoop(self, task):
        
        #Adds 10% each click
        if self.keys["m1"]:
            clickthing()
            
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
            self.wepIcon = loadObject("Sprites/weapon%s" %(self.wepCounter), 17.5, -12.75, 55, self.wepCounter)
            self.wepIcon.setTag("myObjectTag", '1')
            self.keys["swap-up"] = 0
        if self.keys["swap-down"]:
            if self.wepCounter > 0:
                self.wepCounter -= 1
            else:
                self.wepCounter = 2
            self.wepDisplay.remove()
            self.wepDisplay = OnscreenText(text = "%s" % (self.wepAmmo[self.wepCounter]), fg = (0,1,1,1), pos = (1, -.9), scale = .125, font = self.font)
            self.wepIcon.remove()
            self.wepIcon = loadObject("Sprites/weapon%s" %(self.wepCounter), 17.5, -12.75, 55, self.wepCounter)
            self.wepIcon.setTag("myObjectTag", '1')
            self.keys["swap-down"] = 0

        return Task.cont
        
def clickthing():
    base.cTrav = CollisionTraverser()
    cHandler = CollisionHandlerQueue()
    
    pickerNode = CollisionNode('mouseRay')
    pickerNP = camera.attachNewNode(pickerNode)
    pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
    pickerRay = CollisionRay()
    pickerNode.addSolid(pickerRay)
    base.cTrav.addCollider(pickerNP, cHandler)
    
    if base.mouseWatcherNode.hasMouse():
        mpos = base.mouseWatcherNode.getMouse()
        
    pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
     
    base.cTrav.traverse(render)
    # Assume for simplicity's sake that myHandler is a CollisionHandlerQueue.
    if cHandler.getNumEntries() > 0:
    # This is so we get the closest object.
        cHandler.sortEntries()
        pickedObj = cHandler.getEntry(0).getIntoNodePath()
        pickedObj = pickedObj.findNetTag('myObjectTag')
        if not pickedObj.isEmpty():
           print pickedObj          
    
o = Overlay()
run()