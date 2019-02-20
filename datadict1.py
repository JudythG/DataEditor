# Level 1: strings are only element of dictionary

import io

# Store current in git and branch off
# Why string dispaly type not set? Look up constructor format

def call_traverse (o):
    o.traverse (0)

def call_add (o):
    o.add ()

def call_del (o):
    o.delete ()

def call_showpath (o):
    o.showpath ()

def call_ascend (o):
    o.ascend ()

def call_descend (o):
    o.descend()

def call_edit (o):
    o.edit()

def call_quit (o):
    pass

class Prompter():

    # key -> user entered string
    # value -> function to call
    allPrompts = {
	'show': {'prompt': 'Type show to display all nodes that are at and below this level', 'method': call_traverse }, 
	'add':  {'prompt': 'Type add to add an item', 					'method': call_add }, 
	'del':  {'prompt': 'Type del to delete a data element', 			'method': call_del },
	'path': {'prompt': 'Type path to show current location in data editor', 	'method': call_showpath }, 
	'up':   {'prompt': 'Type up to move up the tree', 				'method': call_ascend },
	'down': {'prompt': 'Type down to move down the tree', 				'method': call_descend }, 
	'edit': {'prompt': 'Type edit to edit this value', 				'method': call_edit },
	'q':	{'prompt': 'Type q to quit',						'method': call_quit }
	} # Null for methods that aren't called?

    def addPrompt (self, prompts, key):
	if key in self.allPrompts:
	    v = self.allPrompts[key]
	    prompts[key] = v

    def prompt (self, pMap):
        print "\nEnter a command"
        for k, v in pMap.items():
	    prompt = v['prompt']
	    print "\t" + prompt

    def createPrompts (self):
	pass

    def getPrompts ():
	pass

class NonLeafPrompter (Prompter):
    def __init__(self):
	self.createPrompts ()

    rootPrompts = {}
    midLevelPrompts = {}

    def createPrompts (self):
	self.addPrompt (self.rootPrompts, 'show')
	self.addPrompt (self.rootPrompts, 'path')
	self.addPrompt (self.rootPrompts, 'add')
	self.addPrompt (self.rootPrompts, 'del')
	self.addPrompt (self.rootPrompts, 'down')
	self.addPrompt (self.rootPrompts, 'q')

	self.addPrompt (self.midLevelPrompts, 'show')
	self.addPrompt (self.midLevelPrompts, 'path')
	self.addPrompt (self.midLevelPrompts, 'add')
	self.addPrompt (self.midLevelPrompts, 'del')
	self.addPrompt (self.midLevelPrompts, 'down')
	self.addPrompt (self.midLevelPrompts, 'up')

    def getPrompts (self, isRoot, numberChildren):
	if (isRoot):
		if numberChildren == 1:
			if 'del' in self.rootPrompts:
			    del self.rootPrompts ['del']
		else:
			self.addPrompt (self.rootPrompts, 'del')
		return self.rootPrompts
	else:
		if numberChildren == 1:
			if 'del' in self.midLevelPrompts:
			    del self.midLevelPrompts ['del']
		else:
			self.addPrompt (self.midLevelPrompts, 'del')
		return self.midLevelPrompts

class LeafPrompter (Prompter):
    def __init__(self):
	self.createPrompts ()

    leafPrompts = {}

    def createPrompts (self):
	self.addPrompt (self.leafPrompts, 'show')
	self.addPrompt (self.leafPrompts, 'path')
	self.addPrompt (self.leafPrompts, 'edit')
	self.addPrompt (self.leafPrompts, 'up')

    def getPrompts (self, isRoot, numberOfChildren):
	return self.leafPrompts

class DataEditor(object):
    isRoot = False
    path = []
    indent = '   '
    displayType = ''
    dataTypes = ('dict', 'str') # add list and tuple

    def traverse (self, level):
	pass

    def showpath (self):
	if len(self.path):
            print "Path: " + str(self.path)
	    print
	else:
	    print "Path: At the root"

    def doWork (d, p, key):
	d.parent = p
	d.curKey = key
	d.showpath()

	while True:
	    promptMap = d.prompter.getPrompts(d.isRoot, len(d))
	    d.prompter.prompt (promptMap)

	    response = raw_input()
	    if response in promptMap:

		# move up tree by returning from this function
		if response == 'up' or response == 'q':
			if len (d.path):
			    d.path.pop()
			if response == 'up':
			    print "Path: " + str (d.path)
			break

	        t1 = promptMap[response]
		t1['method'](d)
	    else: 
		print "Invalid response" + response

#DEString: Data Editor for a string
class DEString (str, DataEditor):
    prompter = LeafPrompter()

    def setDisplayType (self):
	self.displayType == "String"

    def traverse (self, level):
	level += 1
	print (level*self.indent) + self.displayType + ": " + self.parent[self.curKey]
	level -= 1

    # Can not add a child to a leaf node
    #def add (self):
	#return

    # Can not delete a chld from a leaf node
    #def delete (self):
	#return

    def edit (self):
	print "in edit"
	self.parent[self.curKey] = self.parent.editChild (self.parent, self.curKey)
	print self.parent

# DEList : Data Editor's list wrapper
class DEList (list, DataEditor):
    curKey = 0
    parent = ''
    prompter = NonLeafPrompter()

    # DataEditor:deepCopy () copies all elements of input dictionary to a DEDict
    # the new DEDict's elements are all DataEditor classes
    # that is, a str object will be a DEString object in the new DEDict, and so forth with the other data types
    def deepCopy (self, d):
        for v in d:
            if type(v) == str:
		self.append (DEString(v))
	    elif type (v) == dict:
		d = DEDict ( {} )
		d.deepCopy (v)
		self.append (d)
	    elif type(v) == list:
		l = DEList ( [] )
		l.deepCopy (v)
		self.append (l)
	return self

    def editChild (child, parent, key):
	s = raw_input ("Type new value: ")
	return s

    def setDisplayType (self):
	self.displayType = "List"

    # DEList : traverse_list ()
    def traverse_list (self, level):
	level += 1
        for l in self:
	    # why polymorphism not work? 
	    dictTemp = DEDict ( {} )
	    listTemp = DEList ( [] )

	    # DEDict
	    if type (dictTemp) == type (l):
		#print (level * self.indent) + "Key" + ": " 
		l.traverse (level)

	    # DEList
	    elif type (listTemp) == type (l):
		l.traverse_list (level)

	    # DEString
	    else:
		level += 1
	        print (level * self.indent) + "String" + ": " + l
		level -= 1

	level -= 1

# DEDict: Data Editor Dictionary
class DEDict (dict, DataEditor):
    curKey = ''
    parent = ''
    prompter = NonLeafPrompter()

    # DataEditor:deepCopy () copies all elements of input dictionary to a DEDict
    # the new DEDict's elements are all DataEditor classes
    # that is, a str object will be a DEString object in the new DEDict, and so forth with the other data types
    def deepCopy (self, d):
        for k, v in d.items ():
            if type(v) == str:
		self[k] = DEString(v)
		self[k].setDisplayType()
	    elif type (v) == dict:
		self[k] = DEDict ( {} )
		self[k].setDisplayType()
		self[k].deepCopy (v)
	    elif type(v) == list:
		self[k] = DEList ( [] )
		self[k].setDisplayType ()
		self[k].deepCopy (v)
	return self

    def editChild (child, parent, key):
	s = raw_input("Type new value: ")
	return s

    def setDisplayType(self):
        self.displayType = "Dict"

    # DEDict:traverse ()
    def traverse (self, level):
	level += 1
        for k in self.keys():

	    # JTG: polymorphism not working
	    # correct function shold be called for data types
	    #	but not
	    dictTemp = DEDict ( {} )
	    listTemp = DEList ( [] )

	    # call for DEDict
	    if type (self[k]) == type (dictTemp):
		print (level * self.indent) + "Dict Key" + ": " + k
		self[k].traverse (level)

	    # call for DEList
	    elif type ( self[k] ) == type (listTemp):
		print (level * self.indent) + "List Key" + ": " + k
		self[k].traverse_list (level)

	    # call for DEString
	    else:
		print (level * self.indent) + "String Key" + ": " + k
		level += 1
		print (level * self.indent) + "String: " + self[k]
		level -= 1

	level -= 1

    # DEDict:add ()
    def add(self):
	print self.path
	print "Enter a key and value pair to add to the current dictionary"
	key = raw_input ("Type a key: :")
	while (key in self.keys()):
	    print "Cannot overwrite an existing key"
	    key = raw_input ("Type in a new key value: ")
	value = raw_input ("Enter a value: ")
	self[key] = value
	# if no error, print added ....

    def delete (self):
	if len (self) == 1:
	    print "Can't delete from a one item list."
	    print "SHOULD NOT EVEN BE ON OPTION LIST"
	    return

	key_str = ''
	for k in self.keys ():
	    key_str = key_str + " " + k
        print "Enter key to delete or q to quit"
	print "Current keys are: " +  key_str
	key = raw_input()
	if key == 'q':
	    return
	if key in self.keys():
	    #print "Deleting " + key + ": " + self[key] + "\n"
	    del self[key]

    # DEDict descend
    def descend (self):
	# if one item in list, descend into it
	if len(self) == 1:
	    for k in self.keys():
		self.path.append (k)
		self[k].doWork (self, k)

	# if multiple items in list, allow user to pick one
	else:
	    keys = ''
	    for k in self.keys():
		keys = keys + k + " "
	    print "select key of item to move down into: " + keys
	    response = raw_input () # JTG: need function to select key response
	    if response in self.keys ():
		self.path.append (response)
		self[response].doWork (self, k)

    # DEDict: setRoot () - sets the boolean isRoot to true
    # call only for the root object
    def setRoot (self):
	self.isRoot = True

# main
d1 = {'k0': {'k1': {'k2': ['l1'], 'k3': 'v3'}, 'k4': 'v4'}, 'k5': 'v5' } 
deDict = DEDict ( {'k1': DEDict ( {'k2': DEList (['l1'] ), 'k3': DEString ('v3' )} ) } )
#deDict = DEDict ()
deDict.setDisplayType ()
#deDict.deepCopy (d1)
deDict.setRoot ()
deDict = deDict.doWork ('', '')
