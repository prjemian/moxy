#! /usr/bin/env python


'''
Basic model for the Moxy program
'''


group_counter = 0


class MoxyGroup(object):
   
    def __init__(self, name=''):
        global group_counter
        group_counter += 1
        if len(name) > 0:
            self.name = name
        else:
            self.name = 'group ' + str(group_counter)
        self.axislist = []
        self.tablelist = []
        self.selected_table = None
    
    def __str__(self):
        return self.name
    
    def axisNameToIndex(self, name):
        '''return the index of the first instance of named axis or None if not found'''
        for index, axis in enumerate(self.axislist):
            if axis.name == name:
                return index
        return None
    
    def tableNameToIndex(self, name):
        '''return the index of the first instance of named table or None if not found'''
        for index, table in enumerate(self.tablelist):
            if table.name == name:
                return index
        return None


class GroupAxis(object):
    
    def __init__(self, name=''):
        self.name = name
        self.isMotorRec = True
        self.field_config = dict(VAL='', RBV='', EGU='', DESC='', STOP='', DMOV='')
        self.pvdict = dict(VAL=None, RBV=None, EGU=None, DESC=None, STOP=None, DMOV=None)


class GroupTable(object):
    
    def __init__(self, name=''):
        self.name = name
        self.rowlist = []
        self.selected_row = None
    
    def nameToIndex(self, name):
        '''return the index of the first instance of named row or None if not found'''
        for index, row in enumerate(self.rowlist):
            if row.name == name:
                return index
        return None


class TableRow(object):
    
    def __init__(self, name=''):
        self.name = name
        self.positionlist = []
    
    def nameToIndex(self, name):
        '''return the index of the first instance of named position or None if not found'''
        for index, pos in enumerate(self.positionList):
            if pos.name == name:
                return index
        return None

    def setPosition(self, name, value, create = False):
        '''redefine a named position, create if it does not exist according to optional flag'''
        index = self.nameToIndex(name)
        if index is not None:
            self.positionlist[index].setValue( value )
        elif create:
            self.positionlist.append( RowPosition(name, value) )


class RowPosition(object):
    
    def __init__(self, name='', text_value='', group_axis_obj=None):
        self.name = name
        self.setValue(text_value)
        self.group_axis_obj = group_axis_obj
    
    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
    
    def setValue(self, text_value):
        self.text_value = str(text_value)
        try:
            self.value = float(text_value)
        except:
            self.value = None
    
    def getValue(self):
        return self.value
    
    def getText(self):
        return self.text_value


class PositionInconsistency(Exception): pass
