import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update  functions
import math,sys

def initializeCollisions():
    """initializeCollisions
    parameters:
        none
    returns:
        CollisionHandlerEvent
        sets base.cTrav to a CollisionTraverser
    """
    base.cTrav = CollisionTraverser('traverser name')
    collisionHandler = CollisionHandlerEvent()
    collisionHandler.addInPattern('ate-%in')
    collisionHandler.addInPattern('%fn-into-%in')
    collisionHandler.addOutPattern('%fn-out-%in')
    collisionHandler.addAgainPattern('%fn-again-%in')
    return collisionHandler

def loadAndPositionModelFromFile(fname,scale=(1,1,1), pos=(0,0,0),hpr=(0,0,0), show=1):
    """loadAndPositionModelFromFile
    parameters:
        fname: name of the file
        scale: scale of the model, scalar or tuple
        pos: new position for the model, scalar or tuple
        hpr: new rotation of the model, scalar or tuple
        show: should this node be rendering right from the get-go?
    returns:
        NodePath to ModelRoot
    example:
        loadAndPositionModelFromFile("blackKnight",scale=.5,pos=(1,2,3))
    """
    # load the model from the file
    model =  loader.loadModel(fname)
    # make scalars into tuples when need be
    if not type(scale)==tuple:
        scale = (scale,scale,scale)
    if not type(pos)==tuple:
        if not type(pos)==Point3:
            pos = (pos,pos,pos)
        else:
            print "NP3"
            pos = (pos.getX(),pos.getY(),pos.getZ())
    if not type(hpr)==tuple:
        hpr = (hpr,hpr,hpr)
    # position the model
    model.setPosHprScale(pos[0],pos[1],pos[2],hpr[0],hpr[1],hpr[2],scale[0],scale[1],scale[2])
    # make it render
    if show:
        model.reparentTo(render)
    return model;

def loadModelCollisionsByName(model,name,newName="",show=1):
    """loadModelCollisionsByName
    parameters:
        model: the panda node
        name: the name of the colision node in the file
        newName: the name you want to call the collider to detect the collision
        show: whether or not to set the show attribute
    returns:
        NodePath to CollisionNode
    example:
        loadModelCollisionsByName(model,"BlackKnightCollision")
    """
    colNode = model.find("**/"+name)
    if colNode.getNumNodes()<1:
        print "\nERROR:\n\tFailed to find "+name+" in "+model.getName()+"\nThe model contains...\n"
        print model.ls()
        return
    if colNode.node().isGeomNode():
        print "\nERROR:\n\t"+name+" in "+model.getName()+" is a geom node!\nThe model contains...\n"
        print model.ls()
        return 
    if newName=="":
        newName=name
    collider = model.attachNewNode(CollisionNode(newName))
    if show:
        collider.show()
    pos = colNode.getPos()
    collider.setPos(pos)
    collider.node().addSolid(colNode.node().getSolid(0))
    origin = colNode.node().getSolid(0).getCollisionOrigin()
    return collider

pickerRay=0
def pickerUpdate(task):
    """pickerUpdate
    Helper function. Do not use.
    """
    global pickerRay
    if base.mouseWatcherNode.hasMouse():
        mpos=base.mouseWatcherNode.getMouse()
        # this is what set our ray to shoot from the actual camera lenses off the 3d scene, passing by the mouse pointer position, making  magically hit in the 3d space what is pointed by it
        pickerRay.setFromLens(base.camNode, mpos.getX(),mpos.getY())
    return task.cont
def setupMousePicker(name,collisionHandler):
    """setupMousePicker
    parameters:
        name: name of the mouse picker CollisionObject
        collisionHandler: the CollisionHandler to associate it with
    returns:
        none
    """
    global pickerRay
    pickerNode=CollisionNode(name)
    pickerNP=base.camera.attachNewNode(pickerNode)
    pickerRay=CollisionRay()
    pickerNode.addSolid(pickerRay)
    base.cTrav.addCollider(pickerNP, collisionHandler)
    taskMgr.add(pickerUpdate, "pickerUpdate",sort=99999)
    