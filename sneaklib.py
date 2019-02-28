import struct
import binascii
from PyQt5 import QtCore, QtGui, QtWidgets #, QtMacExtras


class SneakObj():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		#Do you want a Z for floors?



class Tile(SneakObj):
	squareBrush = QtGui.QBrush(QtGui.QColor(170,170,170))
	wallPen = QtGui.QPen(QtGui.QColor(240,0,0), 4)
	clearPen = QtGui.QPen(QtGui.QColor(0,0,0,48))
	def __init__(self, x, y, flags = 0):
		super(Tile, self).__init__(x, y)
		self.walls = [(flags & 1) != 0, ((flags>>1) & 1) != 0, ((flags>>2) & 1) != 0, ((flags>>3) & 1) != 0]
	def flags(self):
		flag = 0
		for i in range(len(self.walls)):
			flag |= self.walls[i] << i
		return flag;
	def draw(self, painter, size):
		painter.setBrush(self.squareBrush)
		painter.setPen(self.clearPen)
		dx = self.x*size
		dy = self.y*size
		painter.drawRect(dx, dy, size, size)
		painter.setPen(self.wallPen)
		if self.walls[0]:
			painter.drawLine(dx,		dy,			dx+size-1,	dy)
		if self.walls[1]:
			painter.drawLine(dx+size-1,	dy,			dx+size-1,	dy+size-1)
		if self.walls[2]:
			painter.drawLine(dx+size-1,	dy+size-1,	dx,			dy+size-1)
		if self.walls[3]:
			painter.drawLine(dx,		dy+size-1,	dx,			dy)


class SneakstersLevel:
	#send_nudes = [[200.0, 240.0], [160.0, 240.0], [120.0, 240.0], [120.0, 280.0], [120.0, 320.0], [160.0, 320.0], [200.0, 320.0], [200.0, 360.0], [200.0, 400.0], [160.0, 400.0], [120.0, 400.0], [280.0, 240.0], [280.0, 280.0], [280.0, 320.0], [280.0, 360.0], [280.0, 400.0], [320.0, 400.0], [360.0, 400.0], [320.0, 320.0], [360.0, 320.0], [320.0, 240.0], [360.0, 240.0], [440.0, 240.0], [440.0, 280.0], [440.0, 320.0], [440.0, 360.0], [440.0, 400.0], [480.0, 280.0], [520.0, 320.0], [560.0, 360.0], [560.0, 400.0], [560.0, 320.0], [560.0, 280.0], [560.0, 240.0], [640.0, 240.0], [640.0, 280.0], [640.0, 320.0], [640.0, 360.0], [640.0, 400.0], [680.0, 240.0], [720.0, 280.0], [720.0, 320.0], [720.0, 360.0], [680.0, 400.0], [80.0, 480.0], [80.0, 520.0], [80.0, 560.0], [80.0, 600.0], [80.0, 640.0], [120.0, 520.0], [160.0, 560.0], [200.0, 480.0], [200.0, 520.0], [200.0, 560.0], [200.0, 600.0], [200.0, 640.0], [280.0, 480.0], [280.0, 520.0], [280.0, 560.0], [280.0, 600.0], [280.0, 640.0], [320.0, 640.0], [360.0, 640.0], [360.0, 600.0], [360.0, 560.0], [360.0, 520.0], [360.0, 480.0], [440.0, 480.0], [440.0, 520.0], [440.0, 560.0], [440.0, 600.0], [440.0, 640.0], [480.0, 480.0], [520.0, 520.0], [520.0, 560.0], [520.0, 600.0], [480.0, 640.0], [600.0, 480.0], [600.0, 520.0], [600.0, 560.0], [600.0, 600.0], [600.0, 640.0], [640.0, 640.0], [680.0, 640.0], [640.0, 560.0], [680.0, 560.0], [680.0, 480.0], [640.0, 480.0], [840.0, 480.0], [800.0, 480.0], [760.0, 480.0], [760.0, 520.0], [760.0, 560.0], [800.0, 560.0], [840.0, 560.0], [840.0, 600.0], [840.0, 640.0], [800.0, 640.0], [760.0, 640.0]]
	
	def __init__(self):
		super().__init__()

		self.tiles = []

		#glarp = self.PackTileData(self.send_nudes)
		#print(self.UnpackTileData(glarp))
		
	def TileAt(self, x, y):
		for tile in self.tiles:
			if tile.x == x and tile.y == y:
				return tile

	def AutoWall(self, tile, removing = False):
		tileTop = self.TileAt(tile.x, tile.y-1)
		tileRight = self.TileAt(tile.x+1, tile.y)
		tileBottom = self.TileAt(tile.x, tile.y+1)
		tileLeft = self.TileAt(tile.x-1, tile.y)
		
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


	def draw(self, painter, size):
		for tile in self.tiles:
			tile.draw(painter, size)

	def PackTileData(self, tile_data):
		numberOfTiles = len(tile_data)

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


#print(len(send_nudes))