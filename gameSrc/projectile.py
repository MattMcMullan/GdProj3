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
from model import Model
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import BulletCharacterControllerNode

class Projectile():
    projectiles = list()
    model = 0
    index = 0
    def __init__(self, ppos, h, p, parent, parentVel, world, worldNP):
        self.world=world
        if Projectile.model==0:
            Projectile.model = Model("../assets/3d/Actors/ball_proj2.egg")
        h = deg2Rad(camera.getH())
        p = deg2Rad(camera.getP())
        dir = (-cos(p)*sin(h), cos(p)*cos(h), sin(p))
        ppos = map(lambda i: ppos[i]+dir[i]*5, range(3))
        self.instance = Projectile.model.createInstance(pos=ppos,hpr=(h,p,0),scale=3)
        
        self.dhpr = [random.random(),random.random(),random.random()]
        
        pmin = LPoint3()
        pmax = LPoint3()
        self.instance.calcTightBounds(pmin,pmax)
        norm = pmin-pmax
        self.off = (norm[0]*.5,norm[1]*.5,norm[2]*.5)
        r = max(norm)
        
        pos = ppos
        
        shape = BulletSphereShape(.5*r)
        self.sphere = BulletGhostNode('ProjectileSphere')
        self.sphere.addShape(shape)
        self.sphere.setDeactivationEnabled(False)
        self.np = worldNP.attachNewNode(self.sphere)
        self.np.setPos(LVecBase3f(ppos[0],ppos[1],ppos[2]))
        self.np.setCollideMask(BitMask32.allOn())
        world.attachGhost(self.sphere)
        
        dir = (-cos(p)*sin(h), cos(p)*cos(h), sin(p))
        self.vel = parentVel
        self.vel = map(lambda i: dir[i]*100, range(3))
        self.index = Projectile.index
        self.parent = parent
        Projectile.index = Projectile.index + 1
        taskMgr.add(self.move,"Proj"+str(Projectile.index)+"MoveTask")
        self.prevTime = 0
        self.lifeTime = 0
        Projectile.projectiles.append(self)
        self.TIMEDLIFE = 120
    def kill(self):
        self.instance.removeNode()
        self.parent.projectiles.remove(self)
        self.world.removeGhost(self.sphere)
        Projectile.projectiles.remove(self)
    def check(self,contacts,human,players):
        if len(contacts)==0:
            return
        contactObject = contacts[0].getNode0()
        if contacts[0].getNode0().getName()=="TrapSphere":
            contactObject = contacts[0].getNode1()
        name = contactObject.getName()
        print name
        if name==human.character.getName():
            human.impact(self.vel)
            self.kill()
            return
        for i in range(len(players)):
            if name==players[i].character.getName():
                players[i].impact(self.vel)
                self.kill()
                return
        return
        
    def move(self,task):
        dt = task.time-self.prevTime
        #If the projectile exceeds its maximum lifetime or burns out on the arena bounds -
        self.lifeTime += dt
        if(self.lifeTime >= self.TIMEDLIFE):
            #kill projectile
            self.instance.removeNode()
            self.parent.projectiles.remove(self)
            self.world.removeGhost(self.sphere)
            Projectile.projectiles.remove(self)
            return
            #print "Projectile removed"
        if(self.lifeTime < self.TIMEDLIFE):
            #get the position
            pos = self.instance.getPos()
            #get the displacement
            dis = (self.vel[0]*dt,self.vel[1]*dt,self.vel[2]*dt)
            #set the new position
            self.np.setPos(pos[0]+dis[0],pos[1]+dis[1],pos[2]+dis[2])
            self.instance.setPos(pos[0]+dis[0],pos[1]+dis[1],pos[2]+dis[2])
            
            hpr = self.instance.getHpr()
            hpr = map(lambda i: hpr[i]+dt*100*self.dhpr[i], range(3))
            self.instance.setHpr(hpr[0],hpr[1],hpr[2])
            return task.cont
       