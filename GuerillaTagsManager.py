import os, os.path
import shutil
import maya.cmds as cmds
import datetime
import sys

#-------------------------------------------- CHANGE PATH WITH OUR IMAGE -------------------------------------------------

Imagepath = "P:/Groupe_02_ENNUI/03_SCRIPT/Pipeline/GuerillaTags/Icon/" 


#-------------------------------------------- TAG MANAGER -------------------------------------------------

def SetTags():
	prefix = cmds.optionMenu('prefix_tags', v=1,q=1 )
	if prefix == 'Prefix - None':
		prefix = ''
	else:
		prefix = prefix + '_'
	tags = cmds.textFieldGrp('guerilla_tags',tx=1,q=1)
	if tags != '':
		tags = prefix + cmds.textFieldGrp('guerilla_tags',tx=1,q=1)
		shapenodes = []
		selection = cmds.ls(sl=True) # Get Selection

		tags_list = tags.replace(' ', '').split(',')

		for obj in selection:

		    # Check if selected object is a shapeNode
		    is_shape = cmds.objectType(obj, isType='mesh')

		    if not is_shape:
		        shapes = cmds.listRelatives(obj, shapes=True)
		        for itm in shapes:
		            shapenodes.append(itm)
		    else:
		        shapenodes.append(obj)

		for shape in shapenodes:
		    # Check if GuerillaTags attribute exists on selected
		    has_guerilla_tags = cmds.attributeQuery('GuerillaTags', node=shape, exists=True)
		    # If attr GuerillaTags doesnt exists, create it
		    if not has_guerilla_tags:
		        cmds.select(shape)
		        cmds.addAttr( shortName='GuerillaTags', longName='GuerillaTags', dataType='string')
		        cmds.setAttr( '{}.GuerillaTags'.format(shape),', '.join(tags_list), type='string')
		    else:
				print('attribute already exists')
				existing_tags = cmds.getAttr('{}.GuerillaTags'.format(shape))
				existing_tags_list = existing_tags.replace(' ', '').split(',')
				final_tag_list = existing_tags_list
				for tag in tags_list:
					if not tag in existing_tags_list:
						final_tag_list.append(tag)
				cmds.setAttr( '{}.GuerillaTags'.format(shape),', '.join(final_tag_list), type='string')

def DeleteTags():
	selection = cmds.ls(sl=True) # Get Selections
	shapenodes = []
	for obj in selection:

		# Check if selected object is a shapeNode
		is_shape = cmds.objectType(obj, isType='mesh')

		if not is_shape:
			shapes = cmds.listRelatives(obj, shapes=True)
			for itm in shapes:
				shapenodes.append(itm)
		else:
			shapenodes.append(obj)

	for shape in shapenodes:
		# Check if GuerillaTags attribute exists on selected
		has_guerilla_tags = cmds.attributeQuery('GuerillaTags', node=shape, exists=True)
		# If attr GuerillaTags doesnt exists, create it
		if not has_guerilla_tags:
			print('attribute already exists')
		else:
			# Delete an attributes.
			cmds.deleteAttr('{}.GuerillaTags'.format(shape))

def selectObjectsNoTags():

	objects = cmds.ls(geometry=True)
	not_tagged = []

	for obj in objects:
	    is_tagged = False

	    has_guerilla_tags = cmds.attributeQuery('GuerillaTags',
	                                             node=obj,
	                                             exists=True)

	    if has_guerilla_tags:
	        existing_tags = cmds.getAttr('{}.GuerillaTags'.format(obj))
	        existing_tags = existing_tags.replace(' ', '')

	        if existing_tags != '':
	            is_tagged = True

	    if not is_tagged:
	        not_tagged.append(obj)
	        cmds.select(not_tagged)

def makeWindow():
	if (cmds.window("Pipeline", exists=True)):
			cmds.deleteUI("Pipeline")
	#def Pipeline():
	window = cmds.window("Guerilla Tags", title="Guerilla Tags", iconName='Guerilla Tags', w=50,h=150,sizeable=False)

	colonneP=cmds.rowColumnLayout(adjustableColumn=True)
	cmds.iconTextButton( style="iconAndTextHorizontal", image=Imagepath+"icon-GuerillaTags_02.png",h=80,al="center", backgroundColor=[0.15, 0.15, 0.15])
	cmds.text( label='',h=5 )

	#---------- TAG MANAGER ----------
	cmds.columnLayout('GuerillaTagsLayout', adjustableColumn=True,h=200)
	cmds.optionMenu('prefix_tags',h=30)
	cmds.menuItem( label='Prefix - None' )

#-------------------------------------------- CHANGE, REMOVE OR ADD PREFIXE -------------------------------------------------

	cmds.menuItem( label='Student' )
	cmds.menuItem( label='Granny' )
	cmds.menuItem( label='Schoolgirl' )
	cmds.menuItem( label='WorkingWoman' )
	cmds.menuItem( label='Cashier' )
	cmds.menuItem( label='Kitchen' )
	cmds.menuItem( label='Bridge' )
	cmds.menuItem( label='Supermarket' )
	cmds.menuItem( label='Elevator' )
	cmds.menuItem( label='Classroom' )


	cmds.textFieldGrp('guerilla_tags',pht='Tags...',adj=1,h=30)
	cmds.text( label='',h=5)
	cmds.button( label='Add Tags Selection', command="SetTags()")
	cmds.button( label='Delete Tags Selection', command="DeleteTags()" )
	cmds.button( label='Select Objects not Tags', command="selectObjectsNoTags()" )
	cmds.setParent('..')
	

	cmds.showWindow( window )

makeWindow()

#END
