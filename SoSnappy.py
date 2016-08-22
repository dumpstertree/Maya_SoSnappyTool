'''
----------------------------
    
    Written By Zachary Collins
    August 2015
    
    dumpstertree.com
    dumpstertree@gmail.com
    @dumpstertree
    
----------------------------
'''

import maya.cmds as cmds
import maya.mel as mel
import random
import AdvancedUI as ui

import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kPluginCmdName = "soSnappy"
shelfName = "dumpstertree"
buttonName = "soSnappy"

UiName = "SOSNAPPY"
toolName = "so snappy"
headerHeight = 21
bodyHeight = 92

red		=[.8,.5,.5]
green	=[.5,.8,.5]
blue	=[.5,.5,.8]
black	=[.1,.1,.1]
white 	=[.9,.9,.9]


def start(direction):

	currentSelections = cmds.ls( sl=True, fl=1 )
	
	if (breaker(currentSelections) == False ):
		best = findHeight(currentSelections,direction[0],direction[1])
		moveHeight(currentSelections,direction[0],direction[1],best)
		ui.pulseAnimation( "mainUI_C", 1, .5, green)
	else :
		ui.flashAnimation("mainUI_C", 2, .07, black)
		ui.shakeAnimation(UiName, .15, 10)

def breaker(currentSelections):
	broken = False
	if currentSelections >= 1 :
		selectedVerts = cmds.polyEvaluate( vertexComponent=True )
		if len(currentSelections) != selectedVerts:
			cmds.warning("please select only verts; aborted")
			broken =True

	if len(currentSelections) < 2 :
		cmds.warning("please select at least 2 verts; aborted")
		broken =True
	return broken
def findHeight(currentSelections,posNeg,axis):
	currentBest = None
	
	for verts in currentSelections:
		vertPosition = cmds.pointPosition(str(verts),w=True)

		if (axis == "X"):
			xpos = vertPosition[0]
			if (posNeg == "-"):
				if (xpos < currentBest or currentBest == None):
					currentBest = xpos
			if (posNeg == "+"):
				if (xpos > currentBest or currentBest == None):
					currentBest = xpos
		if (axis == "Y"):
			ypos = vertPosition[1]
			if (posNeg == "-"):
				if (ypos < currentBest or currentBest == None):
					currentBest = ypos
			if (posNeg == "+"):
				if (ypos> currentBest or currentBest == None):
					currentBest = ypos
		if (axis == "Z"):
			zpos = vertPosition[2]
			if (posNeg == "-"):
				if (zpos < currentBest or currentBest == None):
					currentBest = zpos
			if (posNeg == "+"):
				if (zpos > currentBest or currentBest == None):
					currentBest = zpos
	return currentBest
def moveHeight(currentSelections,posNeg,axis,best):
	for verts in currentSelections:
		vertPosition = cmds.pointPosition(str(verts),w=True)
		
		if (axis == "X"):
			cmds.move(best,x=True,yz=False,a=True)

		if (axis == "Y"):
			cmds.move(best,y=True,xz=False,a=True)

		if (axis == "Z"):
			cmds.move(best,z=True,xy=False,a=True)

def UI_create():
	UI_checkforExisting()
	UI_createWindow()
	UI_createBody()
	UI_display()
def UI_checkforExisting():
	if cmds.window( UiName, exists=True):
		cmds.deleteUI ( UiName, window=True)
	    
	if cmds.windowPref( UiName, exists=True ):
		cmds.windowPref( UiName, remove=True )
def UI_createWindow():
	global white
	cmds.window(UiName, title="", minimizeButton=False, maximizeButton=False, sizeable=False, h=1, rtf=False, bgc=white)
def UI_createBody():
	global red
	global green
	global blue

	windowWidth = 140
	
	cmds.columnLayout("mainUI_C", parent=UiName)

	cmds.rowColumnLayout(numberOfColumns=3, cw=[(1, windowWidth * .15),(2, windowWidth * .7),(3, windowWidth * .15)], p="mainUI_C")
	cmds.separator(h=10,vis=True)
	cmds.text('title', label = "", align = "center", font = "boldLabelFont")
	cmds.separator(h=10,vis=True)
	cmds.separator(h=5,vis=False)


	cmds.rowColumnLayout(numberOfColumns=1, cw=[(1, windowWidth)], p="mainUI_C")
	cmds.separator(h=1,vis=True)

	cmds.rowColumnLayout(numberOfColumns=7, cw=[(1, windowWidth * .1),(2,windowWidth * .2),(3,windowWidth* .1),(4,windowWidth*.2),(5,windowWidth * .1),(6,windowWidth* .2),(7,windowWidth*.1)], p="mainUI_C")
	cmds.separator(h=10,vis=False)
	cmds.button(l="-X",h=windowWidth * .2, bgc=red, c=lambda arg: start(["-","X"]))
	cmds.separator(h=10,vis=False)
	cmds.button(l="+Y",h=windowWidth * .2, bgc=green, c=lambda arg: start(["+","Y"]))
	cmds.separator(h=10,vis=False)
	cmds.button(l="+X",h=windowWidth * .2, bgc=red, c=lambda arg: start(["+","X"]))
	cmds.separator(h=10,vis=False)

	cmds.rowColumnLayout(numberOfColumns=1, cw=[(1, windowWidth)], p="mainUI_C")
	cmds.separator(h=5,vis=False)

	cmds.rowColumnLayout(numberOfColumns=7, cw=[(1, windowWidth * .1),(2,windowWidth * .2),(3,windowWidth* .1),(4,windowWidth*.2),(5,windowWidth * .1),(6,windowWidth* .2),(7,windowWidth*.1)], p="mainUI_C")
	cmds.separator(h=10,vis=False)
	cmds.button(l="-Z",h=windowWidth * .2, bgc=blue, c=lambda arg: start(["-","Z"]))
	cmds.separator(h=10,vis=False)
	cmds.button(l="-Y",h=windowWidth * .2, bgc=green, c=lambda arg: start(["-","Y"]))
	cmds.separator(h=10,vis=False)
	cmds.button(l="+Z",h=windowWidth * .2, bgc=blue, c=lambda arg: start(["+","Z"]))
	cmds.separator(h=10,vis=False)

	cmds.rowColumnLayout(numberOfColumns=1, cw=[(1, windowWidth)], p="mainUI_C")
	cmds.separator(h=1,vis=True)
	cmds.separator(h=5,vis=False)
	cmds.text(label = "@dumpstertree", font = "smallPlainLabelFont", align = "center")
def UI_display():
	cmds.showWindow(UiName)   
	ui.openAnimation( UiName, 1, headerHeight, .2) 
	ui.textTypingAnimation( "title", toolName, .2) 
	ui.openAnimation( UiName, headerHeight, bodyHeight+headerHeight, .3)    

def cmdCreator():
    return OpenMayaMPx.asMPxPtr( scriptedCommand() ) 
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerCommand( kPluginCmdName, cmdCreator )
        createShelf()
    except:
        sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )
        raise
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )
def createShelf():
	if mel.eval('layout -q -ex dumpstertree;') == 0:
		thing = mel.eval('addNewShelfTab "dumpstertree";')
	
	print cmds.layout( shelfName, q=True, ca=True)
	
	if mel.eval('shelfButton -q -ex vertSnappy;') == 0:
		cmds.shelfButton(buttonName, l="vert snappy", annotation='snap verts', image1='vertSnappyIcon_Low.png', command='cmds.vertSnappy()', p=shelfName)
def killShelf():
	cmds.deleteUI(shelfName)

cmds.scriptJob(e= ["quitApplication",lambda : killShelf() ] )
