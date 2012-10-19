import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update  functions
import math,sys

def setupAmbientLight(name="ambientLight",color=.25,show=1):
    """setupAmbientLight
    parameters:
        name: name of the AmbientLight
        color: color of the AmbientLight. Can be a scalar or tuple of length 3-4
        show: should this be active from the get-go
    return:
        NodePath to an AmbientLight
    """
    # make the color be of the right form
    if not type(color)==tuple:
        color = (color,color,color,1.)
    if len(color) == 3:
        color = (color[0],color[1],color[2],1.)
    # create the light
    light = AmbientLight(name)
    light.setColor(color)
    # create a NodePath, and attach it directly into the scene
    lightNp = render.attachNewNode(light)
    if show:
        # the node that calls setLight is what's illuminated by the given light
        # you can use clearLight() to turn it off
        render.setLight(lightNp)
    return lightNp

def loadModelSpotlightByName(model,originName,targetName,newName,color=1,show=1):
    """loadModelCollisionsByName
    parameters:
        model: the panda node
        originName: The name of the collision node that is the origin of the light
        targetName: The name of the collision node that defines the direction of the light
        color: The color of the light. Can be a scalar, 3, or 4 component tuple
        newName: the name you want to call the finished light
        show: whether or not to set the show attribute
    returns:
        NodePath to Spotlight
    example:
        loadModelCollisionsByName(model,collider,"BlackKnightCollision")
    """
    #find the origin node in the model
    origin = model.find("**/"+originName)
    if origin.getNumNodes()<1:
        print "\nERROR:\n\tFailed to find "+originName+" in "+model.getName()+"\n"
        return
    #find the target node in the model
    target = model.find("**/"+targetName)
    if target.getNumNodes()<1:
        print "\nERROR:\n\tFailed to find "+targetName+" in "+model.getName()+"\n"
        return
    #Create the spotlight
    slight = Spotlight(newName)
    #Make color into a VBase4 to set the color with
    if not type(color)==VBase4:
        if type(color)==tuple:
            if len(color)==4:
                color = VBase4(color[0],color[1],color[2],color[3])
            else:
                color = VBase4(color[0],color[1],color[2],1)
        else:
            color = VBase4(color,color,color,1)
    slight.setColor(color)
    #Setup the lense
    lens = PerspectiveLens()
    slight.setLens(lens)
    #Create a NodePath for it
    slnp = render.attachNewNode(slight)
    #Set the position and orientation
    slnp.setPos(origin.node().getSolid(0).getCollisionOrigin()+origin.getPos())
    print target.getParent().getPos()
    dest = target.node().getSolid(0).getCollisionOrigin()+target.getPos()
    slnp.lookAt(dest.getX(),dest.getY(),dest.getZ())
    slnp.reparentTo(model)
    if show:
        render.setLight(slnp)
    return slnp
    