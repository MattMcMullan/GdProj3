import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update  functions
import math,sys
import collision

class Model():
	def __init__(self, fname,scale=1):
		self.modelRoot = collision.loadAndPositionModelFromFile(fname,scale,show=0)
		print self.modelRoot.ls()
	def createInstance(self,scale=1,pos=(0,0,0),hpr=(0,0,0),show=1):
		nnode = render.attachNewNode("instance")
		copy = self.modelRoot.instanceTo(nnode)
		copy = nnode
		copy.reparentTo(render)
		nnode.setPos(pos)
		nnode.setHpr(hpr)
		nnode.setScale(scale)
		if (not show):
			nnode.detachNode()
		return nnode
	def createCopy(self,scale=1,pos=(0,0,0),hpr=(0,0,0),show=1):
		nnode = self.modelRoot.copyTo(render)
		nnode.setPos(pos)
		nnode.setHpr(hpr)
		nnode.setScale(scale)
		if (not show):
			nnode.detachNode()
		return nnode
	def addCollisions(self,handler,name):
		paths = self.modelRoot.find_all_matches(name)
		print type(paths)