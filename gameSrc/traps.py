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
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import BulletCharacterControllerNode

class floatTrap():
    traps = list()
    model = 0
    index = 0
    def __init__(self, ppos, world, worldNP):
        self.world = world
        if floatTrap.model==0:
            floatTrap.model = Model("../assets/3d/Actors/beartrap2.egg")
        h = deg2Rad(camera.getH())
        p = deg2Rad(camera.getP())
        dir = (-cos(p)*sin(h), cos(p)*cos(h), sin(p))
        npos = map(lambda i: ppos[i]+dir[i]*25, range(3))
        self.instance = floatTrap.model.createInstance(pos=npos,hpr=(0,0,0))
        self.index = floatTrap.index
        
        pmin = LPoint3()
        pmax = LPoint3()
        self.instance.calcTightBounds(pmin,pmax)
        norm = pmin-pmax
        self.off = (norm[0]*.5,norm[1]*.5,norm[2]*.5)
        r = max(norm)
        shape = BulletSphereShape(.7*r)
        self.sphere = BulletGhostNode('TrapSphere')
        self.sphere.addShape(shape)
        self.sphere.setDeactivationEnabled(False)
        self.np = worldNP.attachNewNode(self.sphere)
        self.np.setPos(LVecBase3(npos[0],npos[1],npos[2]))
        self.np.setCollideMask(BitMask32.allOn())
        world.attachGhost(self.sphere)
        
        #taskMgr.add(self.check,"floatTrap"+str(self.index)+"Check")
        floatTrap.traps.append(self)
        floatTrap.index = floatTrap.index + 1
        #pos = self.instance.getPos()
        #self.np.setPos(pos[0]-self.off[0],pos[1]-self.off[1],pos[2]-self.off[2])
    def kill(self):
        floatTrap.traps.remove(self)
        self.world.removeGhost(self.sphere)
        self.instance.detachNode()
    def check(self,contacts,human,players):
        if len(contacts)>0:
            contactObject = contacts[0].getNode0()
            if contacts[0].getNode0().getName()=="TrapSphere":
                contactObject = contacts[0].getNode1()
            name = contactObject.getName()
            print contactObject
            if name==human.character.getName():
                human.trap1()
                self.kill()
                return
            for i in range(len(players)):
                if name==players[i].character.getName():
                    players[i].trap1()
                    self.kill()
                    return

class clawTrap():
    traps = list()
    model = 0
    index = 0
    def __init__(self, world, worldNP):
        self.failed = 1
        self.world = world
        if clawTrap.model==0:
            clawTrap.model = Model("../assets/3d/Actors/claw3.egg")
        h = deg2Rad(camera.getH())
        p = deg2Rad(camera.getP())
        dir = (-cos(p)*sin(h), cos(p)*cos(h), sin(p))
        cpos = camera.getPos()
        vec = map(lambda i: cpos[i]+dir[i]*200, range(3))
        rayHit = world.rayTestClosest(cpos,LPoint3(vec[0],vec[1],vec[2]))
        if not rayHit.hasHit():
            return
        npos = rayHit.getHitPos()
        n = rayHit.getHitNormal()
        print n
        npos = map(lambda i: npos[i]+n[i]*5, range(3))
        self.instance = clawTrap.model.createInstance(pos=npos,hpr=(-90*n.x,180*(n.z==1)+90*(abs(n.x)+n.y),0))
        self.index = clawTrap.index
        
        pmin = LPoint3()
        pmax = LPoint3()
        self.instance.calcTightBounds(pmin,pmax)
        norm = pmin-pmax
        self.off = (norm[0]*.5,norm[1]*.5,norm[2]*.5)
        r = max(norm)
        shape = BulletSphereShape(.7*r)
        self.sphere = BulletGhostNode('TrapSphere')
        self.sphere.addShape(shape)
        self.sphere.setDeactivationEnabled(False)
        self.np = worldNP.attachNewNode(self.sphere)
        self.np.setPos(LVecBase3(npos[0],npos[1],npos[2]))
        self.np.setCollideMask(BitMask32.allOn())
        world.attachGhost(self.sphere)
        
        #taskMgr.add(self.check,"floatTrap"+str(self.index)+"Check")
        clawTrap.traps.append(self)
        clawTrap.index = clawTrap.index + 1
        self.failed = 0
        #pos = self.instance.getPos()
        #self.np.setPos(pos[0]-self.off[0],pos[1]-self.off[1],pos[2]-self.off[2])
    def kill(self):
        clawTrap.traps.remove(self)
        self.world.removeGhost(self.sphere)
        self.instance.detachNode()
    def check(self,contacts,human,players):
        if len(contacts)>0:
            contactObject = contacts[0].getNode0()
            if contacts[0].getNode0().getName()=="TrapSphere":
                contactObject = contacts[0].getNode1()
            name = contactObject.getName()
            print contactObject
            if name==human.character.getName():
                human.trap2()
                self.kill()
                return
            for i in range(len(players)):
                if name==players[i].character.getName():
                    players[i].trap2()
                    self.kill()
                    return
            