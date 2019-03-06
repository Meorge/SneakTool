import struct
import os, sys
import binascii
from math import atan2, sin, cos
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
	def move(self, x, y):
		self.x+=x
		self.y+=y


class Gemstone(Actor):
	def __init__(self, x, y):
		super().__init__(x, y)

	def boundingRect(self):
		return QtCore.QRectF(self.x * size, self.y * size, size, size)

	def draw(self, painter, size, selected = False):
		#print(size)
		#painter.setBrush(QtGui.QBrush(QtGui.QColor(200,200,200)))
		#painter.drawRect(self.x * size, self.y * size, size, size)
		painter.drawPixmap(self.x * size, self.y * size, size, size, QtGui.QPixmap(icons_path + ("official_sneaksters/gem_selected.png" if selected else "official_sneaksters/gem.png")))

class Guard(Actor):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.nodes = []

	def AddNode(self, node):
		node.guard = self
		self.nodes.append(node)

	def RemoveNode(self, node):
		self.nodes.remove(node)

	def boundingRect(self):
		return (QtCore.QRectF(self.x * size, self.y * size, size, size))
	
	def packNodeData(self):
		packed = b''
		for ni in range(len(self.nodes)): #I know we could just iterate directly, but I identify by id just to make sure we're in order.
			packed += struct.pack("2H", int(self.nodes[ni].x), int(self.nodes[ni].y))
		return packed

	def unpackNodeData(self, data, noNodes, offset):
		for ni in range(noNodes): #I know we could just iterate directly, but I identify by id just to make sure we're in order.
			node = GuardNode(*struct.unpack("2H", data[offset+4*ni : offset+4+4*ni]))
			node.guard = self
			self.nodes.append(node)

	def draw(self, painter, size, selected = False):
		#print(self.nodes)
		painter.drawPixmap(self.x * size, self.y * size, size, size, QtGui.QPixmap(icons_path + ("official_sneaksters/guard_selected.png" if selected else "official_sneaksters/guard.png")))

	
class GuardNode(Actor):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.guard = None
		self.fillColor = QtGui.QColor(0, 150, 0)
		self.selectedFillColor = QtGui.QColor(0, 200, 0)

	def __seriouslyDrawPath(self, painter, size, x1, y1, x2, y2):
		painter.setBrush(QtGui.QBrush(self.fillColor))
		painter.setPen(QtGui.QPen(QtGui.QColor(0, 170, 0), 4))
		fx1 = x1 * size + size/2
		fy1 = y1 * size + size/2
		fx2 = x2 * size + size/2
		fy2 = y2 * size + size/2
		painter.drawLine(fx1, fy1, fx2, fy2)

		painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 0))
		
		ax = (fx1 + fx2)/2
		ay = (fy1 + fy2)/2

		angle = atan2(fx2-fx1, fy2-fy1)

		print(angle)

		s = sin(angle)
		c = cos(angle)

		painter.drawPolygon(QtCore.QPoint(ax + 6 * s - 12 * c, ay + 6 * c + 12 * s),
							QtCore.QPoint(ax - 6 * s, ay - 6 * c),
							QtCore.QPoint(ax + 6 * s + 12 * c, ay + 6 * c - 12 * s))

	def drawPath(self, painter, size, previousActor, nextActor):
		if previousActor is not None:
			self.__seriouslyDrawPath(painter, size, previousActor.x, previousActor.y, self.x, self.y)
		if nextActor is not None:
			self.__seriouslyDrawPath(painter, size, self.x, self.y, nextActor.x, nextActor.y)

	def draw(self, painter, size, selected = False):
		print("painting a node")
		fillColor = self.selectedFillColor if selected else self.fillColor
		
		painter.setBrush(QtGui.QBrush(fillColor))
		painter.setPen(QtGui.QPen(QtGui.QColor(0, 170, 0)))

		#painter.drawRect(self.x * size, self.y * size, size, size)
		painter.drawEllipse(self.x * size, self.y * size, size, size)


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
		self.guards = []


		self.selectedActors = []
		

		#glarp = self.PackTileData(self.send_nudes)
		#print(self.UnpackTileData(glarp))
		
	def TileAt(self, x, y):
		for tile in self.tiles:
			if tile.x == x and tile.y == y:
				return tile
		return None

	def ObjectAt(self, x, y):
		obj = self.GemstoneAt(x,y)
		if obj:return obj

		obj = self.GuardAt(x,y)
		if obj:return obj

		obj = self.GuardNodeAt(x,y)
		if obj:return obj
		return None


	def moveSelectedObjects(self, x, y):
		for actor in self.selectedActors:
			actor.move(x,y)

	def GemstoneAt(self, x, y):
		for gem in self.gemstones:
			if gem.x == x and gem.y == y:
				return gem
		return None

	def GuardAt(self, x, y):
		for guard in self.guards:
			if guard.x == x and guard.y == y:
				return guard
		return None

	def GuardNodeAt(self, x, y):
		for guard in self.guards:
			for node in guard.nodes:
				if node.x == x and node.y == y:
					return node
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
			gem.draw(painter, size, gem in self.selectedActors)

		for guard in self.guards:
			for ni in range(len(guard.nodes)):
				guard.nodes[ni].draw(painter, size, guard.nodes[ni] in self.selectedActors)
				guard.nodes[ni].drawPath(painter, size, guard.nodes[ni].guard if ni == 0 else None, guard.nodes[ni+1] if ni < (len(guard.nodes)-1) else guard.nodes[ni].guard)
			guard.draw(painter, size, guard in self.selectedActors)


	def PackLevelData(self):
		headerPacker = struct.Struct('4sIIIIII')

		# start the packing buffer
		packed = b''


		while ((len(packed) + headerPacker.size) % 0x10)!=0:
			packed+=b'\0'

		# calculate offset for tile section
		TileArrayOffset = len(packed) + headerPacker.size
		TileArrayData = self.PackTileData()

		# add the tile data to the packing buffer
		packed += TileArrayData
		
		# some null buffer I think?
		#  -	For file alignment, yes.
		while ((len(packed) + headerPacker.size) % 0x10)!=0:
			packed+=b'\0'

		# calculate offset and data for gemstone section
		GemstoneArrayOffset = len(packed) + headerPacker.size
		GemstoneArrayData = self.PackGemstoneData()

		# add gem data to packing buffer
		packed += GemstoneArrayData

		# tbh I'm just following what John is doing here
		while ((len(packed) + headerPacker.size) % 0x10) != 0:
			packed += b'\0'

		GuardArrayOffset = len(packed) + headerPacker.size
		GuardArrayData = self.PackGuardData()

		# add gem data to packing buffer
		packed += GuardArrayData


		return headerPacker.pack(b'LEVL', TileArrayOffset, len(TileArrayData), GemstoneArrayOffset, len(GemstoneArrayData), GuardArrayOffset, len(GuardArrayData)) + packed
		
	def UnpackLevelData(self, data):
		headerUnpacker = struct.Struct('4sIIIIII')
		header = headerUnpacker.unpack(data[:headerUnpacker.size])
		self.UnpackTileData(data[header[1]:header[1]+header[2]])
		self.UnpackGemstoneData(data[header[3]:header[3]+header[4]])
		self.UnpackGuardData(data[header[5]:header[5]+header[6]])


	def PackGuardData(self):
		noGuards = len(self.guards)
		guardHeader = struct.Struct('4sI')
		guardHeaderData = (b"PTRL", noGuards)

		packed = guardHeader.pack(*guardHeaderData)
		nodeData = b''
		singleGuardHeaderPacker = struct.Struct('HH H i')
		for guard in self.guards:
			singleGuardHeaderData = (int(guard.x), int(guard.y), len(guard.nodes), singleGuardHeaderPacker.size * noGuards + guardHeader.size + len(nodeData))
			nodeData += guard.packNodeData()
			packed += singleGuardHeaderPacker.pack(*singleGuardHeaderData)
		packed += nodeData
		return packed

	def UnpackGuardData(self, data):
		guardHeader = struct.Struct('4sI')
		header = guardHeader.unpack(data[:guardHeader.size])
		noGuards = header[1]
		
		singleGuardHeaderUnpacker = struct.Struct('HH H i')
		for gi in range(noGuards):
			singleGuardHeaderData = singleGuardHeaderUnpacker.unpack(data[guardHeader.size + singleGuardHeaderUnpacker.size * gi: guardHeader.size + singleGuardHeaderUnpacker.size +  singleGuardHeaderUnpacker.size * gi])
			guard = Guard(singleGuardHeaderData[0], singleGuardHeaderData[1])
			guard.unpackNodeData(data, singleGuardHeaderData[2], singleGuardHeaderData[3])
			self.guards.append(guard)

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
			gem = Gemstone(unpacked[0], unpacked[1])
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

icons_path = os.path.dirname(__file__) + "/icons/"

# Apparently this isn't necessary here???
# if (sys.platform == "darwin"):
# 	icons_path += "/icons/"
# else:
# 	icons_path += "/icons/"

print(icons_path + " PLOOPA LOOPA")