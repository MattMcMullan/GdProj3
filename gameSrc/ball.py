from direct.task import Task
from math import sin, cos
from pandac.PandaModules import deg2Rad
import math, sys

class Ball():
    def __init__(self, parent):
        
        self.parent = parent
        self.prevTime = 0
        
        self.keymap = {"m1": 0}
        parent.accept("mouse1", self.setKey, ["m1", 1])
        
        taskMgr.add(self.throw, "throw")
        
    def setKey(self, key, value):
        self.keymap[key] = value
        
    def throw(self, task):
        if self.keymap["m1"] == 1:
            print "throw!"
            self.keymap["m1"] = 0
            dt = task.time-self.prevTime
            self.prevTime = self.prevTime - task.time
            direction = -1
            velocity = 150 * self.parent.overlay.momPercent * .01
            pos = self.parent.player.getPos()
            h = deg2Rad(camera.getH())
            p = deg2Rad(camera.getP())
            dir = (-cos(p)*sin(h)*direction, cos(p)*cos(h)*direction, sin(p)*direction)
            dx = sin(h+math.pi/2)
            dy = cos(h+math.pi/2)
            #get the velocity
            vel = (dir[0]*velocity,dir[1]*velocity,dir[2]*velocity)
            #get displacement
            dis = (vel[0]*dt,vel[1]*dt,vel[2]*dt)
            #set the new position
            self.parent.player.setPos(pos[0]+dis[0],pos[1]+dis[1],pos[2]+dis[2])
            #self.parent.player.setPos(10,10,10)
            
        return task.cont