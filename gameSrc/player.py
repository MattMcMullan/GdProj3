import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update  functions
import math,sys
from math import sin,cos,atan2
import time
import collision
import threading
from model import Model

class Player():
    model = 0
    counter = 0
    def __init__(self,ppos):
        if not Player.model:
            Player.model = Model("../assets/3d/testing assets/robot rig3.egg")
        self.instance = Player.model.createInstance(pos=ppos)
        
        self.prevTime = 0        
        taskMgr.add(self.fpMove,"moveTask")
        
        pnode = ModelRoot("player")
        self.player = render.attachNewNode(pnode)
        pc = self.player.attachNewNode(CollisionNode("playerCollision"))
        pc.node().addSolid(CollisionRay(0,0,-1,0,0,1))
        self.playerCnode = pc
        
        self.id = Player.counter
        Player.counter = Player.counter + 1
         
        
    def fpMove(self,task):
        dt = task.time-self.prevTime
        self.instance.setZ(self.instance.getZ())
        
        self.prevTime = task.time
        targetPos = camera.getPos()
        pos = self.instance.getPos()
        h = deg2Rad(self.instance.getH())
        p = deg2Rad(self.instance.getP())
        #notarget = 0
        #if notarget == 1:
        #    return task.cont
        angle = 90 + ( atan2(targetPos[1]-pos[1],targetPos[0]-pos[0])*180 / math.pi )
        self.instance.setH(angle)
        velocity = 1
        direction = -angle
        dir = (-cos(p)*sin(h)*direction, cos(p)*cos(h)*direction, sin(p)*direction)
        #get the velocity
        vel = (dir[0]*velocity,dir[1]*velocity,dir[2]*velocity)
        #get displacement
        dis = (vel[0]*dt,vel[1]*dt,vel[2]*dt)
        self.player.setPos(pos[0]+dis[0],pos[1]+dis[1],pos[2]+dis[2])
        self.instance.setX(self.player.getX())
        self.instance.setY(self.player.getY())
        if self.id == 0:
            print str(self.id) + " " + str(pos[2])
        return task.cont
        
    def die(self,event):
        base.cTrav.removeCollider(self.wheelsphere)
        self.instance.node().getChild(0).removeChild(0)
        print "Computer player eliminated!"
