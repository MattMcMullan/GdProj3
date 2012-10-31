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
from model import Model
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletCharacterControllerNode

mousePos       = [0,0] 
mousePrevPos    = [0,0] 
class Projectile():
    model = 0
    index = 0
    def __init__(self, ppos, h, p, parent, parentVel, world, worldNP):
        if Projectile.model==0:
            Projectile.model = Model("../assets/3d/Actors/ball_proj1.egg")
        self.instance = Projectile.model.createInstance(pos=ppos,hpr=(h,p,0))
        pos = ppos
        shape = BulletSphereShape(5)
        self.np = worldNP.attachNewNode(BulletRigidBodyNode('Sphere'))
        #np.node().setMass(1.0)
        self.np.node().addShape(shape)
        #np.node().addShape(shape, TransformState.makePos(Point3(0, 1, 0)))
        self.np.setPos(pos)
        self.np.setCollideMask(BitMask32.allOn())
        world.attachRigidBody(self.np.node())
        self.sphere = self.np.node()
        self.instance.reparentTo(self.np)
        
        dir = (-cos(p)*sin(h), cos(p)*cos(h), sin(p))
        self.vel = parentVel
        self.vel = map(lambda i: dir[i]*100, range(3))
        self.index = Projectile.index
        self.parent = parent
        Projectile.index = Projectile.index + 1
        taskMgr.add(self.move,"Proj"+str(Projectile.index)+"MoveTask")
        self.prevTime = 0
        self.lifeTime = 0
        self.TIMEDLIFE = 120
    def move(self,task):
        dt = task.time-self.prevTime
        #If the projectile exceeds its maximum lifetime or burns out on the arena bounds -
        self.lifeTime += dt
        if(self.lifeTime >= self.TIMEDLIFE):
            #kill projectile
            self.instance.removeNode()
            self.parent.projectiles.remove(self)
            #print "Projectile removed"
        if(self.lifeTime < self.TIMEDLIFE):
            #get the position
            pos = self.instance.getPos()
            #get the displacement
            dis = (self.vel[0]*dt,self.vel[1]*dt,self.vel[2]*dt)
            #set the new position
            self.np.setPos(pos[0]+dis[0],pos[1]+dis[1],pos[2]+dis[2])
            return task.cont
            
class floatTrap():
    model = 0
    index = 0
    def __init__(self, ppos):
        if floatTrap.model==0:
            floatTrap.model = Model("../assets/3d/Actors/beartrap2.egg")
        self.instance = floatTrap.model.createInstance(pos=ppos,hpr=(0,0,0))
        self.index = floatTrap.index
        floatTrap.index = floatTrap.index + 1
            
class Human():
    def __init__(self,parent, world, worldNP):
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
        self.human = collision.loadAndPositionModelFromFile("../assets/3d/Actors/robot_rig_basic_coll.egg",scale=.07,show=0)
        self.human.flattenLight()
        print self.human.ls()
        #self.human.node().getChild(0).removeChild(0)
        self.human.setH(camera.getH()+180)
        campos = self.human.getPos()
        campos[2] = campos[2]-5
        camera.lookAt(campos)
        
        #vmin = LPoint3()
        #vmax = LPoint3()
        #self.human.calcTightBounds(vmin,vmax)
        
        #cbox = CollisionBox(vmin,vmax)
        #cnode = CollisionNode("HumanCollide")
        #cnode.addSolid(cbox)
        #env.node().getChild(0).addChild(cnode)
        #path = self.human.attachNewNode(cnode)
        
        #print self.human.ls()
        
        pnode = ModelRoot("player")
        self.player = render.attachNewNode(pnode)
        pc = self.player.attachNewNode(CollisionNode("playerCollision"))
        pc.node().addSolid(CollisionRay(0,0,-1,0,0,1))
        self.playerCnode = pc
        self.player.setPos(0,0,1)
        
    def fpMove(self,task):
        dt = task.time-self.prevTime
        #self.human.setZ(self.player.getZ()-.5)
        #if not self.parent.editMode:
        camera.setPos(self.player.getPos()+(0,0,1))
        damp = (1.-(.2*dt))
        self.vel = map(lambda x: damp*x, self.vel)
        self.prevTime = task.time
        pos = self.player.getParent().getPos()
        delta = 10*dt
        h = deg2Rad(camera.getH())
        p = deg2Rad(camera.getP())
        if self.keymap["up"]:
            dir = (-cos(p)*sin(h), cos(p)*cos(h), sin(p))
            self.vel = map(lambda i: self.vel[i]+dir[i]*delta, range(3))
        if self.keymap["down"]:
            dir = (-cos(p)*sin(h), cos(p)*cos(h), sin(p))
            self.vel = map(lambda i: self.vel[i]-dir[i]*delta, range(3))
        if self.keymap["m1"]:
            weapon = self.parent.overlay.wepCounter
            if self.parent.overlay.wepAmmo[weapon] > 0:
                self.parent.overlay.changeAmmo(weapon, -1)
                if weapon == 0:
                    self.launch()
                    dir = (-cos(p)*sin(h), cos(p)*cos(h), sin(p))
                    self.vel = map(lambda i: self.vel[i]-dir[i]*100, range(3))
                elif weapon == 1:
                    self.placeFloatTrap()
            self.keymap["m1"] = 0
        self.character.setAngularMovement(0)
        self.character.setLinearMovement(LVector3(self.vel[0],self.vel[1],self.vel[2]),True)
        #get displacement
        dis = (self.vel[0]*dt,self.vel[1]*dt,self.vel[2]*dt)
        #set the new position
        self.player.setPos(pos[0]+dis[0],pos[1]+dis[1],pos[2]+dis[2])
        self.human.setX(self.player.getX()+sin(deg2Rad(camera.getH())+math.pi))
        self.human.setY(self.player.getY()-cos(deg2Rad(camera.getH())+math.pi))
        return task.cont
    def launch(self):
        self.projectiles.append(Projectile(self.player.getPos(),deg2Rad(camera.getH()),deg2Rad(camera.getP()),self,self.vel, self.world, self.worldNP))
    def placeFloatTrap(self):
        self.floatTraps.append(floatTrap(self.player.getPos())) 
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
        
        camera.setP(camera.getP()+75*move[1])
        camera.setH(camera.getH()-75*move[0])
        
        self.human.setH(camera.getH()+180)
        self.human.setX(self.player.getX()+sin(deg2Rad(camera.getH()+180)))
        self.human.setY(self.player.getY()-cos(deg2Rad(camera.getH()+180)))
        
        return Task.cont
    def bulletInit(self,world,pos):
        oldpath = self.human.find("**/body_coll")
        shape = BulletSphereShape(oldpath.node().getSolid(0).getRadius())
        self.character = BulletCharacterControllerNode(shape, 0.4, 'Human')
        self.characterNP = render.attachNewNode(self.character)
        self.characterNP.setPos(pos[0],pos[1],pos[2])
        self.character.setGravity(0)
        self.human.setPos(pos)
        self.human.reparentTo(self.characterNP)
        self.player.setPos(pos)
        self.player.reparentTo(self.characterNP)
        self.characterNP.setCollideMask(BitMask32.allOn())
        
        world.attachCharacter(self.character)
        #node = BulletRigidBodyNode('PlayerCollide')
        #node.setMass(1.0)
        #node.addShape(shape)
        #np = render.attachNewNode(node)
        #np.setPos(0,0,-2)
        #world.attachRigidBody(node)
        #self.human.reparentTo(np)
        #self.player.reparentTo(np)
        #camera.reparentTo(self.human)
    def die(self,event):
        base.cTrav.removeCollider(self.wheelsphere)
        self.human.node().getChild(0).removeChild(0)
        self.filters.setInverted()
        print "You Died!"