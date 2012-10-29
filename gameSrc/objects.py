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
    model = Model("../assets/3d/testing assets/GrassCube.egg",scale=5)
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

def loadColBoxes(env, handler):
    # traverse through the collision geometry
    for np in listNodes(env,"Collision_box_"):
        geom = np.node().getGeom(0)
        # get the minimum and maximum points
        vdata = geom.getVertexData()
        vertices = GeomVertexReader(vdata,'vertex')
        mins = [-9999 for i in range(3)]
        maxs = [9999 for i in range(3)]
        while not vertices.isAtEnd():
            vertex = vertices.getData3f()
            mins = [min(mins[i], vertex[i]) for i in range(3)]
            maxs = [max(maxs[i], vertex[i]) for i in range(3)]
        # get rid of the useless geometry
        np.removeNode()
        # use the points to construct collision boxes
        vmin = LPoint3(mins[0],mins[1],mins[2])
        vmax = LPoint3(maxs[0],maxs[1],maxs[2])
        
        cbox = CollisionBox(vmin,vmax)
        cnode = CollisionNode("EnvCollide")
        cnode.addSolid(cbox)
        #env.node().getChild(0).addChild(cnode)
        path = env.find("").attachNewNode(cnode)
        handler.addCollider(path,env)
    extractPositions(env,"collision_boxs_")
    envCollides = env.findAllMatches("**/EnvCollide")
    for i in range(envCollides.getNumPaths()):
        envCollide = envCollides.getPath(i)
        envCollide.show()
    print env.ls()
    