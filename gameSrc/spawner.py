import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update  functions
import math,sys

import collision

class Spawner():
	def __init__(self,ppos,model):
		self.model = model
		self.physrep = model.createInstance(pos=ppos)
		self.pos = ppos
