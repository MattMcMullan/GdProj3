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
import objects
from human import Human

import collision, lights, edit, overlay, menu
from createcube import createCube
print len((1,2,3))

traverser = CollisionTraverser('traverser name')
base.cTrav = traverser

base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
crosshair = OnscreenImage(image = 'crosshair.png', pos = (0, 0, 0.02),scale=(.003,1,.003))

# set up the collision traverser
collisionHandler = collision.initializeCollisions()

collision.setupMousePicker('mouseraycnode',collisionHandler)


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
        self.mover = Human(self)
        self.setupLights()
        self.setupCollisions()
        #self.initMove()
        self.accept("escape",sys.exit)
                
        self.overlay = overlay.Overlay(self)
        #self.ball = ball.Ball(self)

        self.onRay = list()
        self.offRay = list()
        self.activeRay = list()
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
        #self.filters.setCartoonInk()
    def loadModels(self):
        """ loads initial models into the world """
        #self.env = collision.loadAndPositionModelFromFile("environment",scale=.25,pos=(-8,42,0))
        #self.env = collision.loadAndPositionModelFromFile("2012sphereenvironment")
        #self.panda = collision.loadAndPositionModelFromFile("panda-model",scale=.005,show=0)
        
        #NOTE: I'm having a pathing error, and for some reason cannot use the new (currently commented)
        #code!  So I must temporarily keep the old code here.
        self.env = collision.loadAndPositionModelFromFile("../assets/3d/Actors/zzzzzzzzzarena proto spawn tests.egg")
        #self.env = collision.loadAndPositionModelFromFile("../assets/3d/Actors/arena with collisions3.egg")
        #self.env = collision.loadAndPositionModelFromFile('../assets/3d/Actors/arena with collisions3')
        #print self.env.ls()
        self.players = objects.loadPlayers(self.env)
        self.aTrapSpawn = objects.loadTrapAs(self.env)
        self.bTrapSpawn = objects.loadTrapBs(self.env)
        self.ammoSpawn = objects.loadAmmo(self.env)
        
        #self.human.setX(self.player.getX()+sin(deg2Rad(camera.getH()+180)))
        #self.human.setY(self.player.getY()-cos(deg2Rad(camera.getH()+180)))
        #self.human.setZ(1)
        
        #camera.setPos(0,0,0)
        #camera.reparentTo(self.player)
        print camera.getParent().getName()
    def setupCollisions(self):
        self.pusher = CollisionHandlerPusher()
        self.pusher.addInPattern('%fn-into-%in')
        self.pusher.addOutPattern('%fn-out-%in')
        self.pusher.addAgainPattern('%fn-again-%in')
        
        objects.loadColBoxes(self.env,self.pusher)
        #print self.env.ls()
        self.mover.addCollisions(self.pusher,"PlayerCollide")
        
        self.accept("PlayerCollide-into-EnvCollide",sys.exit)
        return
        #pandaCollider = self.panda.attachNewNode(CollisionNode('pandacnode'))
        #pandaCollider.show()
        #pandaCollider.node().addSolid(CollisionSphere((0, 0, 0), 2/.005))
        #base.cTrav.addCollider(pandaCollider,collisionHandler)
        #self.lifter = CollisionHandlerFloor()
        #self.lifter.setOffset(1)
        #base.cTrav.addCollider(self.playerCnode,self.lifter) 
        #self.lifter.addCollider(self.playerCnode, self.player)
        #base.cTrav.showCollisions(render)
    def setupLights(self):
        """loads initial lighting"""
        self.ambientLight = lights.setupAmbientLight()
        
        self.dirLight = DirectionalLight("dirLight")
        self.dirLight.setColor((.4,.4,.4,1))
        self.dirLightNP = render.attachNewNode(self.dirLight)
        self.dirLightNP.setHpr(0,-25,0)
        render.setLight(self.dirLightNP)
        
        #self.light = lights.loadModelSpotlightByName(self.human,"humanlight","humanlight1","segwaLight")
        
        #panda2 = collision.loadAndPositionModelFromFile("panda-model",scale=.005,pos=tifLeftLight.getPos())
        

world = World()
run()