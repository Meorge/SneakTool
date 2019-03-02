import struct
import os, sys
import binascii
from PyQt5 import QtCore, QtGui, QtWidgets #, QtMacExtras

size = 40

class SneakObj():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		#Do you want a Z for floors?
		# - probably not necessary right now

class Actor(SneakObj):
	def __init__(self, x, y):
		super().__init__(x, y)


class Gemstone(Actor):
	def __init__(self, x, y, graphicsItem):
		super().__init__(x, y)
		self.graphicsItem = graphicsItem

	def boundingRect(self):
		return QtCore.QRectF(self.x * size, self.y * size, size, size)

	def draw(self, painter, size):
		painter.drawPixmap(self.x * size, self.y * size, size, size, QtGui.QPixmap(icons_path + "official_sneaksters/gem.png"))



class Tile(SneakObj):
	squareBrush = QtGui.QBrush(QtGui.QColor(170,170,170))
	wallPen = QtGui.QPen(QtGui.QColor(240,0,0), 4)
	diagWallPen = QtGui.QPen(QtGui.QColor(0,0,240), 4)
	clearPen = QtGui.QPen(QtGui.QColor(0,0,0,48))
	def __init__(self, x, y, flags = 0):
		super(Tile, self).__init__(x, y)
		self.walls = [(flags & 1) != 0, ((flags>>1) & 1) != 0, ((flags>>2) & 1) != 0, ((flags>>3) & 1) != 0, ((flags>>4) & 1) != 0, ((flags>>5) & 1) != 0]
		self.shape = (flags>>6)%4

	def flags(self):
		flag = 0
		for i in range(len(self.walls)):
			flag |= self.walls[i] << i
		flag |= self.shape << 6
		return flag

	def drawDiagnalWalls(self,painter,dx,dy,size, show_disabled):
		if self.walls[4] ^ show_disabled:
			painter.drawLine(dx,		dy,			dx+size-1,	dy+size-1)
		if self.walls[5] ^ show_disabled:
			painter.drawLine(dx,		dy+size-1,	dx+size-1,	dy)

	def draw(self, painter, size, show_diag_walls = False):
		painter.setBrush(self.squareBrush)
		painter.setPen(self.clearPen)
		dx = self.x*size
		dy = self.y*size
		if self.shape == 0:
			painter.drawRect(dx, dy, size, size)
		elif self.shape == 1:
			painter.drawPolygon(QtCore.QPoint(dx, dy), QtCore.QPoint(dx+size-1, dy), QtCore.QPoint(dx, dy+size-1))
		elif self.shape == 2:
			painter.drawPolygon(QtCore.QPoint(dx+size-1, dy), QtCore.QPoint(dx+size-1, dy+size-1), QtCore.QPoint(dx, dy))
		elif self.shape == 3:
			painter.drawPolygon(QtCore.QPoint(dx+size-1, dy), QtCore.QPoint(dx+size-1, dy+size-1), QtCore.QPoint(dx, dy+size-1))
		elif self.shape == 4:
			painter.drawPolygon(QtCore.QPoint(dx+size-1, dy+size-1), QtCore.QPoint(dx, dy+size-1), QtCore.QPoint(dx, dy))
		painter.setPen(self.wallPen)
		if self.walls[0]:
			painter.drawLine(dx,		dy,			dx+size-1,	dy)
		if self.walls[1]:
			painter.drawLine(dx+size-1,	dy,			dx+size-1,	dy+size-1)
		if self.walls[2]:
			painter.drawLine(dx+size-1,	dy+size-1,	dx,			dy+size-1)
		if self.walls[3]:
			painter.drawLine(dx,		dy+size-1,	dx,			dy)
		if show_diag_walls:
			painter.setPen(self.clearPen)
			self.drawDiagnalWalls(painter,dx,dy,size, show_diag_walls)
		painter.setPen(self.diagWallPen)
		self.drawDiagnalWalls(painter,dx,dy,size, False)


class SneakstersLevel:
	#send_nudes = [[200.0, 240.0], [160.0, 240.0], [120.0, 240.0], [120.0, 280.0], [120.0, 320.0], [160.0, 320.0], [200.0, 320.0], [200.0, 360.0], [200.0, 400.0], [160.0, 400.0], [120.0, 400.0], [280.0, 240.0], [280.0, 280.0], [280.0, 320.0], [280.0, 360.0], [280.0, 400.0], [320.0, 400.0], [360.0, 400.0], [320.0, 320.0], [360.0, 320.0], [320.0, 240.0], [360.0, 240.0], [440.0, 240.0], [440.0, 280.0], [440.0, 320.0], [440.0, 360.0], [440.0, 400.0], [480.0, 280.0], [520.0, 320.0], [560.0, 360.0], [560.0, 400.0], [560.0, 320.0], [560.0, 280.0], [560.0, 240.0], [640.0, 240.0], [640.0, 280.0], [640.0, 320.0], [640.0, 360.0], [640.0, 400.0], [680.0, 240.0], [720.0, 280.0], [720.0, 320.0], [720.0, 360.0], [680.0, 400.0], [80.0, 480.0], [80.0, 520.0], [80.0, 560.0], [80.0, 600.0], [80.0, 640.0], [120.0, 520.0], [160.0, 560.0], [200.0, 480.0], [200.0, 520.0], [200.0, 560.0], [200.0, 600.0], [200.0, 640.0], [280.0, 480.0], [280.0, 520.0], [280.0, 560.0], [280.0, 600.0], [280.0, 640.0], [320.0, 640.0], [360.0, 640.0], [360.0, 600.0], [360.0, 560.0], [360.0, 520.0], [360.0, 480.0], [440.0, 480.0], [440.0, 520.0], [440.0, 560.0], [440.0, 600.0], [440.0, 640.0], [480.0, 480.0], [520.0, 520.0], [520.0, 560.0], [520.0, 600.0], [480.0, 640.0], [600.0, 480.0], [600.0, 520.0], [600.0, 560.0], [600.0, 600.0], [600.0, 640.0], [640.0, 640.0], [680.0, 640.0], [640.0, 560.0], [680.0, 560.0], [680.0, 480.0], [640.0, 480.0], [840.0, 480.0], [800.0, 480.0], [760.0, 480.0], [760.0, 520.0], [760.0, 560.0], [800.0, 560.0], [840.0, 560.0], [840.0, 600.0], [840.0, 640.0], [800.0, 640.0], [760.0, 640.0]]
	
	def __init__(self):
		super().__init__()

		self.tiles = []
		self.gemstones = []

		#glarp = self.PackTileData(self.send_nudes)
		#print(self.UnpackTileData(glarp))
		
	def TileAt(self, x, y):
		for tile in self.tiles:
			if tile.x == x and tile.y == y:
				return tile
		return None

	def GemstoneAt(self, x, y):
		for gem in self.gemstones:
			if gem.x == x and gem.y == y:
				return gem
		return None

	def AutoWall(self, tile, removing = False):
		tileTop = self.TileAt(tile.x, tile.y-1)
		tileRight = self.TileAt(tile.x+1, tile.y)
		tileBottom = self.TileAt(tile.x, tile.y+1)
		tileLeft = self.TileAt(tile.x-1, tile.y)
		
		if tileTop:
			if \
				tileTop.shape == 1 or\
				tileTop.shape == 2:
				tileTop = None
		if tileRight:
			if \
				tileRight.shape == 2 or\
				tileRight.shape == 3:
				tileRight = None
		if tileBottom:
			if \
				tileBottom.shape == 3 or\
				tileBottom.shape == 4:
				tileBottom = None
		if tileLeft:
			if \
				tileLeft.shape == 4 or\
				tileLeft.shape == 1:
				tileLeft = None
				

		if removing:
			if tileTop:
				tileTop.walls[2] = True
								
			if tileRight:		
				tileRight.walls[3] = True
								
			if tileBottom:		
				tileBottom.walls[0] = True
								
			if tileLeft:		
				tileLeft.walls[1] = True
			return

		if tileTop:
			tile.walls[0] = tileTop.walls[2] = False
		else:
			tile.walls[0] = True
			
		if tileRight:
			tile.walls[1] = tileRight.walls[3] = False
		else:
			tile.walls[1] = True

		if tileBottom:
			tile.walls[2] = tileBottom.walls[0] = False
		else:
			tile.walls[2] = True

		if tileLeft:
			tile.walls[3] = tileLeft.walls[1] = False
		else:
			tile.walls[3] = True

		if tile.shape == 1:
			tile.walls[1] = False
			tile.walls[2] = False

		elif tile.shape == 2:
			tile.walls[2] = False
			tile.walls[3] = False

		elif tile.shape == 3:
			tile.walls[0] = False
			tile.walls[3] = False

		elif tile.shape == 4:
			tile.walls[0] = False
			tile.walls[1] = False


	def draw(self, painter, size, show_diag_walls = False):
		for tile in self.tiles:
			tile.draw(painter, size, show_diag_walls)

		for gem in self.gemstones:
			gem.draw(painter, size)
	def PackLevelData(self):
		headerPacker = struct.Struct('4sIIII')
		packed = b''
		while ((len(packed) + headerPacker.size) % 0x10)!=0:
			packed+=b'\0'
		TileArrayOffset = len(packed) + headerPacker.size
		TileArrayData = self.PackTileData()
		packed += TileArrayData
		while ((len(packed) + headerPacker.size) % 0x10)!=0:
			packed+=b'\0'
		GemstoneArrayOffset = len(packed) + headerPacker.size
		GemstoneArrayData = self.PackGemstoneData()
		packed += GemstoneArrayData

		return headerPacker.pack(b'LEVL', TileArrayOffset, len(TileArrayData), GemstoneArrayOffset, len(GemstoneArrayData)) + packed
	def UnpackLevelData(self, data):
		headerUnpacker = struct.Struct('4sIIII')
		header = headerUnpacker.unpack(data[:headerUnpacker.size])
		self.UnpackTileData(data[header[1]:header[1]+header[2]])
		self.UnpackGemstoneData(data[header[3]:header[3]+header[4]])

	def PackTileData(self):
		numberOfTiles = len(self.tiles)
		firstPacker = struct.Struct('4sI')

		data = (b"TILE", numberOfTiles)
		packed = firstPacker.pack(*data)
		#print(len(packed))



		for tile in self.tiles:
			tilePacker = struct.Struct('HHH')
			#print(tilePacker.size)
			tileData = (int(tile.x), int(tile.y), tile.flags())
			packed += tilePacker.pack(*tileData)

		#print(binascii.hexlify(packed))
		return packed

	def UnpackTileData(self, data):
		headerUnpacker = struct.Struct('4sI')

		self.header = []
		header = headerUnpacker.unpack(data[:8])
		numberOfTiles = header[1]
		for i in range(numberOfTiles):
			tileUnpacker = struct.Struct('HHH')

			#print(tileUnpacker.size)
			unpacked = tileUnpacker.unpack_from(data, 8 + (tileUnpacker.size * i))
			tile = Tile(unpacked[0], unpacked[1], unpacked[2])
			self.tiles.append(tile)
		#print(header)
		#print(dataOut)


	def PackGemstoneData(self):
		headerPacker = struct.Struct('4sI')
		header = (b"GEMS", len(self.gemstones))

		packed = headerPacker.pack(*header)

		for gem in self.gemstones:
			gemPacker = struct.Struct('HHH')
			gemData = (int(gem.x), int(gem.y), 0) # including a flag int just in case we wanna add flags to gems
			packed += gemPacker.pack(*gemData)

		return packed

	def UnpackGemstoneData(self, data):
		headerUnpacker = struct.Struct('4sI')

		gemHeader = []
		gemHeader = headerUnpacker.unpack(data[:8])

		numberOfGems = gemHeader[1]

		for i in range(numberOfGems):
			gemUnpacker = struct.Struct('HHH')

			unpacked = gemUnpacker.unpack_from(data, (8 + gemUnpacker.size * i))
			gem = Gemstone(unpacked[0], unpacked[1], None)
			self.gemstones.append(gem)

	#def PackLevelData(self):
	#	roomData = self.PackTileData()
	#	gemData = self.PackGemstoneData()
	#
	#	lengthOfRoomData = len(roomData)
	#	lengthOfGemData = len(gemData)
	#
	#	headerPacker = struct.Struct('4sII')
		





#print(len(send_nudes))

icons_path = os.path.dirname(__file__)
if (sys.platform == "darwin"):
	icons_path += "icons/"
else:
	icons_path += "/icons/"