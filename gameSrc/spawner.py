import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update  functions
import math,sys

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletConvexHullShape
from panda3d.bullet import BulletDebugNode

import collision

class Spawner():
    count = 0
    def __init__(self,ppos,model,world, worldNP):
        self.model = model
        self.physrep = model.createInstance(pos=ppos)
        self.pos = ppos
        
        shape = BulletSphereShape(13)

        np = worldNP.attachNewNode(BulletRigidBodyNode('Sphere'))
        #np.node().setMass(1.0)
        np.node().addShape(shape)
        #np.node().addShape(shape, TransformState.makePos(Point3(0, 1, 0)))
        np.setPos(self.pos[0], self.pos[1], self.pos[2] + 14)
        np.setCollideMask(BitMask32.allOn())

        world.attachRigidBody(np.node())

        self.sphere = np.node()
        
        # spawnSphere = CollisionSphere((self.pos[0], self.pos[1], self.pos[2] + 13), 14)
        # spawnNode = CollisionNode("spawner" + str(Spawner.count))
        # spawnNode.addSolid(spawnSphere)
        # spawnNodePath = render.attachNewNode(spawnNode)
        # #base.cTrav.addCollider(spawnNodePath,collisionHandler)
        # spawnNodePath.show()
        self.world = world
        self.np = np
        self.hidden = 0
        self.count = Spawner.count
        #taskMgr.add(self.update,"SpawnerTask"+str(Spawner.count))
        Spawner.count = Spawner.count + 1
    def ammoCollide(self,object,mover):
        if self.hidden==1:
            return
        contactObject = object[0].getNode0()
        if object[0].getNode0().getName()=="Sphere":
            contactObject = object[0].getNode1()
        name = contactObject.getName()
        if name==mover.character.getName():
            mover.parent.overlay.wepAmmo[0] = mover.parent.overlay.wepAmmo[0]+10
        self.hidden = 1
        self.world.removeRigidBody(self.np.node())
        self.physrep.hide()
        taskMgr.doMethodLater(30,self.regen,'ammoRegen'+str(self.count))
        return
    def regen(self,task):
        self.hidden = 0
        self.world.attachRigidBody(self.np.node())
        self.physrep.show()
    def trap1Collide(self,object,mover):
        if self.hidden==1:
            return
        contactObject = object[0].getNode0()
        if object[0].getNode0().getName()=="Sphere":
            contactObject = object[0].getNode1()
        name = contactObject.getName()
        if name==mover.character.getName():
            mover.parent.overlay.wepAmmo[1] = mover.parent.overlay.wepAmmo[1]+10
        self.hidden = 1
        self.world.removeRigidBody(self.np.node())
        self.physrep.hide()
        taskMgr.doMethodLater(30,self.regen,'trap1Regen'+str(self.count))
        return
    def trap2Collide(self,object,mover):
        if self.hidden==1:
            return
        contactObject = object[0].getNode0()
        if object[0].getNode0().getName()=="Sphere":
            contactObject = object[0].getNode1()
        name = contactObject.getName()
        if name==mover.character.getName():
            mover.parent.overlay.wepAmmo[2] = mover.parent.overlay.wepAmmo[2]+10
        self.hidden = 1
        self.world.removeRigidBody(self.np.node())
        self.physrep.hide()
        taskMgr.doMethodLater(30,self.regen,'trap2Regen'+str(self.count))
        return
    def update(self, task):
        if not self.physrep.getParent()==render:
            print "DEAD!"
        return task.cont
    