import os
import sys
import sneaklib

from PyQt5 import QtCore, QtGui, QtWidgets#, QtMacExtras
Qt = QtCore.Qt


global icons_path

global current_level


send_nudes = [[200.0, 240.0], [160.0, 240.0], [120.0, 240.0], [120.0, 280.0], [120.0, 320.0], [160.0, 320.0], [200.0, 320.0], [200.0, 360.0], [200.0, 400.0], [160.0, 400.0], [120.0, 400.0], [280.0, 240.0], [280.0, 280.0], [280.0, 320.0], [280.0, 360.0], [280.0, 400.0], [320.0, 400.0], [360.0, 400.0], [320.0, 320.0], [360.0, 320.0], [320.0, 240.0], [360.0, 240.0], [440.0, 240.0], [440.0, 280.0], [440.0, 320.0], [440.0, 360.0], [440.0, 400.0], [480.0, 280.0], [520.0, 320.0], [560.0, 360.0], [560.0, 400.0], [560.0, 320.0], [560.0, 280.0], [560.0, 240.0], [640.0, 240.0], [640.0, 280.0], [640.0, 320.0], [640.0, 360.0], [640.0, 400.0], [680.0, 240.0], [720.0, 280.0], [720.0, 320.0], [720.0, 360.0], [680.0, 400.0], [80.0, 480.0], [80.0, 520.0], [80.0, 560.0], [80.0, 600.0], [80.0, 640.0], [120.0, 520.0], [160.0, 560.0], [200.0, 480.0], [200.0, 520.0], [200.0, 560.0], [200.0, 600.0], [200.0, 640.0], [280.0, 480.0], [280.0, 520.0], [280.0, 560.0], [280.0, 600.0], [280.0, 640.0], [320.0, 640.0], [360.0, 640.0], [360.0, 600.0], [360.0, 560.0], [360.0, 520.0], [360.0, 480.0], [440.0, 480.0], [440.0, 520.0], [440.0, 560.0], [440.0, 600.0], [440.0, 640.0], [480.0, 480.0], [520.0, 520.0], [520.0, 560.0], [520.0, 600.0], [480.0, 640.0], [600.0, 480.0], [600.0, 520.0], [600.0, 560.0], [600.0, 600.0], [600.0, 640.0], [640.0, 640.0], [680.0, 640.0], [640.0, 560.0], [680.0, 560.0], [680.0, 480.0], [640.0, 480.0], [840.0, 480.0], [800.0, 480.0], [760.0, 480.0], [760.0, 520.0], [760.0, 560.0], [800.0, 560.0], [840.0, 560.0], [840.0, 600.0], [840.0, 640.0], [800.0, 640.0], [760.0, 640.0]]

square_button_style = "QPushButton {margin: 1px; padding: 1px; border: 1px; background-color: grey; image-position: center center; text-align: center;}"

CELL_SIZE = 40

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
1 = door
2 = actor
"""


class Window(QtWidgets.QMainWindow):
	"""Main Window"""

	
	
	def __init__(self, parent=None):
		global obj_mode
		obj_mode = 0

		super(Window, self).__init__(parent)
		

		print(icons_path)

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
		#self.toolPaletteWidget_DrawButton.hasHeightForWidth()
		self.toolPaletteWidget_DrawButton.setCheckable(True)
		self.toolPaletteWidget_DrawButton.setAutoExclusive(True)
		self.toolPaletteWidget_DrawButton.clicked.connect(self.EnableDrawMode)
		#self.toolPaletteWidget_DrawButton.setStyleSheet(square_button_style)

		

		self.toolPaletteWidget_EraseButton = QtWidgets.QPushButton("Erase")
		self.toolPaletteWidget_EraseButton.clicked.connect(self.EnableEraseMode)
		#self.toolPaletteWidget_EraseButton.setStyleSheet(square_button_style)
		#self.toolPaletteWidget_EraseButton.setFixedSize(40,40)



		self.toolPaletteWidget_EraseButton.setCheckable(True)
		self.toolPaletteWidget_EraseButton.setAutoExclusive(True)

		self.toolPaletteWidget_MoveButton = QtWidgets.QPushButton("Move")
		self.toolPaletteWidget_MoveButtonIco = QtGui.QIcon(icons_path + "arrow_rl.cur")
		#self.toolPaletteWidget_DrawButton.align
		self.toolPaletteWidget_MoveButton.setIcon(self.toolPaletteWidget_MoveButtonIco)
		
		#self.toolPaletteWidget_MoveButton.setFixedSize(45,40)
		self.toolPaletteWidget_MoveButton.setCheckable(True)
		self.toolPaletteWidget_MoveButton.setAutoExclusive(True)
		#self.toolPaletteWidget_MoveButton.setFixedSize(40,40)
		#self.toolPaletteWidget_MoveButton.setStyleSheet(square_button_style)


		self.toolPaletteWidget_Layout = QtWidgets.QVBoxLayout()
		self.toolPaletteWidget_Layout.addWidget(self.toolPaletteWidget_MoveButton)
		self.toolPaletteWidget_Layout.addSpacing(5)
		self.toolPaletteWidget_Layout.addWidget(self.toolPaletteWidget_DrawButton)
		self.toolPaletteWidget_Layout.addWidget(self.toolPaletteWidget_EraseButton)
		self.toolPaletteWidget_Layout.addSpacing(5)
		self.toolPaletteWidget_Layout.setAlignment(Qt.AlignTop)
		self.toolPaletteWidget_Layout.addStretch(10)

		self.toolPaletteWidget.setLayout(self.toolPaletteWidget_Layout)
		self.toolPalette.setWidget(self.toolPaletteWidget)
		self.toolPalette.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetMovable)
		self.addDockWidget(Qt.LeftDockWidgetArea, self.toolPalette)


		### OBJECT TYPE
		self.toolPaletteWidget_ObjType = QtWidgets.QGroupBox("Type")
		self.toolPaletteWidget_ObjType_Room = QtWidgets.QPushButton("Room")
		self.toolPaletteWidget_ObjType_Door = QtWidgets.QPushButton("Door")
		self.toolPaletteWidget_ObjType_Spr = QtWidgets.QPushButton("Actor")

		self.toolPaletteWidget_ObjType_Room.clicked.connect(self.SetRoomMode)
		self.toolPaletteWidget_ObjType_Door.clicked.connect(self.SetDoorMode)
		self.toolPaletteWidget_ObjType_Spr.clicked.connect(self.SetActorMode)


		self.toolPaletteWidget_ObjType_Room.setCheckable(True)
		self.toolPaletteWidget_ObjType_Door.setCheckable(True)
		self.toolPaletteWidget_ObjType_Spr.setCheckable(True)
		self.toolPaletteWidget_ObjType_Room.setAutoExclusive(True)
		self.toolPaletteWidget_ObjType_Door.setAutoExclusive(True)
		self.toolPaletteWidget_ObjType_Spr.setAutoExclusive(True)

		self.toolPaletteWidget_ObjTypeLayout = QtWidgets.QVBoxLayout()
		self.toolPaletteWidget_ObjTypeLayout.addWidget(self.toolPaletteWidget_ObjType_Room)
		self.toolPaletteWidget_ObjTypeLayout.addWidget(self.toolPaletteWidget_ObjType_Door)
		self.toolPaletteWidget_ObjTypeLayout.addWidget(self.toolPaletteWidget_ObjType_Spr)

		self.toolPaletteWidget_ObjType.setLayout(self.toolPaletteWidget_ObjTypeLayout)

		self.toolPaletteWidget_Layout.addWidget(self.toolPaletteWidget_ObjType)
		self.toolPaletteWidget_ObjType.setAlignment(Qt.AlignBottom)
		self.toolPaletteWidget_Layout.addChildLayout(self.toolPaletteWidget_ObjTypeLayout)
		self.toolPaletteWidget_ObjTypeLayout.setAlignment(Qt.AlignBottom)




		### actor LIST
		self.actorPalette = QtWidgets.QDockWidget()
		self.actorPalette.setWindowTitle("Actor Palette")
		self.actorPaletteWidget = QtWidgets.QListWidget()
		self.actorPalette.setWidget(self.actorPaletteWidget)
		self.addDockWidget(Qt.RightDockWidgetArea, self.actorPalette)


		self.actorPaletteWidget.addItem("Gemstone")
		self.actorPaletteWidget.addItem("Gem Sack")
		self.actorPaletteWidget.addItem("Guard")
		self.actorPaletteWidget.addItem("Trash Can")

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


		### BOTTOM BAR
		self.footerBar = QtWidgets.QStatusBar()
		self.footerBar_label = QtWidgets.QLabel("0 tiles, 0 actors")
		self.footerBar.addPermanentWidget(self.footerBar_label)
		self.setStatusBar(self.footerBar)

		self.setupMenuBar()

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

		data_to_save = current_level.PackTileData(current_level.tiles)
		file.write(data_to_save)
		file.close()

	def openFile(self):
		global current_level
		openFrom = QtWidgets.QFileDialog.getOpenFileName(self, "Open File")
		print(openFrom)
		if openFrom[0] == "":return
		file = open(openFrom[0], 'rb')

		current_level = sneaklib.SneakstersLevel()

		unpacked_data = current_level.UnpackTileData(file.read())
		file.close()

		self.gridScene.update(self.gridScene.sceneRect())
		self.UpdateStatusBar()



	def EnableEraseMode(self):
		global draw_mode
		draw_mode = 1
		print("ERASE MODE")
		print(draw_mode)

	def EnableDrawMode(self):
		global draw_mode
		draw_mode = 0

		print("DRAW MODE")

	def SetDoorMode(self):
		global obj_mode
		obj_mode = 1

	def SetRoomMode(self):
		global obj_mode
		obj_mode = 0

	def SetActorMode(self):
		global obj_mode
		obj_mode = 2



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
		print("move the view")
		super(GridView, self).mouseMoveEvent(event)



##########################################
##########################################
##########################################
class GridScene(QtWidgets.QGraphicsScene):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent

		self.setSceneRect(0, 0, 0x800, 0x800)

	def addNode(self, node):
		self.addItem(node)

		node.EstablishInputsOutputs()

	def mousePressEvent(self, event):
		global current_level
		#event.ignore()
		super(GridScene, self).mousePressEvent(event)
		self.PaintOrErase(event.scenePos().x(), event.scenePos().y())

	def PaintOrErase(self, fixedX, fixedY):
		global obj_mode
		self.update(self.sceneRect())

		nearestMultipleX = int(CELL_SIZE * round(float(fixedX) / CELL_SIZE))
		nearestMultipleY = int(CELL_SIZE * round(float(fixedY) / CELL_SIZE))

		tileX = fixedX // CELL_SIZE
		tileY = fixedY // CELL_SIZE

		#nearestMultipleX = event.scenePos().x() + (CELL_SIZE - event.scenePos().x()) % CELL_SIZE
		#nearestMultipleY = event.scenePos().y() + (CELL_SIZE - event.scenePos().y()) % CELL_SIZE

		array = [tileX, tileY]
		print("DRAW MODE IS " + str(draw_mode))
		if obj_mode == 0:
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

		elif (obj_mode == 1): # painting a door
			self.addItem(DoorItem(tileX, tileY - (CELL_SIZE / 8)))

		elif (obj_mode == 2): # painting a actor
			gem = current_level.GemstoneAt(*array)
			if draw_mode == 0:
				if not gem:

					## At present the GemstoneItem (graphical) is different from the data-structure
					## I tried to follow the way you did the tiles, where their data-structures and draw
					## functions were together, but they weren't painting. Until we figure it out, this will
					## work well enough.
					gem = sneaklib.Gemstone(*array, GemstoneItem(tileX, tileY))
					current_level.gemstones.append(gem)


					self.addItem(gem.graphicsItem)
			elif draw_mode == 1:
				if gem:
					current_level.gemstones.remove(gem)
					self.removeItem(gem.graphicsItem)
			print(current_level.gemstones)
		self.parent.UpdateStatusBar()


	def mouseMoveEvent(self, event):
		#event.ignore()
		#print("move the scene")
		super(GridScene, self).mouseMoveEvent(event)

		if event.buttons() == Qt.LeftButton:
			self.PaintOrErase(event.scenePos().x(), event.scenePos().y())

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

		current_level.draw(painter, CELL_SIZE)


class DoorItem(QtWidgets.QGraphicsItem):
	def __init__(self, xIn, yIn, parent=None):
		super().__init__(parent=parent)
		self.x = xIn
		self.y = yIn

		self.width = CELL_SIZE
		self.height = CELL_SIZE / 4

	def boundingRect(self):
		return QtCore.QRectF(self.x, self.y, self.width, self.height)

	def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
		painter.setBrush(QtGui.QBrush(QtGui.QColor(200,200,200)))
		painter.drawRect(self.x, self.y, CELL_SIZE, CELL_SIZE / 4)
		#super().paint(painter, QStyleOptionGraphicsItem, widget=widget)

class GemstoneItem(QtWidgets.QGraphicsItem):
	def __init__(self, xIn, yIn, parent=None):
		super().__init__(parent=parent)
		self.x = xIn
		self.y = yIn

	def boundingRect(self):
		return QtCore.QRectF(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

	def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
		painter.drawPixmap(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QtGui.QPixmap(icons_path + "official_sneaksters/gem.png"))





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