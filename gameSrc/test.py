from pandac.PandaModules import loadPrcFileData 
loadPrcFileData("", "framebuffer-multisample 1")
loadPrcFileData("","multisamples 1")
loadPrcFileData("","fullscreen #f")
loadPrcFileData("","win-size 800 600")
import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update  functions
from panda3d.bullet import BulletWorld
from direct.filter.CommonFilters import CommonFilters
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
import math,sys
import ConfigParser
from math import sin
from math import cos
import objects

import collision, lights, edit, overlay, menu
from createcube import createCube
print len((1,2,3))

mousePos       = [0,0] 
mousePrevPos    = [0,0] 

traverser = CollisionTraverser('traverser name')
base.cTrav = traverser

base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
crosshair = OnscreenImage(image = 'crosshair.png', pos = (0, 0, 0.02),scale=(.003,1,.003))

# set up the collision traverser
collisionHandler = collision.initializeCollisions()

collision.setupMousePicker('mouseraycnode',collisionHandler)
class Mover():
    def __init__(self,parent):
        self.keymap = {"left": 0, "right":0, "up":0,"down":0}
        self.prevTime = 0
        # panda walk
        parent.accept("w",self.setKey,["up",1])
        parent.accept("w-up",self.setKey,["up",0])
        parent.accept("s",self.setKey,["down",1])
        parent.accept("s-up",self.setKey,["down",0])
        parent.accept("a",self.setKey,["left",1])
        parent.accept("a-up",self.setKey,["left",0])
        parent.accept("d",self.setKey,["right",1])
        parent.accept("d-up",self.setKey,["right",0])
        
        taskMgr.add(self.fpMove,"moveTask")
        taskMgr.add(self.mouseTask, 'mouseTask') 
        self.parent = parent
    def fpMove(self,task):
        dt = task.time-self.prevTime
        self.parent.segway.setZ(self.parent.player.getZ()-.5)
        #if not self.parent.editMode:
        camera.setPos(self.parent.player.getPos()+(0,0,1))
        #camera.setZ(self.parent.player.getZ()+1)
        
        self.prevTime = task.time
        vertical = self.keymap["up"]+self.keymap["down"]
        horizontal = self.keymap["left"]+self.keymap["right"]
        if vertical==0 and horizontal==0:
            return task.cont
        direction = self.keymap["up"]-self.keymap["down"]
        velocity = 150
        vertical = vertical * velocity
        horizontal = horizontal * velocity
        pos = self.parent.player.getPos()
        #pos[2] = pos[2]+1
        h = deg2Rad(camera.getH())
        p = deg2Rad(camera.getP())
        
        #get the direction vector
        dir = (-cos(p)*sin(h)*direction, cos(p)*cos(h)*direction, sin(p)*direction)
        #get the modified direction from strafing
        if self.keymap["left"]:
            dx = sin(h-math.pi/2)
            dy = cos(h-math.pi/2)
            dir = (dir[0]+dx,dir[1]-dy,dir[2])
        if self.keymap["right"]:
            dx = sin(h+math.pi/2)
            dy = cos(h+math.pi/2)
            dir = (dir[0]+dx,dir[1]-dy,dir[2])
        if horizontal:
            len = math.sqrt(dir[0]*dir[0]+dir[1]*dir[1]+dir[2]*dir[2])
            dir = (dir[0]/len,dir[1]/len,dir[2]/len)
        #get the velocity
        vel = (dir[0]*velocity,dir[1]*velocity,dir[2]*velocity)
        #get displacement
        dis = (vel[0]*dt,vel[1]*dt,vel[2]*dt)
        #set the new position
        self.parent.player.setPos(pos[0]+dis[0],pos[1]+dis[1],pos[2]+dis[2])
        self.parent.segway.setX(self.parent.player.getX()+sin(deg2Rad(camera.getH())+math.pi))
        self.parent.segway.setY(self.parent.player.getY()-cos(deg2Rad(camera.getH())+math.pi))
        return task.cont
    def setKey(self,key,value):
        self.keymap[key] = value
    def mouseTask(self,task): 
        global mousePos, mousePrevPos 
        
        if (not base.mouseWatcherNode.hasMouse() ): return Task.cont
        
        # Get mouse coordinates from mouse watcher 
        x=base.mouseWatcherNode.getMouseX()
        y=base.mouseWatcherNode.getMouseY()
        mousePos = [x,y] 
        # Calculate mouse movement from last frame and output (print) 
        move = [mousePos[0],mousePos[1]] 
        if move==[0,0]: return Task.cont
        #print "Moved:\t %f right, \t %f up." %(move[0], move[1]) 
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
        # Save current position for next calculation 
        mousePrevPos = mousePos
        
        camera.setP(camera.getP()+100*move[1])
        camera.setH(camera.getH()-100*move[0])
        
        if self.parent.editMode:
            return Task.cont
        
        self.parent.segway.setH(camera.getH()+180)
        self.parent.segway.setX(self.parent.player.getX()+sin(deg2Rad(camera.getH()+180)))
        self.parent.segway.setY(self.parent.player.getY()-cos(deg2Rad(camera.getH()+180)))
        
        return Task.cont

class World(DirectObject):
    global traverser, queue
    def __init__(self):

        #Note, this sort of breaks all game functionality.
        #Keep it commented out if you want to test the game properly.
        #startMenu = menu.Menu(self)
        
        self.configurePanda()
        camera.setPosHpr(0, -15, 0, 0, 0, 0) # x,y,z,heading, pitch, roll
        # list of instances
        self.boxInstances = list()
        self.waterInstances = list()
        self.dangerInstances = list()
        self.plantInstances = list()
        self.spikeInstances = list()
        self.editMode = False
        #world init
        self.loadModels()
        self.setupLights()
        self.setupCollisions()
        self.mover = Mover(self)
        #self.initMove()
        self.accept("escape",sys.exit)
                
        self.overlay = overlay.Overlay(self)

        self.onRay = list()
        self.offRay = list()
        self.activeRay = list()
        campos = self.segway.getPos()
        campos[2] = campos[2]-5
        camera.lookAt(campos)
    def configurePanda(self):
        props = WindowProperties()
        props.setCursorHidden(True) 
        #props.setSize(1440, 900)
        #props.setFullscreen(1) 
        base.win.requestProperties(props)
        render.setShaderAuto()
        base.disableMouse()
        base.setFrameRateMeter(True)
        #render.setAntialias(AntialiasAttrib.MAuto)
        #render.setAntialias(AntialiasAttrib.MMultisample,1)
        self.filters = CommonFilters(base.win, base.cam)
        self.filters.setCartoonInk()
    def loadModels(self):
        """ loads initial models into the world """
        #self.env = collision.loadAndPositionModelFromFile("environment",scale=.25,pos=(-8,42,0))
        #self.env = collision.loadAndPositionModelFromFile("2012sphereenvironment")
        #self.panda = collision.loadAndPositionModelFromFile("panda-model",scale=.005,show=0)
        
        pnode = ModelRoot("player")
        self.player = render.attachNewNode(pnode)
        pc = self.player.attachNewNode(CollisionNode("playerCollision"))
        pc.node().addSolid(CollisionRay(0,0,-1,0,0,1))
        self.playerCnode = pc
        self.player.setPos(0,0,1)
        
        self.env = collision.loadAndPositionModelFromFile("../assets/3d/zzzzzzzzzarena proto spawn tests.egg")
        print self.env.ls()
        objects.loadPlayers(self.env)
        objects.loadTrapAs(self.env)
        objects.loadTrapBs(self.env)
        objects.loadAmmo(self.env)
        print self.env.ls()
        
        self.segway = collision.loadAndPositionModelFromFile("bestvehicle",scale=.07,show=0)
        self.segway.node().getChild(0).removeChild(0)
        self.segway.setH(camera.getH()+180)
        self.segway.setX(self.player.getX()+sin(deg2Rad(camera.getH()+180)))
        self.segway.setY(self.player.getY()-cos(deg2Rad(camera.getH()+180)))
        #self.segway.setZ(1)
        
        #camera.setPos(0,0,0)
        #camera.reparentTo(self.player)
        print camera.getParent().getName()
    def setupCollisions(self):
        #pandaCollider = self.panda.attachNewNode(CollisionNode('pandacnode'))
        #pandaCollider.show()
        #pandaCollider.node().addSolid(CollisionSphere((0, 0, 0), 2/.005))
        #base.cTrav.addCollider(pandaCollider,collisionHandler)
        self.lifter = CollisionHandlerFloor()
        self.lifter.setOffset(1)
        base.cTrav.addCollider(self.playerCnode,self.lifter) 
        self.lifter.addCollider(self.playerCnode, self.player)
        #base.cTrav.showCollisions(render)
    def die(self,event):
        base.cTrav.removeCollider(self.wheelsphere)
        self.segway.node().getChild(0).removeChild(0)
        self.filters.setInverted()
        print "You Died!"
    def setupLights(self):
        """loads initial lighting"""
        self.ambientLight = lights.setupAmbientLight()
        
        self.dirLight = DirectionalLight("dirLight")
        self.dirLight.setColor((.4,.4,.4,1))
        self.dirLightNP = render.attachNewNode(self.dirLight)
        self.dirLightNP.setHpr(0,-25,0)
        render.setLight(self.dirLightNP)
        
        self.light = lights.loadModelSpotlightByName(self.segway,"segwaylight","segwaylight1","segwayLight")
        
        #panda2 = collision.loadAndPositionModelFromFile("panda-model",scale=.005,pos=tifLeftLight.getPos())
        

world = World()
run()