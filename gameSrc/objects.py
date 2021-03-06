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

from player import Player
from spawner import Spawner
from model import Model
import lights

def extractPositions(env,prefix,index=1):
    positions = list()
    while 1:
        node = env.find("**/"+prefix+str(index))
        if node.getNumNodes()<1:
            return positions
        positions.append(node.getPos())
        node.detachNode()
        index = index + 1

def loadPlayers(env,world,worldNP):
    players = list()
    for ppos in extractPositions(env,"PlayerSpawn",2):
        players.append(Player(ppos,world,worldNP))
    return players

def loadTrapAs(env, world, worldNP):
    model = Model("../assets/3d/Actors/beartrap2",scale=5)
    traps = list()
    for ppos in extractPositions(env,"SpawnTrapA"):
        traps.append(Spawner(ppos,model, world, worldNP))
    return traps
    
def loadTrapBs(env, world, worldNP):
    model = Model("../assets/3d/Actors/claw3",scale=5)
    traps = list()
    for ppos in extractPositions(env,"SpawnTrapB"):
        traps.append(Spawner(ppos,model,world, worldNP))
    return traps
    
def loadAmmo(env, world, worldNP):
    model = Model("../assets/3d/Actors/ball_proj2",scale=5)
    traps = list()
    for ppos in extractPositions(env,"SpawnAmmo"):
        traps.append(Spawner(ppos,model,world, worldNP))
    return traps

def loadSpotlights(env):
    index = 1
    ret = 1
    while not ret==0:
        ret = lights.loadModelSpotlightByName(env,"SpotLight"+str(index),"DirLight"+str(index),"Light"+str(index))
        index = index + 1

def listNodes(env,prefix):
    nodes = list()
    index = 1
    while 1:
        node = env.find("**/"+prefix+str(index))
        if node.getNumNodes()<1:
            return nodes
        nodes.append(node)
        index = index + 1
def genBulletBoxes(env,world):
    boxes = list()
    for np in listNodes(env,"Collision_box_"):
        geom = np.node().getGeom(0)
        # get the minimum and maximum points
        vdata = geom.getVertexData()
        vertices = GeomVertexReader(vdata,'vertex')
        vmin = LPoint3()
        vmax = LPoint3()
        np.calcTightBounds(vmin,vmax)
        #Create the bullet box with center at (0,0)
        norm = vmax-vmin
        hnorm = LVecBase3(norm[0]*.5,norm[1]*.5,norm[2]*.5)
        shape = BulletBoxShape(hnorm)
        # create the surrounding nodes
        node = BulletRigidBodyNode('env')
        node.addShape(shape)
        enp = env.attachNewNode(node)
        enp.setPos(vmin+hnorm)
        # attach it to the world and save it for later
        world.attachRigidBody(node)
        boxes.append(enp.node())
        # clean up the environment higherarchy
        np.removeNode()
    return boxes
def loadColBoxes(env, handler):
    # traverse through the collision geometry
    for np in listNodes(env,"Collision_box_"):
        geom = np.node().getGeom(0)
        # get the minimum and maximum points
        vdata = geom.getVertexData()
        vertices = GeomVertexReader(vdata,'vertex')
        # get the transform
        transform = np.getTransform().getMat()
        # init the mins and maxs
        vmin = LPoint3()
        vmax = LPoint3()
        np.calcTightBounds(vmin,vmax)
        #mins = [-9999 for i in range(3)]
        #maxs = [9999 for i in range(3)]
        #while not vertices.isAtEnd():
        #    vertex = transform.xformVecGeneral(vertices.getData3f())
        #    
        #    mins = [min(mins[i], vertex[i]) for i in range(3)]
        #    maxs = [max(maxs[i], vertex[i]) for i in range(3)]
        # get rid of the useless geometry
        np.removeNode()
        # use the points to construct collision boxes
        #vmin = LPoint3(mins[0],mins[1],mins[2])
        #vmax = LPoint3(maxs[0],maxs[1],maxs[2])
        
        cbox = CollisionBox(vmin,vmax)
        cnode = CollisionNode("EnvCollide")
        cnode.addSolid(cbox)
        #env.node().getChild(0).addChild(cnode)
        path = env.attachNewNode(cnode)
        handler.addCollider(path,env)
    extractPositions(env,"collision_boxs_")
    envCollides = env.findAllMatches("**/EnvCollide")
    for i in range(envCollides.getNumPaths()):
        envCollide = envCollides.getPath(i)
        envCollide.show()
        print "SHOWING!!!!!!!!!!!!!!!!!!!!!!!"
    #print env.ls()
    