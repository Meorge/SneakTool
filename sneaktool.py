import os
import struct
import sys
import traceback

from PyQt5 import QtCore, QtGui, QtWidgets
Qt = QtCore.Qt

icons_path = os.path.dirname(__file__) + "/icons/"

class Window(QtWidgets.QMainWindow):
	"""Main Window"""
	
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		self.setupUi()
		self.gridView = GridView()
		
		self.gridScene = GridScene()
		
		self.gridView.setScene(self.gridScene)
		
		self.gridView.setFrameRect(self.rect())
		self.gridView.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		
		#self.gridScene.set
		
		
		self.setCentralWidget(self.gridView)
		
		#self.resize(500,500)
		
		#############################
		## COMPUTER-GENERATED CODE ##
		#############################

	def setupUi(self):
		self.setObjectName("MainWindow")
		self.resize(1402, 802)
		self.centralwidget = QtWidgets.QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout.setObjectName("gridLayout")
		self.graphicsView = GridView(self.centralwidget)
		self.graphicsView.setObjectName("graphicsView")
		self.gridLayout.addWidget(self.graphicsView, 0, 0, 2, 1)
		self.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(self)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 1402, 36))
		self.menubar.setObjectName("menubar")
		self.menuFile = QtWidgets.QMenu(self.menubar)
		self.menuFile.setObjectName("menuFile")
		self.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(self)
		self.statusbar.setObjectName("statusbar")
		self.setStatusBar(self.statusbar)
		self.ToolsDockWidget = QtWidgets.QDockWidget(self)
		self.ToolsDockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetMovable)
		self.ToolsDockWidget.setObjectName("ToolsDockWidget")
		self.dockWidgetContents = QtWidgets.QWidget()
		self.dockWidgetContents.setObjectName("dockWidgetContents")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setObjectName("verticalLayout")
		self.selectMoveButtom = QtWidgets.QPushButton(self.dockWidgetContents)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(icons_path + "arrow_rl.cur"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.selectMoveButtom.setIcon(icon)
		self.selectMoveButtom.setIconSize(QtCore.QSize(48, 48))
		self.selectMoveButtom.setCheckable(True)
		self.selectMoveButtom.setChecked(True)
		self.selectMoveButtom.setObjectName("selectMoveButtom")
		self.verticalLayout.addWidget(self.selectMoveButtom)
		self.drawTilesButton = QtWidgets.QPushButton(self.dockWidgetContents)
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap(icons_path + "aero_pen_xl.cur"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.drawTilesButton.setIcon(icon1)
		self.drawTilesButton.setIconSize(QtCore.QSize(48, 48))
		self.drawTilesButton.setCheckable(True)
		self.drawTilesButton.setObjectName("drawTilesButton")
		self.verticalLayout.addWidget(self.drawTilesButton)
		self.ActorBox = QtWidgets.QGroupBox(self.dockWidgetContents)
		self.ActorBox.setObjectName("ActorBox")
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.ActorBox)
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.AddGuardButton = QtWidgets.QPushButton(self.ActorBox)
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap(icons_path + "764986.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.AddGuardButton.setIcon(icon2)
		self.AddGuardButton.setIconSize(QtCore.QSize(48, 48))
		self.AddGuardButton.setCheckable(True)
		self.AddGuardButton.setChecked(False)
		self.AddGuardButton.setObjectName("AddGuardButton")
		self.verticalLayout_2.addWidget(self.AddGuardButton)
		self.AddCameraButton = QtWidgets.QPushButton(self.ActorBox)
		icon3 = QtGui.QIcon()
		icon3.addPixmap(QtGui.QPixmap(icons_path + "584abe7e2912007028bd9330.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.AddCameraButton.setIcon(icon3)
		self.AddCameraButton.setIconSize(QtCore.QSize(48, 48))
		self.AddCameraButton.setCheckable(True)
		self.AddCameraButton.setChecked(False)
		self.AddCameraButton.setObjectName("AddCameraButton")
		self.verticalLayout_2.addWidget(self.AddCameraButton)
		self.AddGemstoneButton = QtWidgets.QPushButton(self.ActorBox)
		icon4 = QtGui.QIcon()
		icon4.addPixmap(QtGui.QPixmap(icons_path + "45130c6d03b2256e6615f2a696195f41-diamond-gem-flat-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.AddGemstoneButton.setIcon(icon4)
		self.AddGemstoneButton.setIconSize(QtCore.QSize(48, 48))
		self.AddGemstoneButton.setCheckable(True)
		self.AddGemstoneButton.setChecked(False)
		self.AddGemstoneButton.setObjectName("AddGemstoneButton")
		self.verticalLayout_2.addWidget(self.AddGemstoneButton)
		self.AddDoorButton = QtWidgets.QPushButton(self.ActorBox)
		icon5 = QtGui.QIcon()
		icon5.addPixmap(QtGui.QPixmap(icons_path + "Door-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.AddDoorButton.setIcon(icon5)
		self.AddDoorButton.setIconSize(QtCore.QSize(48, 48))
		self.AddDoorButton.setCheckable(True)
		self.AddDoorButton.setChecked(False)
		self.AddDoorButton.setObjectName("AddDoorButton")
		self.verticalLayout_2.addWidget(self.AddDoorButton)
		self.AddTrashCanButton = QtWidgets.QPushButton(self.ActorBox)
		icon6 = QtGui.QIcon()
		icon6.addPixmap(QtGui.QPixmap(icons_path + "698410_trash_512x512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.AddTrashCanButton.setIcon(icon6)
		self.AddTrashCanButton.setIconSize(QtCore.QSize(48, 48))
		self.AddTrashCanButton.setCheckable(True)
		self.AddTrashCanButton.setChecked(False)
		self.AddTrashCanButton.setObjectName("AddTrashCanButton")
		self.verticalLayout_2.addWidget(self.AddTrashCanButton)
		self.AddGemSackButton = QtWidgets.QPushButton(self.ActorBox)
		icon7 = QtGui.QIcon()
		icon7.addPixmap(QtGui.QPixmap(icons_path + "Money-Bag-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.AddGemSackButton.setIcon(icon7)
		self.AddGemSackButton.setIconSize(QtCore.QSize(48, 48))
		self.AddGemSackButton.setCheckable(True)
		self.AddGemSackButton.setChecked(False)
		self.AddGemSackButton.setObjectName("AddGemSackButton")
		self.verticalLayout_2.addWidget(self.AddGemSackButton)
		self.verticalLayout.addWidget(self.ActorBox)
		self.ToolsDockWidget.setWidget(self.dockWidgetContents)
		self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.ToolsDockWidget)
		self.TilesDockWidget = QtWidgets.QDockWidget(self)
		self.TilesDockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetMovable)
		self.TilesDockWidget.setObjectName("TilesDockWidget")
		self.dockWidgetContents_2 = QtWidgets.QWidget()
		self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
		self.gridLayout_2 = QtWidgets.QGridLayout(self.dockWidgetContents_2)
		self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.listView_2 = QtWidgets.QListView(self.dockWidgetContents_2)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.listView_2.sizePolicy().hasHeightForWidth())
		self.listView_2.setSizePolicy(sizePolicy)
		self.listView_2.setObjectName("listView_2")
		self.gridLayout_2.addWidget(self.listView_2, 0, 0, 1, 1)
		self.TilesDockWidget.setWidget(self.dockWidgetContents_2)
		self.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.TilesDockWidget)
		self.objectsTockWidget = QtWidgets.QDockWidget(self)
		self.objectsTockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetMovable)
		self.objectsTockWidget.setObjectName("objectsTockWidget")
		self.dockWidgetContents_3 = QtWidgets.QWidget()
		self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
		self.gridLayout_3 = QtWidgets.QGridLayout(self.dockWidgetContents_3)
		self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_3.setObjectName("gridLayout_3")
		self.listView = QtWidgets.QListView(self.dockWidgetContents_3)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
		self.listView.setSizePolicy(sizePolicy)
		self.listView.setObjectName("listView")
		self.gridLayout_3.addWidget(self.listView, 0, 0, 1, 1)
		self.objectsTockWidget.setWidget(self.dockWidgetContents_3)
		self.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.objectsTockWidget)
		self.actionNew = QtWidgets.QAction(self)
		self.actionNew.setObjectName("actionNew")
		self.actionSave = QtWidgets.QAction(self)
		self.actionSave.setObjectName("actionSave")
		self.actionOpen = QtWidgets.QAction(self)
		self.actionOpen.setObjectName("actionOpen")
		self.menuFile.addAction(self.actionNew)
		self.menuFile.addAction(self.actionSave)
		self.menuFile.addAction(self.actionOpen)
		self.menubar.addAction(self.menuFile.menuAction())

		self.retranslateUi()
		QtCore.QMetaObject.connectSlotsByName(self)

	def retranslateUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("MainWindow", "Sneaksters Level Maker"))
		self.menuFile.setTitle(_translate("MainWindow", "File"))
		self.ToolsDockWidget.setWindowTitle(_translate("MainWindow", "Tools"))
		self.selectMoveButtom.setText(_translate("MainWindow", "Select && Move"))
		self.drawTilesButton.setText(_translate("MainWindow", "Draw Tiles"))
		self.ActorBox.setTitle(_translate("MainWindow", "Add Actors"))
		self.AddGuardButton.setText(_translate("MainWindow", "Guard"))
		self.AddCameraButton.setText(_translate("MainWindow", "Camera"))
		self.AddGemstoneButton.setText(_translate("MainWindow", "Gemstone"))
		self.AddDoorButton.setText(_translate("MainWindow", "Door"))
		self.AddTrashCanButton.setText(_translate("MainWindow", "Trash Can"))
		self.AddGemSackButton.setText(_translate("MainWindow", "Gem Sack"))
		self.TilesDockWidget.setWindowTitle(_translate("MainWindow", "Tiles"))
		self.objectsTockWidget.setWindowTitle(_translate("MainWindow", "Objects"))
		self.actionNew.setText(_translate("MainWindow", "New"))
		self.actionSave.setText(_translate("MainWindow", "Save"))
		self.actionOpen.setText(_translate("MainWindow", "Open"))

##########################################
##########################################
##########################################
class GridView(QtWidgets.QGraphicsView):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setRenderHints(self.renderHints() | QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)

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
		# CELL_SIZE.  We want to do this by *expanding* the rect -- that is,
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


	# 	# draw the lines - for numbers from 1 to 500 (or maybe zero, IDK) check if
	# 	divisible by 2; if so, multiply by 15 and draw it from
	# 	# (15x - halfOfWidth, -halfOfHeight) to (15x, height)
	# 	for x in range(1000):
	# 		if (x % 2 == 0):
	# 			painter.drawLine(x * 15 - halfOfWidth, 0 - halfOfHeight, x * 15 -
	# 			halfOfWidth, 1000)

	# 	# (-halfOfWidth, 15y - halfOfHeight) to (width, 15y - halfOfHeight)
	# 	for y in range(1000):
	# 		if (y % 2 == 0):
	# 			painter.drawLine(0 - halfOfWidth, y * 15 - halfOfHeight, 1000, y * 15 -
	# 			halfOfHeight)





if __name__ == '__main__':
	global app, window
	app = QtWidgets.QApplication(sys.argv)

	window = Window()
	window.show()
	sys.exit(app.exec_())

	