from maya import cmds


def create_gear(teeth=10, length=0.3):
    """
    This function will create gears with the parameters
    Args:
        teeth: The number of teeth to create
        length: The length of the teeth

    Returns: A tuple of the transform, constructor and extrude node

    """
    # Teeth are every alternate face, so spans = teeth X 2
    spans = teeth * 2

    transform, constructor = cmds.polyPipe(subdivisionsAxis=spans)

    side_faces = range(spans*2, spans*3, 2)
    print side_faces

    cmds.select(clear=True)

    for face in side_faces:
        cmds.select("%s.f[%s]" % (transform, face), add=True)

    extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]
    return transform, constructor, extrude


def change_teeth(constructor, extrude, teeth=10, length=0.3):
    spans = teeth*2

    cmds.polyPipe(constructor, edit=True, subdivisionsAxis=spans)

    side_faces = range(spans*2, spans*3, 2)
    faces_names = []

    for face in side_faces:
        faces_name = 'f[%s]' % (face)
        faces_names.append(faces_name)

    cmds.setAttr('%s.inputComponents' % (extrude), len(faces_names),
                 *faces_names, type = 'componentList')

    cmds.polyExtrudeFacet(extrude, edit=True, localTranslateZ=length)


