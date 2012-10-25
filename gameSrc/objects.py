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
    