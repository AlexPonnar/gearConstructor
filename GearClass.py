from maya import cmds


class Gear(object):
    """
    This is a Gear object that lets us create and modify a gear
    """
    def __init__(self):

        # The __init__ method lets us set default values
        self.transform = None
        self.extrude = None
        self.constructor = None

    def create_gear(self, teeth=10, length=.3):
        """
        This function will create gears with the parameters
        Args:
            teeth: The number of teeth to create
            length: The length of the teeth

        Returns: A tuple of the transform, constructor and extrude

        """

        # Teeth are in every alternate faces, so spans = teeth X 2
        spans = teeth * 2

        self.transform, self.constructor = cmds.polyPipe(subdivisionsAxis=spans)

        side_faces = range(spans*2, spans*3, 2)

        cmds.select(clear=True)

        for face in side_faces:
            cmds.select("%s.f[%s]" % (self.transform, face), add=True)

        self.extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]

    def change_teeth(self, teeth=10, length=0.3):
        spans = teeth * 2

        cmds.polyPipe(self.constructor, edit=True, subdivisionsAxis=spans)

        side_faces = range(spans * 2, spans * 3, 2)
        faces_names = []

        for face in side_faces:
            faces_name = 'f[%s]' % (face)
            faces_names.append(faces_name)

        cmds.setAttr('%s.inputComponents' % (self.extrude), len(faces_names),
                     *faces_names, type='componentList')

        cmds.polyExtrudeFacet(self.extrude, edit=True, localTranslateZ=length)

