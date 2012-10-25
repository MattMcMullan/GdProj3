import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update  functions
import math,sys

import collision
from model import Model

class Player():
    model = 0
    def __init__(self,ppos):
        if not Player.model:
            Player.model = Model("../assets/3d/testing assets/robot rig3.egg")
        self.instance = Player.model.createInstance(pos=ppos)
