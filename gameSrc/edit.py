import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update  functions
from panda3d.bullet import BulletWorld
from direct.filter.CommonFilters import CommonFilters
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
import math,sys
from math import sin
from math import cos
from createcube import createCube

def spawnBox(name,pos=(0,0,0),scale=1,color=(1,1,1,0)):
    boxGeom = createCube(name+"Geom",color)
    boxNode = PandaNode(name+"Node")
    boxNode.addChild(boxGeom)
    boxRoot = ModelRoot(name)
    boxRoot.addChild(boxNode)
    box = render.attachNewNode(boxRoot)
    box.setScale(scale)
    #box.setPos(pos)
    return box
def attachUnitCollisionBox(model,name,show=1):
    solid = CollisionBox((0,0,0),.5,.5,.5)
    node = CollisionNode(name)
    node.addSolid(solid)
    np = model.attachNewNode(node)
    if show:
        np.show()
    np.setPos(model.getPos())
    return np