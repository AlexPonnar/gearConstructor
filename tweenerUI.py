from maya import cmds


def tween(percentage, obj=None, attrs= None, selection=True):

    # if obj is not given and selection is set to False, error early
    if not obj and not selection:
        raise ValueError("No object given to tween")

    # if no obj is specified, get it from the first selection
    if not obj:
        obj = cmds.ls(selection=True)[0]

    if not attrs:
        attrs = cmds.listAttr(obj, keyable=True)

    current_time = cmds.currentTime(query=True)

    for attr in attrs:

        # Construct the full name of the attribute with its object
        attrFull = "%s.%s" % (obj, attr)

        # Get the keyframes of the attribute on this object
        keyframes = cmds.keyframe(attrFull, query=True)

        # If there are no keyframes then continue
        if not keyframes:
            continue

        previous_key_frames=[]
        for frame in keyframes:
            if frame < current_time:
                previous_key_frames.append(frame)

        later_key_frames = [frame for frame in keyframes if frame > current_time]

        if not previous_key_frames and not later_key_frames:
            continue

        if previous_key_frames:
            previous_frame = max(previous_key_frames)

        else:
            previous_frame = None

        next_frame = min(later_key_frames) if later_key_frames else None

        if not previous_key_frames or next_frame:
            continue

        previous_value = cmds.getAttr(attrFull, time=previous_frame)
        next_value = cmds.getAttr(attrFull, time= next_frame)

        difference = next_value - previous_value
        weighted_difference = (difference * percentage) / 100.0
        curreent_value = previous_value + weighted_difference

        cmds.setKeyframe(attrFull, time=current_time, value=curreent_value)


class TweenerWindow(object):

    window_name = "TweenerWindow"

    def show(self):

        if cmds.window(self.window_name, query=True, exists=True):
            cmds.deleteUI(self.window_name)

        cmds.window(self.window_name)

        self.buildUI()

        cmds.showWindow()

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

    def close(self, *args):
        cmds.deleteUI(self.window_name)


