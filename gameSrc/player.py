import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update  functions
import math,sys
from math import sin,cos,atan2,fabs,pow,sqrt
import time
import collision
import threading
from model import Model
from human import Projectile

class Player():
    model = 0
    counter = 0
    def __init__(self,ppos):
        if not Player.model:
            Player.model = Model("../assets/3d/Actors/robot_rig_basic_coll.egg")
            Player.model.modelRoot.find("**/body_coll").show()
        self.instance = Player.model.createInstance(pos=ppos)
        
        self.velocity = (0,0,0)
        self.prevTime = 0
        taskMgr.add(self.fpMove,"moveTask")
        
        self.projectiles = list()
        self.projTime = 0.0
        
        pnode = ModelRoot("player")
        self.player = render.attachNewNode(pnode)
        pc = self.player.attachNewNode(CollisionNode("playerCollision"))
        pc.node().addSolid(CollisionRay(0,0,-1,0,0,1))
        self.playerCnode = pc
        
        self.id = Player.counter
        Player.counter = Player.counter + 1
        
    def fpMove(self,task):
        #CONSTANTS
        ACCELERATION =  0.6
        MINDISTANCE =   150
        MAXSPEED =      100
        THROWPERIOD =   5.0
        
        #Function    
        dt = task.time-self.prevTime
        self.instance.setZ(self.instance.getZ())
        
        self.prevTime = task.time
        target = camera
        targetPos = target.getPos()
        pos = self.instance.getPos()
        vector2Target = self.normalize(targetPos - pos)
        
        #notarget = 0
        #if notarget == 1:
        #    return task.cont
        
        #gogo trigonometry
        angle = 90 + ( atan2(vector2Target[1],vector2Target[0])*180 / math.pi )
        angle2 = ( atan2(-vector2Target[2],sqrt(pow(vector2Target[1], 2) + pow(vector2Target[0], 2)))*180 / math.pi )
        self.instance.setH(angle)
        self.instance.setP(angle2)
        #curSpeed = sqrt(pow(self.velocity[0],2)+pow(self.velocity[1],2)+pow(self.velocity[2],2))
        #Use Distance formula, if further than MINDISTANCE, keep moving, otherwise stop 
        distance = sqrt(pow(target.getX()-self.instance.getX(),2)+pow(target.getY()-self.instance.getY(),2)+pow(target.getZ()-self.instance.getZ(),2))
        if(distance<MINDISTANCE):
            ACCELERATION = 0.0
        #get the velocity
        self.velocity = (self.velocity[0] + ACCELERATION * vector2Target[0], self.velocity[1] + ACCELERATION * vector2Target[1], self.velocity[2] + ACCELERATION * vector2Target[2]) 
        self.velocity = (min(MAXSPEED,self.velocity[0]),min(MAXSPEED,self.velocity[1]),min(MAXSPEED,self.velocity[2]))
        #get displacement
        dis = (self.velocity[0]*dt,self.velocity[1]*dt,self.velocity[2]*dt)
        #update position
        self.player.setPos(pos[0]+dis[0],pos[1]+dis[1],pos[2]+dis[2])
        self.instance.setPos(self.player.getX(),self.player.getY(),self.player.getZ())
        #if self.id == 0:
        #    print pos[0]+dis[0]
        #    print pos[1]+dis[1]
        #    print pos[2]+dis[2]
        #    print str(self.id) + " Z Displacement:" + str(dis[2]) + " distance:" + str(distance)
        self.projTime += dt
        if self.projTime >= THROWPERIOD:
            self.projTime -= THROWPERIOD
            self.projectiles.append(Projectile(self.player.getPos(),deg2Rad(180+angle),deg2Rad(angle2),self,self.velocity))
        return task.cont
    def normalize(self, vector):
        return vector / sqrt(pow(vector[0],2) + pow(vector[1], 2) + pow(vector[2], 2))
    def die(self,event):
        base.cTrav.removeCollider(self.wheelsphere)
        self.instance.node().getChild(0).removeChild(0)
        print "Computer player eliminated!"