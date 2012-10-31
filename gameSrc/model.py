import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update  functions
from panda3d.core import RigidBodyCombiner, NodePath
import math,sys
import collision

class Model():
    combiner = 0
    def __init__(self, fname,scale=1):
        if Model.combiner == 0:
            Model.combiner = NodePath(RigidBodyCombiner("rbc"))
            Model.combiner.reparentTo(render)
        self.modelRoot = collision.loadAndPositionModelFromFile(fname,scale,show=0)
        self.modelRoot.flattenStrong()
        self.modelRoot.reparentTo(Model.combiner)
        #print self.modelRoot.ls()
    def createInstance(self,scale=1,pos=(0,0,0),hpr=(0,0,0),show=1):
        nnode = Model.combiner.attachNewNode("instance")
        copy = self.modelRoot.instanceTo(nnode)
        copy = nnode
        copy.reparentTo(render)
        nnode.setPos(LVecBase3(pos[0],pos[1],pos[2]))
        nnode.setHpr(hpr)
        nnode.setScale(scale)
        if (not show):
            nnode.detachNode()
        return nnode
    def createCopy(self,scale=1,pos=(0,0,0),hpr=(0,0,0),show=1):
        nnode = self.modelRoot.copyTo(Model.combiner)
        nnode.setPos(pos)
        nnode.setHpr(hpr)
        nnode.setScale(scale)
        if (not show):
            nnode.detachNode()
        return nnode
    def addCollisions(self,handler,name):
        paths = self.modelRoot.find_all_matches(name)
        print type(paths)