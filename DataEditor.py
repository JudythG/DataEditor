# Future updates
#   * edit a leaf object (string)
#   * add non-leaf objects
#   * add tuple class

import io
import Prompter

# base class for Python types that can be edited and moved through
# curretly childre are DEDict, DEList, and DEString
class DataEditor():
    type = ''           # display type 
    path = []           # current path
    isRoot = False      # set to True only for the root object

    def print (self, descriptor):
        print (descriptor, self.type)

    def showpath (self):
        if len(self.path):
            print ("Path: " + str(self.path))
            print ()
        else:
            print ("Path: At the root")

    # called when application moves into into a DE object
    # the cursor is at this object
    #   path reflects the path to this object
    #   any functions - add, edit, up, quit - are applied off of this object
    # prompts user for an action and applies that action
    def doWork (d, p, key):
        d.parent = p
        d.curKey = key
        d.showpath()

        while True:
            promptMap = d.prompter.getPrompts(d.isRoot, len(d))
            d.prompter.prompt (promptMap)

            #response = input()
            response = input()
            if response in promptMap:

  	        # move up tree by returning from this function
                if response == 'up' or response == 'q':
                    if len (d.path):
                        d.path.pop()
                    if response == 'up':
                        print ("Path: " + str (d.path))
                    break 

                t1 = promptMap[response]
                t1['method'](d)
            else: 
                 print ("Invalid response" + response)

# DataEditor for a string
class DEString (str, DataEditor):
    prompter = Prompter.LeafPrompter()

    def __init__(self, s=''):
        str.__init__(s)
        self.type = 'string'

    # level -> how far to indent output
    # indents, prints type (string) and value
    def traverse (self, level):
        level += 1
        print (level * "\t", self.type, ": ", self)
        level -= 1

# DataEdditor for a list
class DEList (list, DataEditor):
    prompter = Prompter.NonLeafPrompter()

    def __init__(self, l=[]):
        super().__init__(l)
        self.type = 'list'

    # deepCopy copies data struct into DataEditor classes
    # that is, a list becomes a DEList, a dict a DEDict and so on
    def deepCopy (self, obj):
        for l in obj:
            if type(l) == str:
                self.append (DEString(l))
            elif type(l) == list:
                deList = DEList()
                deList.deepCopy (l)
                self.append (deList)
            elif type(l) == dict:
                deDict = DEDict()
                deDict.deepCopy (l)
                self.append(deDict)

    # DEList traverse
    # traverse displays the data structure to the terminal
    def traverse (self, level):
        level += 1
        print (level * "\t", "List")
        for l in self:
            l.traverse(level)
        level -= 1

    # DEList descend
    def descend (self):
	# if one item in list, descend into it
        if len(self) == 1:
            for k in self:
                self.path.append (k)
                self[0].doWork (self, k)

	# if multiple items in list, allow user to pick one
        else:
            choices = ''
            count = 0
            for value in self:
                choices = choices + str(count) + ': ' + value + '\n'
                count += 1
            print ("select index of item to move down into:\n" + choices)
            response = input ()
            idx = int(response)
            if idx < len(self):
                self.path.append (self[idx])
                self[idx].doWork (self, idx)

# DataEditor class for a dict               
class DEDict (dict, DataEditor):
    prompter = Prompter.NonLeafPrompter()

    def __init__(self, d={}):
        super().__init__(d)
        self.type = 'dict'

    # DEDict deepCopy
    # deepCopy copies data struct into DataEditor classes
    # that is, a list becomes a DEList, a dict a DEDict and so on
    def deepCopy (self, obj):
        for k, v in obj.items():
            if type(v) == str:
                self[k] = DEString (v)
            elif type(v) == dict:
                self[k] = DEDict()
                self[k].deepCopy (v)
            elif type(v) == list:
                self[k] = DEList()
                self[k].deepCopy (v)

    # DEDict traverse
    # traverse displays the data structure to the terminal
    def traverse (self, level):
        level += 1
        print (level * "\t", "Dict")
        for k, v in self.items():
            print (level * "\t", "Key: " , k)
            v.traverse (level)
        level -= 1

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
            print ("select key of item to move down into: " + keys)
            response = input () # JTG: need function to select key response
            if response in self.keys ():
                self.path.append (response)
                self[response].doWork (self, k)
                
    # DEDict:add ()
    def add(self):
        print (self.path)
        print ("Enter a key and value pair to add to the current dictionary")
        key = input ("Type a key: ")
        while (key in self.keys()):
            print ("Cannot overwrite an existing key")
            key = input ("Type in a new key value: ")
        value = input ("Enter a value: ")
        self[key] = DEString(value)
	# if no error, print added ....

    # DEDict delete 
    def delete (self):
        if len (self) == 1:
            print ("Can't delete from a one item list.")
            print ("SHOULD NOT EVEN BE ON OPTION LIST")
            return

        key_str = ''
        for k in self.keys ():
            key_str = key_str + " " + k
        print ("Enter key to delete or q to quit")
        print ("Current keys are: " +  key_str)
        key = input()
        if key == 'q':
            return
        if key in self.keys():
	    #print ("Deleting " + key + ": " + self[key] + "\n")
            del self[key]

# main
d = {'hobbies': ['spinning poi', 'reading'], 'best_friend': 'Anne', 'travel': {'date': 'Spring 2003', 'location':'London'}}
print (d)
print ()

d1 = DEDict()
d1.deepCopy (d)
d1.isRoot = True
d1 = d1.doWork('', '')

