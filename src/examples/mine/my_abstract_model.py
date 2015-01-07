#! /usr/bin/env python


'''
PySide example MVC code

starting from:
see: 'http://pythoncentral.org/pyside-pyqt-tutorial-qlistview-and-qstandarditemmodel
'''


import sys, os, pprint, time
from PySide import QtCore
from PySide import QtGui
import config
import moxygroup


class MyMainWindow(QtGui.QMainWindow):
	
	def __init__(self, *args, **kwargs):
		QtGui.QMainWindow.__init__(self, *args, **kwargs)
		self.treeview = QtGui.QTreeView()

		self.setWindowTitle('My Abstract Model')
		self.setMinimumSize(600, 400)
		self.setCentralWidget(self.treeview)

		# Create an empty model for the list's data
		self.model = MyAbstractModel(self.treeview)
		self.treeview.setModel(self.model)
		self.treeview.model().headers = ['the first column']
		
		self.statusBar().showMessage('Ready')
	
	def createData(self):
		groups = config.read_config(config.XML_CONFIG_FILE)[1]


class TreeItem(object):
	def __init__(self, data, parent=None):
		self.parentItem = parent
		self.itemData = data
		self.childItems = []

	def appendChild(self, item):
		self.childItems.append(item)
	
	def child(self, row):
		return self.childItems[row]
	
	def childCount(self):
		return len(self.childItems)
	
	def columnCount(self):
		return len(self.itemData)
	
	def data(self, column):
		try:
			return self.itemData[column]
		except IndexError:
			return None
	
	def parent(self):
		return self.parentItem
	
	def row(self):
		if self.parentItem:
			return self.parentItem.childItems.index(self)
		
		return 0


class MyAbstractModel(QtCore.QAbstractItemModel):
	# http://pyside.github.io/docs/pyside/PySide/QtCore/QAbstractItemModel.html
	
	def __init__(self, *args, **kwargs):
		QtCore.QAbstractItemModel.__init__(self, *args, **kwargs)

		self.rootItem = TreeItem( ('Group',) )

		groups = config.read_config(config.XML_CONFIG_FILE)[1]
		lines = []
		for group in groups:
			lines += [group.name]
			for table in group.tablelist:
				lines += [' '*4 + table.name]
				for row in table.rowlist:
					lines += [' '*8 + row.name]
		self.setupModelData(lines, self.rootItem)

	def columnCount(self, parent):
		if parent.isValid():
			return parent.internalPointer().columnCount()
		else:
			return self.rootItem.columnCount()

	def data(self, index, role):
		if not index.isValid():
			return None
		
		if role != QtCore.Qt.DisplayRole:
			return None
		
		item = index.internalPointer()
		
		return item.data(index.column())
	
	def flags(self, index):
		if not index.isValid():
			return QtCore.Qt.NoItemFlags
		
		return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
	
	def headerData(self, section, orientation, role):
		if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
			return self.rootItem.data(section)
		
		return None
	
	def index(self, row, column, parent):
		if not self.hasIndex(row, column, parent):
			return QtCore.QModelIndex()
	
		if not parent.isValid():
			parentItem = self.rootItem
		else:
			parentItem = parent.internalPointer()
	
		childItem = parentItem.child(row)
		if childItem:
			return self.createIndex(row, column, childItem)
		else:
			return QtCore.QModelIndex()
	
	def parent(self, index):
		if not index.isValid():
			return QtCore.QModelIndex()
	
		childItem = index.internalPointer()
		parentItem = childItem.parent()
	
		if parentItem == self.rootItem:
			return QtCore.QModelIndex()
	
		return self.createIndex(parentItem.row(), 0, parentItem)
	
	def rowCount(self, parent):
		if parent.column() > 0:
			return 0
	
		if not parent.isValid():
			parentItem = self.rootItem
		else:
			parentItem = parent.internalPointer()
	
		return parentItem.childCount()

	def setupModelData(self, lines, parent):
		parents = [parent]
		indentations = [0]
		
		for whole_line in lines:
			position = len(whole_line) - len(whole_line.lstrip())
			lineData = whole_line.strip()
			
			if lineData:
				# Read the column data from the rest of the line.
				columnData = [s for s in lineData.split('\t') if s]
				
				if position > indentations[-1]:
					# The last child of the current parent is now the new
					# parent unless the current parent has no children.
					
					if parents[-1].childCount() > 0:
						parents.append(parents[-1].child(parents[-1].childCount() - 1))
						indentations.append(position)
				
				else:
					while position < indentations[-1] and len(parents) > 0:
						parents.pop()
						indentations.pop()
				
				# Append a new item to the current parent's list of children.
				parents[-1].appendChild(TreeItem(columnData, parents[-1]))


def main():
	app = QtGui.QApplication(sys.argv)
	main_window = MyMainWindow()
	main_window.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
