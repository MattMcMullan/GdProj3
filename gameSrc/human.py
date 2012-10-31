import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update  functions
import math,sys
from math import sin
from math import cos
import random
import collision
from projectile import Projectile
from model import Model
from traps import clawTrap
from traps import floatTrap
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import BulletCharacterControllerNode

mousePos       = [0,0] 
mousePrevPos    = [0,0]

class Human():
    def __init__(self,parent, world, worldNP):
        """__init__
        parameters:
            self
            parent: the World object
            world: bullet world
            worldNP: where in the world to put it
        returns:
            none
        Description:
            Create the human player
        """
        self.traptime = 0
        self.world = world
        self.worldNP = worldNP
        
        self.projectiles = list()
        self.floatTraps = list()
        
        self.keymap = {"left": 0, "right":0, "up":0,"down":0, "m1":0}
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
        parent.accept("mouse1", self.setKey, ["m1",1])
        
        self.velocity = 0
        self.dir = (0,0,0)
        
        self.vel = (0,0,0)
        
        taskMgr.add(self.fpMove,"moveTask",sort=50)
        taskMgr.add(self.mouseTask, 'mouseTask')
        self.parent = parent
        #self.human = self.parent.human
        #self.human = collision.loadAndPositionModelFromFile("../assets/3d/Actors/robot rig 10 coll.egg",scale=.07,show=0)
        self.human = Actor('../assets/3d/Actors/robot_idle_final_actor.egg', {
          'idle':'../assets/3d/Actors/robot_idle_final_anim.egg',
        #  'throw':'../assets/3d/Actors/animation eggs/robot_throw_final.egg',
        #  'place':'../assets/3d/Actors/animation eggs/robot_place_final.egg',
        #  'death':'../assets/3d/Actors/animation eggs/robot_death_final.egg',
        })
        #print self.human.find("**/eyes_sphere").getPos()
        #self.human.flattenLight()
        print self.human.ls()
        #self.human.node().getChild(0).removeChild(0)
        self.human.setH(camera.getH()+180)
        campos = self.human.getPos()
        campos[2] = campos[2]-5
        camera.lookAt(campos)
        
        pnode = ModelRoot("player")
        self.player = render.attachNewNode(pnode)
        pc = self.player.attachNewNode(CollisionNode("playerCollision"))
        pc.node().addSolid(CollisionRay(0,0,-1,0,0,1))
        self.playerCnode = pc
        self.player.setPos(0,0,1)
        #self.human.play('idle')
        self.human.loop('idle')
    def bulletInit(self,world,pos):
        """bulletInit
        parameters:
            self
            task: the tskMgr structure
        returns:
            none
        Description:
            The rest of init requires bullet things
        """
        oldpath = self.human.find("**/body_coll")
        self.shape = BulletSphereShape(10)#oldpath.node().getSolid(0).getRadius())
        self.character = BulletCharacterControllerNode(self.shape, 0.4, 'Human')
        self.characterNP = render.attachNewNode(self.character)
        self.characterNP.setPos(pos[0],pos[1],pos[2])
        self.character.setGravity(0)
        #self.human.setPos(pos)
        self.human.reparentTo(self.characterNP)
        self.human.hide()
        #self.player.setPos(pos)
        self.player.reparentTo(self.characterNP)
        self.characterNP.setCollideMask(BitMask32.allOn())
        
        world.attachCharacter(self.character)
    def fpMove(self,task):
        """fpMove
        parameters:
            self
            task: the taskMgr structure
        returns:
            none
        Description:
            player movement
        """
        dt = task.time-self.prevTime
        camera.setPos(self.player.getPos()+(0,0,1))
        damp = (1.-(.2*dt))
        self.vel = map(lambda x: damp*x, self.vel)
        if self.traptime>0:
            self.traptime = self.traptime-dt
        #self.human.setZ(self.player.getZ()-.5)
        #if not self.parent.editMode:
        #camera.setPos(self.player.getPos()-(0.0264076, 4.60993, -10.0715))
        self.prevTime = task.time
        pos = self.player.getParent().getPos()
        delta = 10*dt
        h = deg2Rad(camera.getH())
        p = deg2Rad(camera.getP())
        # player control
        if self.keymap["up"] and self.traptime<=0:
            dir = (-cos(p)*sin(h), cos(p)*cos(h), sin(p))
            self.vel = map(lambda i: self.vel[i]+dir[i]*delta, range(3))
        if self.keymap["down"] and self.traptime<=0:
            dir = (-cos(p)*sin(h), cos(p)*cos(h), sin(p))
            self.vel = map(lambda i: self.vel[i]-dir[i]*delta, range(3))
        if self.keymap["m1"] and self.traptime<=0:
            weapon = self.parent.overlay.wepCounter
            if self.parent.overlay.wepAmmo[weapon] > 0:
                self.parent.overlay.changeAmmo(weapon, -1)
                if weapon == 0:
                    self.launch()
                    dir = (-cos(p)*sin(h), cos(p)*cos(h), sin(p))
                    self.vel = map(lambda i: self.vel[i]-dir[i]*100, range(3))
                elif weapon == 1:
                    self.placeFloatTrap()
                elif weapon == 2:
                    self.placeClawTrap()
            self.keymap["m1"] = 0
        self.character.setAngularMovement(0)
        self.character.setLinearMovement(LVector3(self.vel[0],self.vel[1],self.vel[2]),True)
        #get displacement
        dis = (self.vel[0]*dt,self.vel[1]*dt,self.vel[2]*dt)
        #set the new position
        self.player.setPos(pos[0]+dis[0],pos[1]+dis[1],pos[2]+dis[2])
        self.human.setPos(pos[0]+dis[0],pos[1]+dis[1],pos[2]+dis[2])
        #self.human.setX(self.player.getX()+sin(deg2Rad(camera.getH())+math.pi))
        #self.human.setY(self.player.getY()-cos(deg2Rad(camera.getH())+math.pi))
        return task.cont
    def launch(self):
        """launch
        parameters:
            self
        returns:
            none
        Description:
            Fire a projectile
        """
        self.projectiles.append(Projectile(self.player.getPos(),deg2Rad(camera.getH()),deg2Rad(camera.getP()),self,self.vel, self.world, self.worldNP))
    def placeFloatTrap(self):
        """placeFloatTrap
        parameters:
            self
        returns:
            none
        Description:
            Place a float trap
        """
        self.floatTraps.append(floatTrap(self.player.getPos(),self.world,self.worldNP)) 
    def placeClawTrap(self):
        """placeClawTrap
        parameters:
            self
        returns:
            none
        Description:
            Place a claw trap
        """
        trap = clawTrap(self.world,self.worldNP)
        weapon = self.parent.overlay.wepCounter
        self.parent.overlay.changeAmmo(weapon, trap.failed)
    def setKey(self,key,value):
        self.keymap[key] = value
    def mouseTask(self,task): 
        """mouseTask
        parameters:
            self
            task: the tskMgr structure
        returns:
            none
        Description:
            Keep track of the mouse and record its movement
        """
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
        
        camera.setP(camera.getP()+75*move[1])
        camera.setH(camera.getH()-75*move[0])
        
        self.human.setH(camera.getH()+180)
        self.human.setX(self.player.getX()+sin(deg2Rad(camera.getH()+180)))
        self.human.setY(self.player.getY()-cos(deg2Rad(camera.getH()+180)))
        
        contacts = self.world.contactTest(self.character).getContacts()
        for c in contacts:
            contactObject = c.getNode0()
            if c.getNode0().getName()=="Human":
                contactObject = c.getNode1()
            if contactObject.getName()=="env":
                self.vel = map(lambda x: x*.9, self.vel)
        
        return Task.cont
    def die(self,event):
        """die
        parameters:
            self
            task: the tskMgr structure
        returns:
            none
        Description:
            Kill the player
        """
        #base.cTrav.removeCollider(self.wheelsphere)
        self.human.node().getChild(0).removeChild(0)
        self.filters.setInverted()
        print "You Died!"
    def trap1(self):
        """trap1
        parameters:
            self
        returns:
            none
        Description:
            Inflict the floating trap penalty
        """
        self.vel = map(lambda x: x*.25, self.vel)
        self.traptime = self.traptime + 20
        return
    def trap2(self):
        """trap2
        parameters:
            self
        returns:
            none
        Description:
            Inflict the claw trap penalty
        """
        self.vel = (0,0,0)
        self.traptime = self.traptime + 30
        return
    def impact(self,vel):
        diff = map(lambda i: self.vel[i]-vel[i], range(3))
        self.vel = map(lambda i: self.vel[i]-diff[i], range(3))