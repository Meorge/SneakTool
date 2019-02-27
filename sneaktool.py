import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
Qt = QtCore.Qt

class Window(QtWidgets.QMainWindow):
	"""Main Window"""
	
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)

		self.gridView = GridView()

		self.gridScene = GridScene()

		self.gridView.setScene(self.gridScene)

		self.gridView.setFrameRect(self.rect())
		self.gridView.setAlignment(Qt.AlignTop | Qt.AlignLeft)

		#self.gridScene.set
		

		self.setCentralWidget(self.gridView)

		self.resize(500,500)
	
##########################################
##########################################
##########################################

class GridView(QtWidgets.QGraphicsView):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setRenderHints(self.renderHints() | QtGui.QPainter.Antialiasing  | QtGui.QPainter.SmoothPixmapTransform)

		#self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
		#self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
		# self.viewport().setCursor(Qt.CrossCursor)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		#self.setBaseSize(10000, 10000)

	def mousePressEvent(self, event):
		event.ignore()
		super(GridView, self).mousePressEvent(event)

	def mouseMoveEvent(self, event):
		event.ignore()
		print("move the view")
		super(GridView, self).mouseMoveEvent(event)



##########################################
##########################################
##########################################

class GridScene(QtWidgets.QGraphicsScene):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setSceneRect(0, 0, 1000, 1000)

	def addNode(self, node):
		self.addItem(node)

		node.EstablishInputsOutputs()

	def mousePressEvent(self, event):
		event.ignore()
		super(GridScene, self).mousePressEvent(event)

	def mouseMoveEvent(self, event):
		event.ignore()
		#print("move the scene")
		super(GridScene, self).mouseMoveEvent(event)

	def drawBackground(self, painter, rect):
		
		painter.setBrush(QtGui.QBrush(QtGui.QColor(50,50,50)))
		painter.drawRect(rect)

		self.gridPen = QtGui.QPen(QtGui.QColor(85,85,85), 1, Qt.DotLine)
		painter.setPen(self.gridPen)


		# stuff past this point in this func is written by RoadrunnerWMC,
		# who is really cool.

		CELL_SIZE = 25

		# Get the coordinates of the rect
		x1 = rect.left()
		y1 = rect.top()
		x2 = rect.right()
		y2 = rect.bottom()

		# Now we need to adjust those coordinates to be multiples of
		# CELL_SIZE. We want to do this by *expanding* the rect -- that is,
		# we move x1 further to the left, x2 further to the right, etc.
		x1 -= x1 % CELL_SIZE # rounds down to nearest multiple of CELL_SIZE
		y1 -= y1 % CELL_SIZE
		x2 += (CELL_SIZE - x2) % CELL_SIZE # rounds up to nearest multiple of CELL_SIZE
		y2 += (CELL_SIZE - y2) % CELL_SIZE

		# Now we draw the grid lines within that slightly expanded rect
		for x in range(int(x1), int(x2 + 1), CELL_SIZE):
			painter.drawLine(x, y1, x, y2)
		for y in range(int(y1), int(y2 + 1), CELL_SIZE):
			painter.drawLine(x1, y, x2, y)

	# def drawBackground(self, painter, rect):

	# 	halfOfWidth = (rect.width() / 2)
	# 	halfOfHeight = (rect.height() / 2)
	# 	self.backgroundBrush = QtGui.QBrush(QtGui.QColor(50,50,50))
	# 	painter.setBrush(self.backgroundBrush)

	# 	painter.drawRect(rect)



	# 	self.gridPen = QtGui.QPen(QtGui.QColor(85,85,85), 1, Qt.DotLine)
	# 	# self.gridPen = QtGui.QPen(Qt.white, 3, Qt.SolidLine)
	# 	# painter.setPen(self.gridPen)

	# 	# painter.drawLine(0,0,1000,1000)


	# 	# draw the lines - for numbers from 1 to 500 (or maybe zero, IDK) check if divisible by 2; if so, multiply by 15 and draw it from
	# 	# (15x - halfOfWidth, -halfOfHeight) to (15x, height)
	# 	for x in range(1000):
	# 		if (x % 2 == 0):
	# 			painter.drawLine(x * 15 - halfOfWidth, 0 - halfOfHeight, x * 15 - halfOfWidth, 1000)

	# 	# (-halfOfWidth, 15y - halfOfHeight) to (width, 15y - halfOfHeight)
	# 	for y in range(1000):
	# 		if (y % 2 == 0):
	# 			painter.drawLine(0 - halfOfWidth, y * 15 - halfOfHeight, 1000, y * 15 - halfOfHeight)





		


if __name__ == '__main__':
	global app, window
	app = QtWidgets.QApplication(sys.argv)

	window = Window()
	window.show()
	sys.exit(app.exec_())

	
