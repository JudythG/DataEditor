import io

# call functions are function objects called when user selects a prompt
# the object functions (i.e. add) are functions that must be implemented
#   by the DataEditor class or its children
#
# So, if a user enters add at the prompt, the call_add function will be called.
# Call add calls o.add() which calls add(self) for a DataEditor object
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

# base class of prompters for the DataEditor classes
# two types of prompters:
#    non-leaf
#    leaf
# Leaf prompters provide prompts for obects with no chidren (strings, numbers)
# Non-leaf promptes provide prompts for objects that can have children (dict, list, tuple)
# Functions:
#  show     | display nodes at or below current level    | applies to both leaf and non_leaf objects
#  add      | add an element to an obect                 | applies to non-leaf objects only
#  del      | delete an element from an object           | applies to non-leaf objects only
#             Note: del may only be applied when an object has more than one child
#  path     | display current path                       | applies to both leaf and non_leaf objects
#  up       | move up in the list                        | applies to any object except the root
#  down     | down down the list                         | applies to non-leaf objects only
#  edit     | edit current object                        | applies to leaf objects only
#             Note: edit currently not available
#  q        | quit the application                       | may only quit from the root
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
	}

    # prompts are taken from list of allPrompts and added to either a Leaf or Non-Leaf Prompter
    def addPrompt (self, prompts, key):
        if key in self.allPrompts:
            v = self.allPrompts[key]
            prompts[key] = v

    # display list of available prompts for an object
    def prompt (self, pMap):
        print ("\nEnter a command")
        for k, v in pMap.items():
            prompt = v['prompt']
            print ("\t" + prompt)

    # defined in child classes
    # creates the prompt structures
    def createPrompts (self):
        pass

    # defined in child classes
    # displays prompts for user selection
    def getPrompts ():
        pass

# Prompter for dict, list, tuple
class NonLeafPrompter (Prompter):
    def __init__(self):
        self.createPrompts ()

    rootPrompts = {}        # prompts if at the root
    midLevelPrompts = {}    # any other non-leaf prompts

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
            # cannot delete if only one child
            if numberChildren == 1:
       	        if 'del' in self.rootPrompts:
                    del self.rootPrompts ['del']
            else:
                self.addPrompt (self.rootPrompts, 'del')
            return self.rootPrompts
        else:
            # cannot delete if only one child
            if numberChildren == 1:
                if 'del' in self.midLevelPrompts:
                    del self.midLevelPrompts ['del']
                else:
                    self.addPrompt (self.midLevelPrompts, 'del')
            return self.midLevelPrompts

# prompter for strings, number, etc
class LeafPrompter (Prompter):
    def __init__(self):
        self.createPrompts ()

    leafPrompts = {}

    # NB: removing edit - having trouble with that functionality
    def createPrompts (self):
        self.addPrompt (self.leafPrompts, 'show')
        self.addPrompt (self.leafPrompts, 'path')
        #self.addPrompt (self.leafPrompts, 'edit')
        self.addPrompt (self.leafPrompts, 'up')

    def getPrompts (self, isRoot, numberOfChildren):
        return self.leafPrompts
