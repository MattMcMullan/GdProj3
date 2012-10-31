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

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletConvexHullShape
from panda3d.bullet import BulletDebugNode

import math,sys
import ConfigParser
import objects
import human
from projectile import Projectile
from traps import clawTrap
from traps import floatTrap
from human import Human

import collision, lights, edit, overlay, menu
from createcube import createCube
#print len((1,2,3))

#base.cTrav = CollisionTraverser()
#base.cTrav = traverser

base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
crosshair = OnscreenImage(image = 'crosshair.png', pos = (0, 0, 0.02),scale=(.003,1,.003))

#collision.setupMousePicker('mouseraycnode',collisionHandler)

class World(DirectObject):
    global traverser, queue
    def __init__(self):
        startMenu = menu.Menu(self)
    
    #Please do not remove this function, it makes the menu work.
    def beginGame(self):
        self.configurePanda()
        camera.setPosHpr(0, -15, 0, 0, 0, 0) # x,y,z,heading, pitch, roll
        #world init
        self.setupBullet()
        self.loadModels()
        self.setupLights()
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
        self.filters.setBloom(blend=(1,0,0,1), desat=-0.5, intensity=6.0, size=2)
        #self.filters.setAmbientOcclusion()
        #self.filters.setCartoonInk()
    def setupBullet(self):
        taskMgr.add(self.update, 'updateWorld')
        self.worldNP = render.attachNewNode('World')
        # World
        #self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
        #self.debugNP.show()
        #self.debugNP.node().showWireframe(False)
        #self.debugNP.node().showConstraints(False)
        #self.debugNP.node().showBoundingBoxes(False)
        #self.debugNP.node().showNormals(False)
        
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, 0))
        #self.world.setDebugNode(self.debugNP.node())
        
    def update(self, task):
        dt = globalClock.getDt()

        for i in self.aTrapSpawn:
            contacts = self.world.contactTest(i.sphere).getContacts()
            if len(contacts)>0:
                i.trap1Collide(contacts,self.mover)
        for i in self.bTrapSpawn:
            contacts = self.world.contactTest(i.sphere).getContacts()
            if len(contacts)>0:
                i.trap2Collide(contacts,self.mover)
        for i in self.ammoSpawn:
            contacts = self.world.contactTest(i.sphere).getContacts()
            if len(contacts)>0:
                i.ammoCollide(contacts,self.mover)
        for i in human.floatTrap.traps:
            contacts = self.world.contactTest(i.sphere).getContacts()
            if len(contacts)>0:
                i.check(contacts,self.mover,self.players)
        for i in human.clawTrap.traps:
            contacts = self.world.contactTest(i.sphere).getContacts()
            if len(contacts)>0:
                i.check(contacts,self.mover,self.players)
        
        self.world.doPhysics(dt,1)

        return task.cont
    def loadModels(self):
        """ loads initial models into the world """
        # create the environment
        self.env = collision.loadAndPositionModelFromFile("../assets/3d/mayaActors/arena_collisions_nogrid.egg")
        self.envBoxes = objects.genBulletBoxes(self.env,self.world)
        #load objects out of the environment
        #human
        self.mover = Human(self,self.world,self.worldNP)
        tmp = self.env.find("**/PlayerSpawn1")
        self.mover.bulletInit(self.world,tmp.getPos())
        tmp.detachNode()
        #AI players
        self.players = objects.loadPlayers(self.env,self.world,self.worldNP)
        for i in range(0,5):
            self.players[i].bulletInit(self.world,self.players[i].instance.getPos())
        
        #Spawners
        collisionHandler=0
        self.aTrapSpawn = objects.loadTrapAs(self.env, self.world, self.worldNP)
        self.bTrapSpawn = objects.loadTrapBs(self.env, self.world, self.worldNP)
        self.ammoSpawn = objects.loadAmmo(self.env, self.world, self.worldNP)
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