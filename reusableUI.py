from tweenerUI import tween
from GearClass import Gear
from maya import cmds


class BaseWindow(object):

    window_name = "BaseWindow"

    def show(self):

        if cmds.window(self.window_name, query=True, exists=True):
            cmds.deleteUI(self.window_name)

        cmds.window(self.window_name)

        self.buildUI()

        cmds.showWindow()

    def buildUI(self):
        pass

    def reset(self):
        pass

    def close(self, *args):
        cmds.deleteUI(self.window_name)


class TweenerUI(BaseWindow):

    window_name = "TweenerWindow"

    def buildUI(self):

        column = cmds.columnLayout()

        cmds.text(label="Use this slider to set the tween amount")

        row = cmds.rowLayout(numberOfColumns=2)

        self.slider = cmds.floatSlider(min=0, max=100, value=50, step=1,
                                       changeCommand=tween)

        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    def reset(self, *args):
        print "Resetting UI"

        cmds.floatSlider(self.slider, edit=True, value=50)


class GearUI(BaseWindow):

    window_name = "GearWindow"

    def __init__(self):
        self.gear = None

    def buildUI(self):

        column = cmds.columnLayout()
        cmds.text(label="Use slider to modify the gear")

        cmds.rowLayout(numberOfColumns=4)
        self.label = cmds.text(label="10")

        self.slider = cmds.intSlider(min=5, max=30, value=10, step= 1,
                                     dragCommand=self.modifyGear)
        cmds.button(label="Make Gear", command=self.makeGear)
        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    def makeGear(self, *args):
        teeth = cmds.intSlider(self.slider, query=True, value=True)

        self.gear = Gear()
        self.gear.create_gear(teeth=teeth)

    def modifyGear(self, teeth):
        if self.gear:
            self.gear.change_teeth(teeth=teeth)

        cmds.text(self.label, edit=True, label=teeth)

    def reset(self, *args):
        self.gear = None
        cmds.intSlider(self.slider, edit=True, value=10)
        cmds.text(self.label, edit=True, label=10)




