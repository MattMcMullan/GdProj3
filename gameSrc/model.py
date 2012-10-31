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
        """__init__
        parameters:
            self
            fname: path to the model file
            scale=1: optional scaling factor for the model
        returns:
            none
        Description:
            Loads a model from a file and makes it ready for instancing.
            Also applies node optimization and batches the static models.
        """
        if Model.combiner == 0:
            Model.combiner = NodePath(RigidBodyCombiner("rbc"))
            Model.combiner.reparentTo(render)
        self.modelRoot = collision.loadAndPositionModelFromFile(fname,scale,show=0)
        self.modelRoot.flattenStrong()
        self.modelRoot.reparentTo(Model.combiner)
        #print self.modelRoot.ls()
    def createInstance(self,scale=1,pos=(0,0,0),hpr=(0,0,0),show=1):
        """createInstance
        parameters:
            self
            scale=1: optional scaling factor for this instance
            pos=(0,0,0): optional position to place the instance at
            show=1: optional flag to determine whether or not it should be visible
        returns:
            none
        Description:
            Creates an instance of the model with specified transforms
        """
        nnode = Model.combiner.attachNewNode("instance")
        copy = self.modelRoot.instanceTo(nnode)
        copy = nnode
        copy.reparentTo(render)
        nnode.setPos(LVecBase3(pos[0],pos[1],pos[2]))
        nnode.setHpr(hpr)
        nnode.setScale(scale)
        if (not show):
            nnode.hide()
        return nnode
    def createCopy(self,scale=1,pos=(0,0,0),hpr=(0,0,0),show=1):
        """createCopy
        parameters:
            self
            scale=1: optional scaling factor for this instance
            pos=(0,0,0): optional position to place the instance at
            show=1: optional flag to determine whether or not it should be visible
        returns:
            none
        Description:
            Creates a copy of the model with specified transforms
        """
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