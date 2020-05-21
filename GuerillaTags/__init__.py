
import os
import re
import maya.cmds as cmds

IMAGE_PATH = os.path.dirname(__file__) + "/Icon/"
TAG_PATTERN = re.compile(r"\w+")


def _iter_geo_with_tags():
    for geo in cmds.ls(geometry=True):
        if cmds.attributeQuery(
                'GuerillaTags',
                node=geo,
                exists=True):
            yield geo


def _get_tags(obj):
    try:
        raw_tags = cmds.getAttr('{}.GuerillaTags'.format(obj))
    except ValueError:  # Raised when attribute does not exist
        raw_tags = ""
    return set(TAG_PATTERN.findall(raw_tags))


def _set_tags(obj, tags):
    if not cmds.attributeQuery("GuerillaTags", node=obj, exists=True):
        cmds.addAttr(obj, longName="GuerillaTags", dataType="string")
    cmds.setAttr('{}.GuerillaTags'.format(obj),
                 ', '.join(set(tags)),
                 type='string')


def _shapes_under_selection():
    selected = cmds.ls(
        selection=True, type="shape") or []
    relatives = cmds.listRelatives(
        allDescendents=True, type="shape", path=True) or []
    return selected + relatives


class GuerillaTagsWindow(object):
    """
    Class containing both logic and UI for the guerilla tags tool.
    """

    def __init__(self):
        print("zab")
        if (cmds.window("GuerillaTagsWindow", exists=True)):
                cmds.deleteUI("GuerillaTagsWindow")

        window = cmds.window(
            "GuerillaTagsWindow",
            title="Guerilla Tags",
            iconName='Guerilla Tags',
            w=50, h=150, sizeable=False)

        cmds.rowColumnLayout(adjustableColumn=True)
        cmds.iconTextButton(
            style="iconAndTextHorizontal",
            image=IMAGE_PATH + "icon-GuerillaTags_02.png",
            h=80, al="center", backgroundColor=[0.15, 0.15, 0.15])
        cmds.text(label='', h=5)

        cmds.columnLayout('GuerillaTagsLayout', adjustableColumn=True, h=200)

    #-------------------------------------------- CHANGE, REMOVE OR ADD PREFIXE -------------------------------------------------

        cmds.textFieldGrp('guerilla_tags', pht='Tags...', adj=1, h=30)
        cmds.text(label='', h=5)
        cmds.button(label='Insert Tag(s) to selection', command=self.insert_tags)
        cmds.button(label='Replace Tag(s) on selection', command=self.replace_tags)
        cmds.button(label='Remove Tag(s) from Selection', command=self.remove_tags)
        cmds.button(label='Select matching Tag(s)', command=self.select_tags)

        cmds.text(label='', h=5)
        cmds.button(label='Clear Tags on selection', command=self.clear_tags)
        cmds.button(label='Select Objects not Tags', command=self.select_no_tags)
        cmds.setParent('..')

        print("zob")
        cmds.showWindow(window)

    def get_user_tags(self):
        raw = cmds.textFieldGrp('guerilla_tags', tx=1, q=1)
        return set(TAG_PATTERN.findall(raw))

    def insert_tags(self, *args):
        new_tags = self.get_user_tags()
        for shape in _shapes_under_selection():
            old_tags = _get_tags(shape)
            _set_tags(shape, new_tags | old_tags)

    def replace_tags(self, *args):
        new_tags = self.get_user_tags()
        for shape in _shapes_under_selection():
            _set_tags(shape, new_tags)

    def remove_tags(self, *args):
        new_tags = self.get_user_tags()
        for shape in _shapes_under_selection():
            old_tags = _get_tags(shape)
            _set_tags(shape, old_tags - new_tags)

    def select_tags(self, *args):
        user_tags = self.get_user_tags()
        cmds.select(clear=True)
        for shape in _iter_geo_with_tags():
            # Test if user tags are included in existing tags on shape
            if user_tags <= _get_tags(shape):
                cmds.select(shape, add=True)

    def clear_tags(self, *args):
        for shape in _shapes_under_selection():
            _set_tags(shape, [])

    def select_no_tags(self, *args):
        cmds.select(clear=True)
        for obj in _iter_geo_with_tags():
            if not _get_tags(obj):
                cmds.select(obj, add=True)

if __name__ == "__main__":
    GuerillaTagsWindow()
