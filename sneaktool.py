import os
import sys
import sneaklib

from PyQt5 import QtCore, QtGui, QtWidgets#, QtMacExtras
Qt = QtCore.Qt


global icons_path

global current_level


send_nudes = [[200.0, 240.0], [160.0, 240.0], [120.0, 240.0], [120.0, 280.0], [120.0, 320.0], [160.0, 320.0], [200.0, 320.0], [200.0, 360.0], [200.0, 400.0], [160.0, 400.0], [120.0, 400.0], [280.0, 240.0], [280.0, 280.0], [280.0, 320.0], [280.0, 360.0], [280.0, 400.0], [320.0, 400.0], [360.0, 400.0], [320.0, 320.0], [360.0, 320.0], [320.0, 240.0], [360.0, 240.0], [440.0, 240.0], [440.0, 280.0], [440.0, 320.0], [440.0, 360.0], [440.0, 400.0], [480.0, 280.0], [520.0, 320.0], [560.0, 360.0], [560.0, 400.0], [560.0, 320.0], [560.0, 280.0], [560.0, 240.0], [640.0, 240.0], [640.0, 280.0], [640.0, 320.0], [640.0, 360.0], [640.0, 400.0], [680.0, 240.0], [720.0, 280.0], [720.0, 320.0], [720.0, 360.0], [680.0, 400.0], [80.0, 480.0], [80.0, 520.0], [80.0, 560.0], [80.0, 600.0], [80.0, 640.0], [120.0, 520.0], [160.0, 560.0], [200.0, 480.0], [200.0, 520.0], [200.0, 560.0], [200.0, 600.0], [200.0, 640.0], [280.0, 480.0], [280.0, 520.0], [280.0, 560.0], [280.0, 600.0], [280.0, 640.0], [320.0, 640.0], [360.0, 640.0], [360.0, 600.0], [360.0, 560.0], [360.0, 520.0], [360.0, 480.0], [440.0, 480.0], [440.0, 520.0], [440.0, 560.0], [440.0, 600.0], [440.0, 640.0], [480.0, 480.0], [520.0, 520.0], [520.0, 560.0], [520.0, 600.0], [480.0, 640.0], [600.0, 480.0], [600.0, 520.0], [600.0, 560.0], [600.0, 600.0], [600.0, 640.0], [640.0, 640.0], [680.0, 640.0], [640.0, 560.0], [680.0, 560.0], [680.0, 480.0], [640.0, 480.0], [840.0, 480.0], [800.0, 480.0], [760.0, 480.0], [760.0, 520.0], [760.0, 560.0], [800.0, 560.0], [840.0, 560.0], [840.0, 600.0], [840.0, 640.0], [800.0, 640.0], [760.0, 640.0]]

#square_button_style = "QPushButton {width: 20; height: 20;}"

CELL_SIZE = 40
#CURRENT_FLOOR = 0

global draw_mode
"""
Draw modes
0 = draw
1 = erase
"""

global obj_mode
"""
Object modes
0 = room
1 = wall
2 = door
3 = Actor
"""

global obj_selected
"""
Actors to select
0 = gemstone
1 = guard
"""

class Window(QtWidgets.QMainWindow):
	"""Main Window"""

	
	
	def __init__(self, parent=None):
		global obj_mode, obj_selected
		obj_mode = 0
		obj_selected = 0

		super(Window, self).__init__(parent)

		#print(icons_path)

		#self.setupUi()
		self.meorgeUI()
		self.gridView = GridView()
		
		self.gridScene = GridScene(parent=self)
		
		self.gridView.setScene(self.gridScene)
		
		self.gridView.setFrameRect(self.rect())
		self.gridView.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		
		#self.gridScene.set
		
		
		self.setCentralWidget(self.gridView)


		#self.resize(500,500)


	def meorgeUI(self):

		### TOOL PALETTE
		self.toolPalette = QtWidgets.QDockWidget()
		self.toolPalette.setWindowTitle("Tools")
		self.toolPaletteWidget = QtWidgets.QWidget()

		self.toolPaletteWidget_DrawButton = QtWidgets.QPushButton("Draw")
		self.toolPaletteWidget_DrawButtonIco = QtGui.QIcon(icons_path + "aero_pen_xl.cur")
		#self.toolPaletteWidget_DrawButton.align
		self.toolPaletteWidget_DrawButton.setIcon(self.toolPaletteWidget_DrawButtonIco)
		#self.toolPaletteWidget_DrawButton.setFlat(True)
		#self.toolPaletteWidget_DrawButton.setFixedSize(40,40)
		self.toolPaletteWidget_DrawButton.setCheckable(True)
		self.toolPaletteWidget_DrawButton.setAutoExclusive(True)
		self.toolPaletteWidget_DrawButton.clicked.connect(self.EnableDrawMode)
		

		
		self.toolPaletteWidget_EraseButton = QtWidgets.QPushButton("Erase")
		self.toolPaletteWidget_EraseButton.clicked.connect(self.EnableEraseMode)
		#self.toolPaletteWidget_EraseButton.setFixedSize(40,40)
		self.toolPaletteWidget_EraseButton.setCheckable(True)


		self.toolPaletteWidget_EraseButton.setCheckable(True)
		self.toolPaletteWidget_EraseButton.setAutoExclusive(True)

		self.toolPaletteWidget_MoveButton = QtWidgets.QPushButton("Select / Move")
		self.toolPaletteWidget_MoveButtonIco = QtGui.QIcon(icons_path + "arrow_rl.cur")
		self.toolPaletteWidget_MoveButton.clicked.connect(self.EnableMoveMode)
		self.toolPaletteWidget_MoveButton.setAutoExclusive(True)
		#self.toolPaletteWidget_DrawButton.align
		self.toolPaletteWidget_MoveButton.setIcon(self.toolPaletteWidget_MoveButtonIco)
		#self.toolPaletteWidget_MoveButton.setFixedSize(40,40)
		self.toolPaletteWidget_MoveButton.setCheckable(True)

		self.toolPaletteWidget_Layout = QtWidgets.QVBoxLayout()
		self.toolPaletteWidget_Layout.addWidget(self.toolPaletteWidget_MoveButton)
		self.toolPaletteWidget_Layout.addSpacing(5)
		self.toolPaletteWidget_Layout.addWidget(self.toolPaletteWidget_DrawButton)
		self.toolPaletteWidget_Layout.addWidget(self.toolPaletteWidget_EraseButton)
		self.toolPaletteWidget_Layout.addSpacing(5)
		self.toolPaletteWidget_Layout.setAlignment(Qt.AlignTop)

		self.toolPaletteWidget.setLayout(self.toolPaletteWidget_Layout)
		self.toolPalette.setWidget(self.toolPaletteWidget)
		self.toolPalette.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetMovable)
		self.addDockWidget(Qt.LeftDockWidgetArea, self.toolPalette)


		### OBJECT TYPE
		self.toolPaletteWidget_ObjType = QtWidgets.QGroupBox("Type")
		self.toolPaletteWidget_ObjType_Room = QtWidgets.QPushButton("Room")
		self.toolPaletteWidget_ObjType_FloorShape = QtWidgets.QPushButton("Floor Shape")
		self.toolPaletteWidget_ObjType_Wall = QtWidgets.QPushButton("Wall")
		self.toolPaletteWidget_ObjType_Door = QtWidgets.QPushButton("Door")
		self.toolPaletteWidget_ObjType_Spr = QtWidgets.QPushButton("Actor")
		
		self.toolPaletteWidget_ObjType_Room.clicked.connect(self.SetRoomMode)
		self.toolPaletteWidget_ObjType_FloorShape.clicked.connect(self.SetRoomShapeMode)
		self.toolPaletteWidget_ObjType_Wall.clicked.connect(self.EnableWallMode)
		self.toolPaletteWidget_ObjType_Door.clicked.connect(self.EnableDoorMode)
		self.toolPaletteWidget_ObjType_Spr.clicked.connect(self.SetActorMode)
		
		self.toolPaletteWidget_ObjType_Room.setCheckable(True)
		self.toolPaletteWidget_ObjType_Room.setAutoExclusive(True)
		
		# self.toolPaletteWidget_ObjType_FloorShape.setCheckable(True)
		# self.toolPaletteWidget_ObjType_FloorShape.setAutoExclusive(True)

		self.toolPaletteWidget_ObjType_Wall.setCheckable(True)
		self.toolPaletteWidget_ObjType_Wall.setAutoExclusive(True)

		self.toolPaletteWidget_ObjType_Door.setCheckable(True)
		self.toolPaletteWidget_ObjType_Door.setAutoExclusive(True)

		self.toolPaletteWidget_ObjType_Spr.setCheckable(True)
		self.toolPaletteWidget_ObjType_Spr.setAutoExclusive(True)

		self.toolPaletteWidget_ObjTypeLayout = QtWidgets.QVBoxLayout()
		self.toolPaletteWidget_ObjTypeLayout.addWidget(self.toolPaletteWidget_ObjType_Room)
		# self.toolPaletteWidget_ObjTypeLayout.addWidget(self.toolPaletteWidget_ObjType_FloorShape)
		self.toolPaletteWidget_ObjTypeLayout.addWidget(self.toolPaletteWidget_ObjType_Wall)
		self.toolPaletteWidget_ObjTypeLayout.addWidget(self.toolPaletteWidget_ObjType_Door)
		self.toolPaletteWidget_ObjTypeLayout.addWidget(self.toolPaletteWidget_ObjType_Spr)

		self.toolPaletteWidget_ObjType.setLayout(self.toolPaletteWidget_ObjTypeLayout)

		self.toolPaletteWidget_Layout.addStretch(10)
		self.toolPaletteWidget_Layout.addWidget(self.toolPaletteWidget_ObjType)
		self.toolPaletteWidget_ObjType.setAlignment(Qt.AlignBottom)
		self.toolPaletteWidget_Layout.addChildLayout(self.toolPaletteWidget_ObjTypeLayout)
		self.toolPaletteWidget_ObjTypeLayout.setAlignment(Qt.AlignBottom)




		### actor LIST
		self.actorPalette = QtWidgets.QDockWidget()
		self.actorPalette.setWindowTitle("Actor Palette")
		self.actorPaletteWidget = QtWidgets.QListWidget()
		self.actorPaletteWidget.currentRowChanged.connect(self.actorItemChanged)
		self.actorPalette.setWidget(self.actorPaletteWidget)
		self.addDockWidget(Qt.RightDockWidgetArea, self.actorPalette)


		self.actorPaletteWidget.addItem("Gemstone")
		self.actorPaletteWidget.addItem("Guard")
		self.actorPaletteWidget.addItem("Gem Sack")
		self.actorPaletteWidget.addItem("Trash Can")


		### ACTOR INFO
		self.actorInfo = QtWidgets.QWidget()
		self.actorInfo_actorIconLabel = QtWidgets.QLabel()

		self.actorInfo_actorIcon = QtGui.QPixmap(icons_path + "official_sneaksters/guard.png")
		self.actorInfo_actorIconLabel.setPixmap(self.actorInfo_actorIcon.scaled(40,40, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
		self.actorInfo_actorIconLabel.setFixedSize(40,40)
		self.actorInfo_actorName = QtWidgets.QLabel("Guard")
		self.actorInfo_actorPos = QtWidgets.QLabel("(300, 300)")

		self.actorInfo_labelsLayout = QtWidgets.QVBoxLayout()
		self.actorInfo_labelsLayout.addWidget(self.actorInfo_actorName)
		self.actorInfo_labelsLayout.addWidget(self.actorInfo_actorPos)

		# self.actorInfo_labelsWidget = QtWidgets.QWidget()
		# self.actorInfo_labelsWidget.setLayout(self.actorInfo_labelsLayout)

		self.actorInfo_headerLayout = QtWidgets.QHBoxLayout()
		self.actorInfo_headerLayout.addWidget(self.actorInfo_actorIconLabel)
		self.actorInfo_headerLayout.addLayout(self.actorInfo_labelsLayout)

		self.actorInfo_layout = QtWidgets.QVBoxLayout()

		self.actorInfo_nodeList = QtWidgets.QListWidget()
		self.actorInfo_addNodeButton = QtWidgets.QPushButton("Add Node")
		self.actorInfo_addNodeButton.clicked.connect(self.AddNodeToGuard)
		self.actorInfo_removeNodeButton = QtWidgets.QPushButton("Remove Node")
		self.actorInfo_nodeLayout = QtWidgets.QHBoxLayout()
		self.actorInfo_nodeLayout.addWidget(self.actorInfo_addNodeButton)
		self.actorInfo_nodeLayout.addWidget(self.actorInfo_removeNodeButton)
		
		self.actorInfo_layout.addLayout(self.actorInfo_headerLayout, 100)
		self.actorInfo_layout.addWidget(self.actorInfo_nodeList)
		self.actorInfo_layout.addLayout(self.actorInfo_nodeLayout)
		self.actorInfo.setLayout(self.actorInfo_layout)

		self.actorInfo_Panel = QtWidgets.QDockWidget()
		self.actorInfo_Panel.setWindowTitle("Actor Settings")
		self.actorInfo_Panel.setWidget(self.actorInfo)
		self.addDockWidget(Qt.RightDockWidgetArea, self.actorInfo_Panel)


		### CURRENT actorS
		self.currentActors = QtWidgets.QDockWidget()
		self.currentActors.setWindowTitle("Current actors")
		self.currentActorsWidget = QtWidgets.QTreeWidget()
		self.currentActors.setWidget(self.currentActorsWidget)
		self.addDockWidget(Qt.RightDockWidgetArea, self.currentActors)

		self.currentActorsWidget.setHeaderHidden(True)
		
		self.currentActorsWidget_Gems = QtWidgets.QTreeWidgetItem()
		self.currentActorsWidget_Gems.setText(0, "Gemstones")

		#self.currentActorsWidget_Gems.set

		self.currentActorsWidget.addTopLevelItem(self.currentActorsWidget_Gems)

		self.currentActorsWidget_Grds = QtWidgets.QTreeWidgetItem()
		self.currentActorsWidget_Grds.setText(0, "Guards")

		self.currentActorsWidget_GemSacks = QtWidgets.QTreeWidgetItem()
		self.currentActorsWidget_GemSacks.setText(0, "Gem Sacks")


		self.currentActorsWidget.addTopLevelItem(self.currentActorsWidget_Grds)
		self.currentActorsWidget.addTopLevelItem(self.currentActorsWidget_GemSacks)


		### BOTTOM BAR
		self.footerBar = QtWidgets.QStatusBar()
		self.footerBar_label = QtWidgets.QLabel("0 tiles, 0 sprites")

		self.zoomInButton = QtWidgets.QPushButton("+")
		self.zoomOutButton = QtWidgets.QPushButton("-")
		self.zoomInButton.setFixedSize(32,32)
		self.zoomOutButton.setFixedSize(32,32)
		self.zoomInButton.clicked.connect(self.zoomIn)
		self.zoomOutButton.clicked.connect(self.zoomOut)
		self.footerBar.addWidget(self.zoomInButton)
		self.footerBar.addWidget(self.zoomOutButton)

		
		#self.FloorUpButton = QtWidgets.QPushButton("Go Upstairs")
		#self.FloorDownButton = QtWidgets.QPushButton("Go Downstairs")
		#self.FloorLevel = QtWidgets.QLabel("Floor 0")

		#self.FloorUpButton.clicked.connect(self.FloorUp)
		#self.FloorDownButton.clicked.connect(self.FloorDown)
		
		#self.footerBar.addWidget(self.FloorUpButton)
		#self.footerBar.addWidget(self.FloorLevel)
		#self.footerBar.addWidget(self.FloorDownButton)
		
		self.footerBar.addPermanentWidget(self.footerBar_label)

		self.setStatusBar(self.footerBar)

		self.setupMenuBar()

		self.UpdateSelection()

	def UpdateStatusBar(self):
		global current_level
		self.footerBar_label.setText(str(len(current_level.tiles)) + " rooms")


	def setupMenuBar(self):
		self.menuBar = QtWidgets.QMenuBar()
		self.fileMenu = self.menuBar.addMenu("&File")

		self.saveAsAction = QtWidgets.QAction("&Save As", self)
		self.saveAsAction.setShortcut(QtGui.QKeySequence.Save)
		self.saveAsAction.triggered.connect(self.saveFileAs)

		self.openAction = QtWidgets.QAction("&Open", self)
		self.openAction.setShortcut(QtGui.QKeySequence.Open)
		self.openAction.triggered.connect(self.openFile)

		self.fileMenu.addAction(self.saveAsAction)
		self.fileMenu.addAction(self.openAction)
		self.setMenuBar(self.menuBar)


	def saveFileAs(self):
		saveTo = QtWidgets.QFileDialog.getSaveFileName(self, "Save File")
		print(saveTo)
		if saveTo[0] == "": return
		file = open(saveTo[0], 'wb')
		data_to_save = current_level.PackLevelData()
		file.write(data_to_save)
		file.close()

	def openFile(self):
		global current_level
		openFrom = QtWidgets.QFileDialog.getOpenFileName(self, "Open File")
		print(openFrom)
		if openFrom[0] == "":return
		file = open(openFrom[0], 'rb')

		self.gridScene.clearObjects()

		current_level = sneaklib.SneakstersLevel()

		current_level.UnpackLevelData(file.read())
		file.close()

		self.UpdateActorList()
		self.gridScene.update(self.gridScene.sceneRect())



		
	def EnableMoveMode(self):
		global draw_mode
		draw_mode = 2
		self.gridScene.update()
		print("MOVE MODE")
		print(draw_mode)

	def EnableEraseMode(self):
		global draw_mode
		draw_mode = 1
		self.gridScene.update()
		print("ERASE MODE")
		print(draw_mode)

	def EnableDrawMode(self):
		global draw_mode
		draw_mode = 0

		self.gridScene.update()
		print("DRAW MODE")


	def EnableWallMode(self):
		global obj_mode
		obj_mode = 1

		self.gridScene.update()
		print("WALL MODE")
		print(obj_mode)

	def EnableDoorMode(self):
		global obj_mode
		obj_mode = 2

		self.gridScene.update()
		print("DOOR MODE")
		print(obj_mode)
		
	def zoomIn(self):
		global CELL_SIZE
		CELL_SIZE += 10
		self.gridScene.update()
		self.gridScene.UpdateSize()
		
	def zoomOut(self):
		global CELL_SIZE
		CELL_SIZE -= 10
		if CELL_SIZE < 10:
			CELL_SIZE = 10
		else:
			self.gridScene.update()
			self.gridScene.UpdateSize()
		
	#def FloorUp(self):
	#	global CURRENT_FLOOR
	#	CURRENT_FLOOR += 1
	#	self.gridScene.update()
	#	self.gridScene.UpdateSize()
	#	
	#def FloorDown(self):
	#	global CURRENT_FLOOR
	#	CURRENT_FLOOR += 1
	#	if CURRENT_FLOOR < 0:
	#		CURRENT_FLOOR = 0
	#	else:
	#		self.gridScene.update()
	#		self.gridScene.UpdateSize()
	
	def SetRoomMode(self):
		global obj_mode
		obj_mode = 0

		self.gridScene.update()

	def SetActorMode(self):
		global obj_mode

		self.gridScene.update()

		print("ACTOR MODE ACTIVATE")
		obj_mode = 3

	def SetRoomShapeMode(self):
		global obj_mode
		obj_mode = 4


	def actorItemChanged(self, currentRow):
		global obj_selected
		obj_selected = currentRow

		
	def UpdateActorList(self):
		self.UpdateGemstoneList()
		self.UpdateGuardList()

	def UpdateGemstoneList(self):
		for i in reversed(range(self.currentActorsWidget_Gems.childCount())):
			self.currentActorsWidget_Gems.removeChild(self.currentActorsWidget_Gems.child(i))

		for g in current_level.gemstones:
			newItem = QtWidgets.QTreeWidgetItem()
			newItem.setText(0, "(" + str(g.x) + ", " + str(g.y) + ")")
			self.currentActorsWidget_Gems.addChild(newItem)
		
		self.currentActorsWidget_Gems.setText(0, "Gemstones (" + str(len(current_level.gemstones)) + ")")

	def UpdateGuardList(self):
		for i in reversed(range(self.currentActorsWidget_Grds.childCount())):
			self.currentActorsWidget_Grds.removeChild(self.currentActorsWidget_Grds.child(i))

		for g in current_level.guards:
			newItem = QtWidgets.QTreeWidgetItem()
			newItem.setText(0, "(" + str(g.x) + ", " + str(g.y) + ")")
			self.currentActorsWidget_Grds.addChild(newItem)
		
		self.currentActorsWidget_Grds.setText(0, "Guards (" + str(len(current_level.guards)) + ")")

	def UpdateGemSackList(self):
		for i in reversed(range(self.currentActorsWidget_GemSacks.childCount())):
			self.currentActorsWidget_GemSacks.removeChild(self.currentActorsWidget_GemSacks.child(i))

		for g in current_level.gemSacks:
			newItem = QtWidgets.QTreeWidgetItem()
			newItem.setText(0, "(" + str(g.x) + ", " + str(g.y) + ")")
			self.currentActorsWidget_GemSacks.addChild(newItem)
		
		self.currentActorsWidget_GemSacks.setText(0, "Gem Sacks (" + str(len(current_level.gemSacks)) + ")")

	def UpdateSelection(self):
		if len(current_level.selectedActors) == 1:
			currentSelected = current_level.selectedActors[0]
			self.actorInfo_actorPos.setText("(" + str(int(currentSelected.x)) + ", " + str(int(currentSelected.y)) + ")")
			if type(currentSelected) is sneaklib.Gemstone:
				self.actorInfo_actorName.setText("Gemstone")
				gemIco = QtGui.QPixmap(icons_path + "official_sneaksters/gem.png")
				self.actorInfo_actorIconLabel.setPixmap(gemIco.scaled(40,40, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))

				self.actorInfo_addNodeButton.setEnabled(False)
				self.actorInfo_removeNodeButton.setEnabled(False)

			elif type(currentSelected) is sneaklib.Guard:
				self.actorInfo_actorName.setText("Guard")
				guardIco = QtGui.QPixmap(icons_path + "official_sneaksters/guard.png")
				self.actorInfo_actorIconLabel.setPixmap(guardIco.scaled(40,40, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
				self.actorInfo_addNodeButton.setEnabled(True)
				self.actorInfo_removeNodeButton.setEnabled(True)

			elif type(currentSelected) is sneaklib.GuardNode:
				self.actorInfo_actorName.setText("Guard")
				guardIco = QtGui.QPixmap(icons_path + "official_sneaksters/guard.png")
				self.actorInfo_actorIconLabel.setPixmap(guardIco.scaled(40,40, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
				self.actorInfo_addNodeButton.setEnabled(True)
				self.actorInfo_removeNodeButton.setEnabled(True)
				self.actorInfo_actorPos.setText("(" + str(currentSelected.guard.x) + ", " + str(currentSelected.guard.y) + ")")

			elif type(currentSelected) is sneaklib.GemSack:
				self.actorInfo_actorName.setText("Gem Sack")
				gemsackIco = QtGui.QPixmap(icons_path + "official_sneaksters/gem_sack_ico.png")
				self.actorInfo_actorIconLabel.setPixmap(gemsackIco.scaled(40,40, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))

				self.actorInfo_addNodeButton.setEnabled(False)
				self.actorInfo_removeNodeButton.setEnabled(False)

		elif len(current_level.selectedActors) > 1:
			self.actorInfo_actorName.setText("Multiple actors selected")
			self.actorInfo_actorPos.setText("")
			self.actorInfo_actorIconLabel.clear()
			self.actorInfo_addNodeButton.setEnabled(False)
			self.actorInfo_removeNodeButton.setEnabled(False)

		else:
			self.actorInfo_actorName.setText("No actors selected")
			self.actorInfo_actorPos.setText("")
			self.actorInfo_actorIconLabel.clear()
			self.actorInfo_addNodeButton.setEnabled(False)
			self.actorInfo_removeNodeButton.setEnabled(False)


	def AddNodeToGuard(self):
		if type(current_level.selectedActors[0]) is sneaklib.Guard:
			x = current_level.selectedActors[0].x
			y = current_level.selectedActors[0].y
		else:
			x = current_level.selectedActors[0].guard.x
			y = current_level.selectedActors[0].guard.y

		newNode = sneaklib.GuardNode(x, y)

		if type(current_level.selectedActors[0]) is sneaklib.Guard:
			current_level.selectedActors[0].AddNode(newNode)
		else:
			current_level.selectedActors[0].guard.AddNode(newNode)

		self.gridScene.update()

		self.UpdateNodeList()

	def UpdateNodeList(self):
		print("UPDATE NODE LIST")
		for i in reversed(range(self.actorInfo_nodeList.count())):
			self.actorInfo_nodeList.takeItem(i)

		if len(current_level.selectedActors) == 0:
			return
		if type(current_level.selectedActors[0]) is sneaklib.Guard:
			guard = current_level.selectedActors[0]
		elif type(current_level.selectedActors[0]) is sneaklib.GuardNode:
			guard = current_level.selectedActors[0].guard
		else:
			return



		for node in guard.nodes:
			self.actorInfo_nodeList.addItem("(" + str(int(node.x)) + ", " + str(int(node.y)) + ")")


			
		


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
		#event.ignore()
		super(GridView, self).mousePressEvent(event)
		#print(event.x(), event.y())
		
		#self.scene().update(self.sceneRect())
		#current_level.tiles.append([event.x(), event.y()])
		#self.repaint(0,0,1000,1000)

	def mouseMoveEvent(self, event):
		event.ignore()
		#print("move the view")
		super(GridView, self).mouseMoveEvent(event)



##########################################
##########################################
##########################################
class GridScene(QtWidgets.QGraphicsScene):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent
		self.UpdateSize()
		self.mouseDown = False
	def UpdateSize(self):
		self.setSceneRect(0, 0, 0x80000/CELL_SIZE, 0x80000/CELL_SIZE)
	def addNode(self, node):
		self.addItem(node)

		node.EstablishInputsOutputs()
		
	def clearObjects(self):
		for gem in current_level.gemstones:
			self.removeItem(gem)

	def mousePressEvent(self, event):
		global current_level
		#event.ignore()
		super(GridScene, self).mousePressEvent(event)
		self.update(self.sceneRect())

		fixedX = event.scenePos().x()
		fixedY = event.scenePos().y()

		# nearestMultipleX = int(CELL_SIZE * round(float(fixedX) / CELL_SIZE))
		# nearestMultipleY = int(CELL_SIZE * round(float(fixedY) / CELL_SIZE))

		tileX = fixedX // CELL_SIZE
		tileY = fixedY // CELL_SIZE
		tile_x_pos = (fixedX / CELL_SIZE) % 1.0
		tile_y_pos = (fixedY / CELL_SIZE) % 1.0

		#nearestMultipleX = event.scenePos().x() + (CELL_SIZE - event.scenePos().x()) % CELL_SIZE
		#nearestMultipleY = event.scenePos().y() + (CELL_SIZE - event.scenePos().y()) % CELL_SIZE

		array = [tileX, tileY]
		print("DRAW MODE IS " + str(draw_mode))
		if draw_mode == 2:
			if((QtGui.QGuiApplication.keyboardModifiers() & QtCore.Qt.ShiftModifier) != QtCore.Qt.ShiftModifier):
				current_level.selectedActors.clear()
			obj = current_level.ObjectAt(*array)
			if obj:
				if obj not in current_level.selectedActors: current_level.selectedActors.append(obj)
				else: current_level.selectedActors.remove(obj)

			self.parent.UpdateNodeList()
		elif obj_mode == 0:
			if draw_mode == 0:
				tile = current_level.TileAt(*array)
				if not tile:
					tile = sneaklib.Tile(*array)
					current_level.tiles.append(tile)
					current_level.AutoWall(tile)
			elif draw_mode == 1:
				tile = current_level.TileAt(*array)
				if tile:
					current_level.tiles.remove(tile)
					current_level.AutoWall(tile, True)
		elif obj_mode == 1: ### WALL
			tile = current_level.TileAt(*array)
			if tile:
				if tile_x_pos < 0.25:
					sideTile = current_level.TileAt(tile.x-1, tile.y)
					tile.walls[3] = not tile.walls[3]
					if sideTile:
						sideTile.walls[1] = tile.walls[3]
				elif tile_x_pos >= 0.75:
					sideTile = current_level.TileAt(tile.x+1, tile.y)
					tile.walls[1] = not tile.walls[1]
					if sideTile:
						sideTile.walls[3] = tile.walls[1]
				elif tile_y_pos < 0.25:
					sideTile = current_level.TileAt(tile.x, tile.y-1)
					tile.walls[0] = not tile.walls[0]
					if sideTile:
						sideTile.walls[2] = tile.walls[0]
				elif tile_y_pos >= 0.75:
					sideTile = current_level.TileAt(tile.x, tile.y+1)
					tile.walls[2] = not tile.walls[2]
					if sideTile:
						sideTile.walls[0] = tile.walls[2]

		elif obj_mode == 2: ### DOOR
			tile = current_level.TileAt(*array)
			if tile:
				if tile_x_pos < 0.25: # left door
					sideTile = current_level.TileAt(tile.x-1, tile.y)
					tile.walls[7] = not tile.walls[7]
					tile.walls[3] = False

					if sideTile:
						sideTile.walls[1] = False
						sideTile.walls[5] = False

				elif tile_x_pos >= 0.75: # right door
					sideTile = current_level.TileAt(tile.x+1, tile.y)
					tile.walls[5] = not tile.walls[5]
					tile.walls[1] = False

					if sideTile:
						sideTile.walls[3] = False
						sideTile.walls[7] = False

				elif tile_y_pos < 0.25: # top door
					sideTile = current_level.TileAt(tile.x, tile.y-1)
					tile.walls[4] = not tile.walls[4]
					tile.walls[0] = False

					if sideTile:
						sideTile.walls[2] = False
						sideTile.walls[6] = False

				elif tile_y_pos >= 0.75:
					sideTile = current_level.TileAt(tile.x, tile.y+1)
					tile.walls[6] = not tile.walls[6]
					tile.walls[2] = False

					if sideTile:
						sideTile.walls[0] = False
						sideTile.walls[4] = False





		elif obj_mode == 3:
			if obj_selected == 0: ### GEMSTONE SELECTED
				gem = current_level.GemstoneAt(*array)
				if draw_mode == 0:
					if not gem:

						## At present the GemstoneItem (graphical) is different from the data-structure
						## I tried to follow the way you did the tiles, where their data-structures and draw
						## functions were together, but they weren't painting. Until we figure it out, this will
						## work well enough.
						gem = sneaklib.Gemstone(*array)
						current_level.gemstones.append(gem)
						#self.addItem(gem.graphicsItem)
				elif draw_mode == 1:
					if gem:
						current_level.gemstones.remove(gem)
						#self.removeItem(gem.graphicsItem)

			elif obj_selected == 1: ### GUARD SELECTED
				guard = current_level.GuardAt(*array)
				if draw_mode == 0:
					if not guard:
						guard = sneaklib.Guard(*array)
						current_level.guards.append(guard)

				elif draw_mode == 1:
					if guard:
						current_level.guards.remove(guard)
				#self.parent.UpdateNodeList()

			elif obj_selected == 2: ### GEM SACK
				gemSack = current_level.GemSackAt(*array)
				if draw_mode == 0:
					if not gemSack:
						gemSack = sneaklib.GemSack(*array)
						current_level.gemSacks.append(gemSack)
				elif draw_mode == 1:
					if gemSack:
						current_level.gemSacks.remove(gemSack)

				self.parent.UpdateGemSackList()
			self.parent.UpdateNodeList()
						

		elif obj_mode == 4:
			tile = current_level.TileAt(*array)
			if tile:
				tile.shape+=1
				if tile.shape > 4:
					tile.shape = 0
				current_level.AutoWall(tile)
		self.tileX = tileX
		self.tileY = tileY
		self.mouseDown = True
		self.parent.UpdateActorList()
		self.parent.UpdateStatusBar()
		self.parent.UpdateSelection()

	def mouseReleaseEvent(self, event):
		self.mouseDown = False
	def mouseMoveEvent(self, event):
		if not self.mouseDown:
			event.ignore()
			return
		#print("move the scene")
		super(GridScene, self).mouseMoveEvent(event)
		
		if len(current_level.selectedActors) == 0: return
		self.parent.UpdateSelection()
		self.parent.UpdateGemstoneList()
		self.parent.UpdateGuardList()
		self.parent.UpdateNodeList()
		self.parent.UpdateGemSackList()
		fixedX = event.scenePos().x()
		fixedY = event.scenePos().y()
		tileX = fixedX // CELL_SIZE
		tileY = fixedY // CELL_SIZE
		tile_x_pos = (fixedX / CELL_SIZE) % 1.0
		tile_y_pos = (fixedY / CELL_SIZE) % 1.0

		current_level.moveSelectedObjects(tileX - self.tileX, tileY - self.tileY)
		self.tileX = tileX
		self.tileY = tileY
		self.parent.UpdateActorList()
		self.update()


	def drawBackground(self, painter, rect):
		#print("boopy")
		#print(current_level.tiles)
		painter.setBrush(QtGui.QBrush(QtGui.QColor(50,50,50)))
		painter.drawRect(rect)

		self.gridPen = QtGui.QPen(QtGui.QColor(85,85,85), 1, Qt.DotLine)
		painter.setPen(self.gridPen)


		# stuff past this point in this func is written by RoadrunnerWMC,
		# who is really cool.

		

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

		current_level.draw(painter, CELL_SIZE, obj_mode == 2)

# class GemstoneItem(QtWidgets.QGraphicsItem):
# 	def __init__(self, xIn, yIn, parent=None):
# 		super().__init__(parent=parent)
# 		self.x = xIn
# 		self.y = yIn

# 	def boundingRect(self):
# 		return QtCore.QRectF(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

# 	def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
# 		None





if __name__ == '__main__':
	global app, window, current_level

	draw_mode = 0
	current_level = sneaklib.SneakstersLevel()

	icons_path = os.path.dirname(__file__)
	if (sys.platform == "darwin"):
		icons_path += "icons/"
	else:
		icons_path += "/icons/"

	app = QtWidgets.QApplication(sys.argv)

	window = Window()
	window.show()
	sys.exit(app.exec_())

	