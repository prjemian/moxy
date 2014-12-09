#! /usr/bin/env python


'''
PySide example MVC code

starting from:
see: 'http://pythoncentral.org/pyside-pyqt-tutorial-qlistview-and-qstandarditemmodel
'''


import sys, os, pprint, time
from PySide import QtCore
from PySide import QtGui


class MyView(QtGui.QListView):
	
	def __init__(self, *args, **kwargs):
		QtGui.QListView.__init__(self, *args, **kwargs)


class MyModel(QtGui.QStandardItemModel):
	
	def __init__(self, *args, **kwargs):
		QtGui.QStandardItemModel.__init__(self, *args, **kwargs)


class MyMainWindow(QtGui.QMainWindow):
	
	def __init__(self, *args, **kwargs):
		QtGui.QMainWindow.__init__(self, *args, **kwargs)
		self.listview = MyView()

		self.setWindowTitle('Honey-Do List')
		self.setMinimumSize(600, 400)
		self.setCentralWidget(self.listview)

		# Create an empty model for the list's data
		self.model = MyModel(self.listview)
		self.listview.setModel(self.model)
		
		# put some data into the model
		self.makeData()

		self.model.itemChanged.connect(self.on_item_changed)
		
		self.statusBar().showMessage('Ready')


	def makeData(self):
		''''Add some textual items'''
		foods = [
		    'Cookie dough', # Must be store-bought
		    'Hummus', # Must be homemade
		    'Spaghetti', # Must be saucy
		    'Dal makhani', # Must be spicy
		    'Chocolate whipped cream' # Must be plentiful
		]
		for food in foods:
			item = QtGui.QStandardItem(food)	# Create an item with a caption
			item.setCheckable(True)				# Add a checkbox to it
			self.model.appendRow(item)			# Add the item to the model

	def on_item_changed(self, item):
		'''check if all boxes are checked, then exit'''
		# If the changed item is not checked, don't bother checking others
		if not item.checkState():
			return
		
		self.statusBar().showMessage(item.text())
		# Loop through the items until you get None, which
		# means you've passed the end of the list
		i = 0
		while self.model.item(i):
			if not self.model.item(i).checkState():
				return
			i += 1
		self.bailout()

	def bailout(self):
		def delayMessage(seconds, method):
			QtCore.QTimer.singleShot(seconds*1000, method)
		delayMessage(3, self.close)
		delayMessage(2, self.one_second_left)
		delayMessage(1, self.two_seconds_left)
		self.statusBar().showMessage('exiting in 3 s ...')

	def two_seconds_left(self):
		self.statusBar().showMessage('exiting in 2 s ...')

	def one_second_left(self):
		self.statusBar().showMessage('exiting in 1 s ...')


def main():
	app = QtGui.QApplication(sys.argv)
	main_window = MyMainWindow()
	main_window.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
