import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update  functions
import math,sys

from player import Player
from spawner import Spawner
from model import Model

def extractPositions(env,prefix):
    positions = list()
    index = 1
    while 1:
        node = env.find("**/"+prefix+str(index))
        if node.getNumNodes()<1:
            return positions
        positions.append(node.getPos())
        node.detachNode()
        index = index + 1

def loadPlayers(env):
    players = list()
    for ppos in extractPositions(env,"PlayerSpawn"):
        players.append(Player(ppos))
    return players

def loadTrapAs(env):
    model = Model("../assets/3d/Actors/beartrap1",scale=5)
    traps = list()
    for ppos in extractPositions(env,"SpawnTrapA"):
        traps.append(Spawner(ppos,model))
    return traps
    
def loadTrapBs(env):
    model = Model("../assets/3d/Actors/claw1",scale=5)
    traps = list()
    for ppos in extractPositions(env,"SpawnTrapB"):
        traps.append(Spawner(ppos,model))
    return traps
    
def loadAmmo(env):
    model = Model("GrassCube",scale=5)
    traps = list()
    for ppos in extractPositions(env,"SpawnAmmo"):
        traps.append(Spawner(ppos,model))
    return traps


def listNodes(env,prefix):
    nodes = list()
    index = 1
    while 1:
        node = env.find("**/"+prefix+str(index))
        if node.getNumNodes()<1:
            return nodes
        nodes.append(node)
        index = index + 1

def loadColBoxes(env):
    # traverse through the collision geometry
    for np in listNodes(env,"Collision_box_"):
        geom = np.node().getGeom(0)
        # get the minimum and maximum points
        vdata = geom.getVertexData()
        vertices = GeomVertexReader(vdata,'vertex')
        xmin = -9999
        ymin = -9999
        zmin = -9999
        xmax = 9999
        ymax = 9999
        zmax = 9999
        while not vertices.isAtEnd():
            vertex = vertices.getData3f()
            xmin = min(xmin,vertex[0])
            ymin = min(ymin,vertex[1])
            zmin = min(zmin,vertex[2])
            xmax = max(xmax,vertex[0])
            ymax = max(ymax,vertex[1])
            zmax = max(zmax,vertex[2])
        # get rid of the useless geometry
        np.detachNode()
        np.removeNode()
        # use the points to construct collision boxes
        vmin = LPoint3(xmin,ymin,zmin)
        vmax = LPoint3(xmax,ymax,zmax)
        
        cbox = CollisionBox(vmin,vmax)
        cnode = CollisionNode("EnvCollide")
        cnode.addSolid(cbox)
        env.node().addChild(cnode)
    extractPositions(env,"collision_boxs_")
