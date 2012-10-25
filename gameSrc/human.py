import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update  functions
import math,sys
from math import sin
from math import cos
import collision

class Human():
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
        #self.human = self.parent.human
        
        self.human = collision.loadAndPositionModelFromFile("../assets/3d/testing assets/robot rig3.egg",scale=.07,show=0)
        self.human.node().getChild(0).removeChild(0)
        self.human.setH(camera.getH()+180)
        campos = self.human.getPos()
        campos[2] = campos[2]-5
        camera.lookAt(campos)
        print self.human.ls()
        
        pnode = ModelRoot("player")
        self.player = render.attachNewNode(pnode)
        pc = self.player.attachNewNode(CollisionNode("playerCollision"))
        pc.node().addSolid(CollisionRay(0,0,-1,0,0,1))
        self.playerCnode = pc
        self.player.setPos(0,0,1)
        
    def fpMove(self,task):
        dt = task.time-self.prevTime
        self.human.setZ(self.player.getZ()-.5)
        #if not self.parent.editMode:
        camera.setPos(self.player.getPos()+(0,0,1))
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
        pos = self.player.getPos()
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
        self.player.setPos(pos[0]+dis[0],pos[1]+dis[1],pos[2]+dis[2])
        self.human.setX(self.player.getX()+sin(deg2Rad(camera.getH())+math.pi))
        self.human.setY(self.player.getY()-cos(deg2Rad(camera.getH())+math.pi))
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
        
        self.human.setH(camera.getH()+180)
        self.human.setX(self.player.getX()+sin(deg2Rad(camera.getH()+180)))
        self.human.setY(self.player.getY()-cos(deg2Rad(camera.getH()+180)))
        
        return Task.cont
    def die(self,event):
        base.cTrav.removeCollider(self.wheelsphere)
        self.human.node().getChild(0).removeChild(0)
        self.filters.setInverted()
        print "You Died!"
