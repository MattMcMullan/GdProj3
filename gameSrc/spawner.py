import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update  functions
import math,sys

import collision

class Spawner():
    count = 0
    def __init__(self,ppos,model,collisionHandler):
        self.model = model
        self.physrep = model.createInstance(pos=ppos)
        self.pos = ppos
        
        spawnSphere = CollisionSphere((self.pos[0], self.pos[1], self.pos[2] + 13), 14)
        spawnNode = CollisionNode("spawner" + str(Spawner.count))
        spawnNode.addSolid(spawnSphere)
        spawnNodePath = render.attachNewNode(spawnNode)
        #base.cTrav.addCollider(spawnNodePath,collisionHandler)
        spawnNodePath.show()
        
        #taskMgr.add(self.update,"SpawnerTask"+str(Spawner.count))
        Spawner.count = Spawner.count + 1
    def update(self, task):
        if not self.physrep.getParent()==render:
            print "DEAD!"
        return task.cont
    