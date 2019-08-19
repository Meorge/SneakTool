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
		self.id = -1

	def move(self, x, y):
		self.x+=x
		self.y+=y

	def pack_base(self):
		outputStruct = struct.Struct('HHH')
		return outputStruct.pack(int(self.id), int(self.x), int(self.y))

	def pack(self):
		return self.pack_base() + struct.pack('8x')

class ThiefSpawnPoint(Actor):
	def __init__(self, x, y):
		super().__init__(x, y)

		self.id = 0

	def boundingRect(self):
		return QtCore.QRectF(self.x * size, self.y * size, size, size)

	def draw(self, painter, size, selected = False):
		painter.drawPixmap(self.x * size, self.y * size, size, size, QtGui.QPixmap(icons_path + ("official_sneaksters/thief_ico.png" if selected else "official_sneaksters/thief_ico.png")))


class ExitManhole(Actor):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.id = 1

	def boundingRect(self):
		return QtCore.QRectF(self.x * size, self.y * size, size, size)

	def draw(self, painter, size, selected = False):
		painter.drawPixmap(self.x * size, self.y * size, size, size, QtGui.QPixmap(icons_path + ("official_sneaksters/manhole_ico.png" if selected else "official_sneaksters/manhole_ico.png")))

class Gemstone(Actor):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.id = 3

	def boundingRect(self):
		return QtCore.QRectF(self.x * size, self.y * size, size, size)

	def draw(self, painter, size, selected = False):
		painter.drawPixmap(self.x * size, self.y * size, size, size, QtGui.QPixmap(icons_path + ("official_sneaksters/gem_selected.png" if selected else "official_sneaksters/gem.png")))

class VisibilityBeacon(Actor):
	def __init__(self, x, y, radius=10):
		super().__init__(x, y)
		self.radius = radius
		self.id = 2

	def boundingRect(self):
		return QtCore.QRectF(self.x * size, self.y * size, size, size)

	def draw(self, painter, size, selected = False):
		painter.setBrush(QtGui.QBrush(QtGui.QColor(100,100,200,100)))
		painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))
		painter.drawEllipse((self.x * size) - (size * self.radius / 2) + (size / 2), (self.y * size) - (size * self.radius / 2) + (size / 2), self.radius * size, self.radius * size)
		painter.drawPixmap(self.x * size, self.y * size, size, size, QtGui.QPixmap(icons_path + ("official_sneaksters/beacon_ico.png" if selected else "official_sneaksters/beacon_ico.png")))

	def pack(self):
		# Data:
		# H - radius
		# ? - Inverted
		output = super().pack_base()
		actorData = struct.Struct('H ? 5x')
		return output + actorData.pack(self.radius, False)

class GemSack(Actor):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.id = 4

	def boundingRect(self):
		return QtCore.QRectF(self.x * size, self.y * size, size, size)

	def draw(self, painter, size, selected = False):
		painter.drawPixmap(self.x * size, self.y * size, size, size, QtGui.QPixmap(icons_path + ("official_sneaksters/gem_sack_ico.png" if selected else "official_sneaksters/gem_sack_ico.png")))

class Guard(Actor):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.id = 5

		self.nodes = []

		self.nodeSetID = 0

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
			node = NodeObject(*struct.unpack("2H", data[offset+4*ni : offset+4+4*ni]))
			node.guard = self

			

			print("Raw: {},{}".format(node.x, node.y))
			self.nodes.append(node)

	def draw(self, painter, size, selected = False):
		#print(self.nodes)
		painter.drawPixmap(self.x * size, self.y * size, size, size, QtGui.QPixmap(icons_path + ("official_sneaksters/guard_selected.png" if selected else "official_sneaksters/guard.png")))

	def pack(self):
		# Data:
		# H - Node set ID

		return super().pack_base() + struct.pack("H 6x", int(self.nodeSetID))

	
class NodeObject(Actor):
	def __init__(self, x, y):
		super().__init__(x, y)
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
		fillColor = self.selectedFillColor if selected else self.fillColor
		
		painter.setBrush(QtGui.QBrush(fillColor))
		painter.setPen(QtGui.QPen(QtGui.QColor(0, 170, 0)))

		painter.drawEllipse(self.x * size, self.y * size, size, size)

class NodeSet:
	def __init__(self):
		self.nodes = []

	def addNode(self, node: NodeObject):
		self.nodes.append(node)

	def removeNode(self, node: NodeObject):
		self.nodes.remove(node)

	def pack(self):
		output = b""
		singleNodePacker = struct.Struct("HHH")

		for i in self.nodes:
			output += singleNodePacker.pack(int(i.x), int(i.y), int(0))

		return output


class Tile(SneakObj):
	squareBrush = QtGui.QBrush(QtGui.QColor(170,170,170))
	wallPen = QtGui.QPen(QtGui.QColor(240,0,0), 4)
	doorPen = QtGui.QPen(QtGui.QColor(0,0,240), 6)
	clearPen = QtGui.QPen(QtGui.QColor(0,0,0,48))
	def __init__(self, x, y, flags = 0):
		super(Tile, self).__init__(x, y)

		"""
		Flags stuff
		0000 000X (bit 0, num 1)   - top wall
		0000 00X0 (bit 1, num 2)   - right wall
		0000 0X00 (bit 2, num 4)   - bottom wall
		0000 X000 (bit 3, num 8)   - left wall

		000X 0000 (bit 4, num 16)  - top door
		00X0 0000 (bit 5, num 32)  - right door
		0X00 0000 (bit 6, num 64)  - bottom door
		X000 0000 (bit 7, num 128) - left door
		"""

		self.walls = [(flags & 1) != 0, ((flags>>1) & 1) != 0, ((flags>>2) & 1) != 0, ((flags>>3) & 1) != 0, ((flags>>4) & 1) != 0, ((flags>>5) & 1) != 0, ((flags>>6) & 1), ((flags>>7) & 1)]

	def flags(self):
		flag = 0
		for i in range(len(self.walls)):
			flag |= self.walls[i] << i
		return flag

		
	"""
	Had to get rid of diagonal walls in order to accomodate doors.
	Perhaps one day they can come back :(
	RIP Diagonal Walls, 28 February 2019 - 28 July 2019
	"""
	# def drawDiagnalWalls(self,painter,dx,dy,size, show_disabled):
	# 	if self.walls[4] ^ show_disabled:
	# 		painter.drawLine(dx,		dy,			dx+size-1,	dy+size-1)
	# 	if self.walls[5] ^ show_disabled:
	# 		painter.drawLine(dx,		dy+size-1,	dx+size-1,	dy)

	def draw(self, painter, size, show_diag_walls = False):
		painter.setBrush(self.squareBrush)
		painter.setPen(self.clearPen)
		dx = self.x*size
		dy = self.y*size
		# if self.shape == 0:
		painter.drawRect(dx, dy, size, size)
		# elif self.shape == 1:
		# 	painter.drawPolygon(QtCore.QPoint(dx, dy), QtCore.QPoint(dx+size-1, dy), QtCore.QPoint(dx, dy+size-1))
		# elif self.shape == 2:
		# 	painter.drawPolygon(QtCore.QPoint(dx+size-1, dy), QtCore.QPoint(dx+size-1, dy+size-1), QtCore.QPoint(dx, dy))
		# elif self.shape == 3:
		# 	painter.drawPolygon(QtCore.QPoint(dx+size-1, dy), QtCore.QPoint(dx+size-1, dy+size-1), QtCore.QPoint(dx, dy+size-1))
		# elif self.shape == 4:
		# 	painter.drawPolygon(QtCore.QPoint(dx+size-1, dy+size-1), QtCore.QPoint(dx, dy+size-1), QtCore.QPoint(dx, dy))
		painter.setPen(self.wallPen)

		
		if self.walls[0]:
			painter.drawLine(dx,		dy,			dx+size-1,	dy)
		if self.walls[1]:
			painter.drawLine(dx+size-1,	dy,			dx+size-1,	dy+size-1)
		if self.walls[2]:
			painter.drawLine(dx+size-1,	dy+size-1,	dx,			dy+size-1)
		if self.walls[3]:
			painter.drawLine(dx,		dy+size-1,	dx,			dy)

		painter.setPen(self.doorPen)

		if self.walls[4]:
			painter.drawLine(dx,		dy,			dx+size-1,	dy)
		if self.walls[5]:
			painter.drawLine(dx+size-1,	dy,			dx+size-1,	dy+size-1)
		if self.walls[6]:
			painter.drawLine(dx+size-1,	dy+size-1,	dx,			dy+size-1)
		if self.walls[7]:
			painter.drawLine(dx,		dy+size-1,	dx,			dy)

		# # if show_diag_walls:
		# # 	painter.setPen(self.clearPen)
		# # 	self.drawDiagnalWalls(painter,dx,dy,size, show_diag_walls)
		# painter.setPen(self.diagWallPen)

		# #self.drawDiagnalWalls(painter,dx,dy,size, False)
class SpecialTile(SneakObj):
	squareBrush = QtGui.QBrush(QtGui.QColor(170,0,170))
	wallPen = QtGui.QPen(QtGui.QColor(240,0,0), 4)
	clearPen = QtGui.QPen(QtGui.QColor(0,0,0,48))
	SpecialTileShapes_path = os.path.dirname(__file__) + "/SpecialTileShapes.bin"
	f = open(SpecialTileShapes_path, 'rb');
	shapeData = f.read();
	f.close()
	
	shapes = []
	shapeSeeker = 8
	numShapes = struct.unpack('I', shapeData[4:8])[0]

	for i in range(numShapes):
		numPoints = struct.unpack('I', shapeData[shapeSeeker+4:shapeSeeker+8])[0]
		shapeBytes = shapeData[shapeSeeker:shapeSeeker+numPoints*8+8]
		shape = []
		print(numPoints)
		for j in range(numPoints):
			print(shapeBytes[8+j*8:16+j*8])
			shape.append(struct.unpack('2f', shapeBytes[8+j*8:16+j*8]))
		shapeSeeker += len(shapeBytes)
		
		shapes.append(shape)
	def __init__(self, x, y, flags = 0, shapeType = 0):
		super(SpecialTile, self).__init__(x, y)
		
		"""
		Depending on the complexity of the shape, you can go up to 16 walls.
		"""
		
		self.walls = []
		for i in range(16):
			self.walls.append(((flags>>i) & 1) != 0)
		self.shapeType = shapeType;

	def flags(self):
		flag = 0
		for i in range(len(self.walls)):
			flag |= self.walls[i] << i
		return flag

	def getSize(self):
		return (1,1)
		
	def draw(self, painter, size, show_diag_walls = False):
		painter.setBrush(self.squareBrush)
		painter.setPen(self.clearPen)
		dx = self.x*size
		dy = self.y*size
		shape_to_draw = QtGui.QPolygonF();
		if self.shapeType >= len(self.shapes):
			return
		for point in self.shapes[self.shapeType]:
			shape_to_draw.append(QtCore.QPointF(point[0]*size+dx, point[1]*size+dy))
		painter.drawPolygon(shape_to_draw)
class SneakstersLevel:
	#send_nudes = [[200.0, 240.0], [160.0, 240.0], [120.0, 240.0], [120.0, 280.0], [120.0, 320.0], [160.0, 320.0], [200.0, 320.0], [200.0, 360.0], [200.0, 400.0], [160.0, 400.0], [120.0, 400.0], [280.0, 240.0], [280.0, 280.0], [280.0, 320.0], [280.0, 360.0], [280.0, 400.0], [320.0, 400.0], [360.0, 400.0], [320.0, 320.0], [360.0, 320.0], [320.0, 240.0], [360.0, 240.0], [440.0, 240.0], [440.0, 280.0], [440.0, 320.0], [440.0, 360.0], [440.0, 400.0], [480.0, 280.0], [520.0, 320.0], [560.0, 360.0], [560.0, 400.0], [560.0, 320.0], [560.0, 280.0], [560.0, 240.0], [640.0, 240.0], [640.0, 280.0], [640.0, 320.0], [640.0, 360.0], [640.0, 400.0], [680.0, 240.0], [720.0, 280.0], [720.0, 320.0], [720.0, 360.0], [680.0, 400.0], [80.0, 480.0], [80.0, 520.0], [80.0, 560.0], [80.0, 600.0], [80.0, 640.0], [120.0, 520.0], [160.0, 560.0], [200.0, 480.0], [200.0, 520.0], [200.0, 560.0], [200.0, 600.0], [200.0, 640.0], [280.0, 480.0], [280.0, 520.0], [280.0, 560.0], [280.0, 600.0], [280.0, 640.0], [320.0, 640.0], [360.0, 640.0], [360.0, 600.0], [360.0, 560.0], [360.0, 520.0], [360.0, 480.0], [440.0, 480.0], [440.0, 520.0], [440.0, 560.0], [440.0, 600.0], [440.0, 640.0], [480.0, 480.0], [520.0, 520.0], [520.0, 560.0], [520.0, 600.0], [480.0, 640.0], [600.0, 480.0], [600.0, 520.0], [600.0, 560.0], [600.0, 600.0], [600.0, 640.0], [640.0, 640.0], [680.0, 640.0], [640.0, 560.0], [680.0, 560.0], [680.0, 480.0], [640.0, 480.0], [840.0, 480.0], [800.0, 480.0], [760.0, 480.0], [760.0, 520.0], [760.0, 560.0], [800.0, 560.0], [840.0, 560.0], [840.0, 600.0], [840.0, 640.0], [800.0, 640.0], [760.0, 640.0]]
	
	def __init__(self, spawnX=100, spawnY=100, exitX=100, exitY=101):
		super().__init__()

		self.tiles = []
		self.specialTiles = []
		self.actors = []
		self.nodeSets = []

		self.thiefSpawnPoint = ThiefSpawnPoint(spawnX, spawnY)
		self.exitManhole = ExitManhole(exitX, exitY)


		self.selectedActors = []
		

		#glarp = self.PackTileData(self.send_nudes)
		#print(self.UnpackTileData(glarp))
		
	def TileAt(self, x, y):
		for tile in self.tiles:
			if tile.x == x and tile.y == y:
				return tile
		return None
		
	def SpecialTileAt(self, x, y):
		for tile in self.specialTiles:
			tsize = tile.getSize()
			print(tsize)
			for tx in range(tsize[0]):
				for ty in range(tsize[1]):
					if (tile.x + tx) == x and (tile.y + ty) == y:
						return tile
		return None

	def ObjectAt(self, x, y):
		print("Looking for {},{}".format(x, y))
		obj = self.ActorAt(x,y)
		if obj: return obj

		for i in self.nodeSets:
			for g in i.nodes:
				print("This node is {},{}".format(g.x, g.y))
				if x == g.x and y == g.y:
					return g

		if x == self.thiefSpawnPoint.x and y == self.thiefSpawnPoint.y:
			return self.thiefSpawnPoint

		if x == self.exitManhole.x and y == self.exitManhole.y:
			return self.exitManhole
		
		return None




	def moveSelectedObjects(self, x, y):
		for actor in self.selectedActors:
			actor.move(x,y)


	def ActorAt(self, x, y):
		for i in self.actors:
			if i.x == x and i.y == y:
				return i
		return None

	def NodeAt(self, x, y):
		for i in self.nodeSets:
			for g in i.nodes:
				print("This node is {},{}".format(g.x, g.y))
				if x == g.x and y == g.y:
					return g
		return None


	def AutoWall(self, tile, removing = False):
		tileTop = self.TileAt(tile.x, tile.y-1)
		tileRight = self.TileAt(tile.x+1, tile.y)
		tileBottom = self.TileAt(tile.x, tile.y+1)
		tileLeft = self.TileAt(tile.x-1, tile.y)
		
		# if tileTop:
		# 	if \
		# 		tileTop.shape == 1 or\
		# 		tileTop.shape == 2:
		# 		tileTop = None
		# if tileRight:
		# 	if \
		# 		tileRight.shape == 2 or\
		# 		tileRight.shape == 3:
		# 		tileRight = None
		# if tileBottom:
		# 	if \
		# 		tileBottom.shape == 3 or\
		# 		tileBottom.shape == 4:
		# 		tileBottom = None
		# if tileLeft:
		# 	if \
		# 		tileLeft.shape == 4 or\
		# 		tileLeft.shape == 1:
		# 		tileLeft = None
				

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

		# doors should always overwrite walls
		if tile.walls[4]: tile.walls[0] = False
		if tile.walls[5]: tile.walls[1] = False
		if tile.walls[6]: tile.walls[2] = False
		if tile.walls[7]: tile.walls[3] = False
			
		# if tile.shape == 1:
		# 	tile.walls[1] = False
		# 	tile.walls[2] = False

		# elif tile.shape == 2:
		# 	tile.walls[2] = False
		# 	tile.walls[3] = False

		# elif tile.shape == 3:
		# 	tile.walls[0] = False
		# 	tile.walls[3] = False

		# elif tile.shape == 4:
		# 	tile.walls[0] = False
		# 	tile.walls[1] = False


	def draw(self, painter, size, show_diag_walls = False):
		for tile in self.tiles:
			tile.draw(painter, size, show_diag_walls)
			
		for tile in self.specialTiles:
			tile.draw(painter, size, show_diag_walls)

		for actor in self.actors:
			actor.draw(painter, size, actor in self.selectedActors)

		for nodeSet in self.nodeSets:
			for nodeIndex in range(len(nodeSet.nodes)):
				nodeSet.nodes[nodeIndex].draw(painter, size, nodeSet.nodes[nodeIndex] in self.selectedActors)
				nodeSet.nodes[nodeIndex].drawPath(painter, size, nodeSet.nodes[len(nodeSet.nodes)-1] if nodeIndex == 0 else None, nodeSet.nodes[nodeIndex+1] if nodeIndex < (len(nodeSet.nodes)-1) else nodeSet.nodes[0])

		# Need to separate node sets into their own thing first
		# for guard in self.guards:
		# 	for ni in range(len(guard.nodes)):
		# 		guard.nodes[ni].draw(painter, size, guard.nodes[ni] in self.selectedActors)
		# 		guard.nodes[ni].drawPath(painter, size, guard.nodes[ni].guard if ni == 0 else None, guard.nodes[ni+1] if ni < (len(guard.nodes)-1) else guard.nodes[ni].guard)
		# 	guard.draw(painter, size, guard in self.selectedActors)


		self.thiefSpawnPoint.draw(painter, size, self.thiefSpawnPoint in self.selectedActors)
		self.exitManhole.draw(painter, size, self.exitManhole in self.selectedActors)


	def PackLevelData(self):
		# LEVL header
		# version number
		
		# Tile array offset
		# Tile array data
		
		# Actor array offset
		# Actor array data

		# Nodeset array offset
		# Nodeset array data

		headerPacker = struct.Struct('4s B II II II')

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
		ActorArrayOffset = len(packed) + headerPacker.size
		ActorArrayData = self.PackActorData()

		# add gem data to packing buffer
		packed += ActorArrayData

		# tbh I'm just following what John is doing here
		while ((len(packed) + headerPacker.size) % 0x10) != 0:
			packed += b'\0'

		NodeSetArrayOffset = len(packed) + headerPacker.size
		NodeSetArrayData = self.PackNodeSetData()

		# add gem data to packing buffer
		packed += NodeSetArrayData

		while ((len(packed) + headerPacker.size) % 0x10) != 0:
			packed += b'\0'
		
		headerToPack = (b'LEVL', 2,
			TileArrayOffset, len(TileArrayData), 
			ActorArrayOffset, len(ActorArrayData), 
			NodeSetArrayOffset, len(NodeSetArrayData)
			)
		fileData = headerPacker.pack(*headerToPack)
		print(headerToPack)
		fileData += packed
		return fileData
		

		
	def UnpackLevelData(self, data):
		
		headerUnpacker = struct.Struct('4s B II II II')
		print(data[:headerUnpacker.size])
		header = headerUnpacker.unpack(data[:headerUnpacker.size])


		tileArrayOffset = header[2]
		tileArrayLength = header[3]

		actorArrayOffset = header[4]
		actorArrayLength = header[5]

		nodeSetArrayOffset = header[6]
		nodeSetArrayLength = header[7]

		self.UnpackTileData(data[header[2]:header[2]+header[3]])
		self.UnpackActorData(data[header[4]:header[4]+header[5]])
		self.UnpackNodeSetData(data[header[6]:header[6]+header[7]])

	def PackActorData(self):
		# bam thats it
		output = b''

		actorHeaderPacker = struct.Struct('4sI')
		output += actorHeaderPacker.pack(b"ACTR", len(self.actors) + 2) # adding two for spawn point and exit manhole, which will always be there

		for i in self.actors:
			print("Packing actor of type {} - it is {} bytes".format(type(i), len(i.pack())))
			output += i.pack()

		output += self.thiefSpawnPoint.pack()
		output += self.exitManhole.pack()

		return output

	def UnpackActorData(self, data):
		# yoink
		actorHeaderUnpacker = struct.Struct('4sI')
		header = actorHeaderUnpacker.unpack(data[:actorHeaderUnpacker.size])
		noActors = header[1]

		theGoodStuff = data[actorHeaderUnpacker.size:]

		# the 8s is the flags, it can be anything
		singleActorUnpacker = struct.Struct('H HH 8s')
		for i in range(noActors):
			currentOffset = singleActorUnpacker.size * i

			theData = theGoodStuff[currentOffset:currentOffset + singleActorUnpacker.size]
			print(len(theData))


			#if len(data) != singleActorUnpacker.size: continue
			singleActorUnpackedData = singleActorUnpacker.unpack(theData)

			actor_id = singleActorUnpackedData[0]
			actor_x = singleActorUnpackedData[1]
			actor_y = singleActorUnpackedData[2]
			actor_data = singleActorUnpackedData[3]

			self.CreateActorFromData(actor_id, actor_x, actor_y, actor_data)

	def PackNodeSetData(self):
		nodeSetArrayHeaderPacker = struct.Struct('4s I')
		singleNodePacker = struct.Struct('HHH')

		output = b''
		output += nodeSetArrayHeaderPacker.pack(b"NODE", len(self.nodeSets))

		# next, we need to get the offsets of each node set
		offset = 0
		for i in self.nodeSets:
			output += struct.pack('H', int(offset))
			offset += len(i.nodes) * singleNodePacker.size

		for i in self.nodeSets:
			output += i.pack()

		return output

	def UnpackNodeSetData(self, data):
		return

	def CreateActorFromData(self, id, x, y, data):
		# no switch statements :(

		print("Actor has ID {}".format(id))
		if id == 0:
			# spawn point
			self.thiefSpawnPoint = ThiefSpawnPoint(x, y)
			print("Thief spawn point goes at {},{}".format(x, y))
			return

		elif id == 1:
			# exit point
			self.exitManhole = ExitManhole(x, y)
			print("Manhole goes at {},{}".format(x, y))
			return

		elif id == 2:
			# visibility beacon
			radius, inverted = struct.unpack('H ? 5x', data)
			print("Visibility beacon has radius {}".format(radius))
			newActor = VisibilityBeacon(x, y, radius)

		elif id == 3:
			# gemstone
			newActor = Gemstone(x, y)

		elif id == 4:
			# gem sack
			newActor = GemSack(x, y)

		elif id == 5:
			# guard
			newActor = Guard(x, y)

		else:
			print("Unknown actor")
			return

		if newActor is not None:
			self.actors.append(newActor)
			print("Created actor of type {}".format(type(newActor)))
		return

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

			print(singleGuardHeaderData[3])
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

	def PackSpecialTileData(self):
		numberOfTiles = len(self.specialTiles)
		firstPacker = struct.Struct('4sI')

		data = (b"SPTI", numberOfTiles)
		packed = firstPacker.pack(*data)
		#print(len(packed))



		for tile in self.specialTiles:
			tilePacker = struct.Struct('HHHH')
			#print(tilePacker.size)
			tileData = (int(tile.x), int(tile.y), tile.flags(), int(tile.shapeType))
			packed += tilePacker.pack(*tileData)

		#print(binascii.hexlify(packed))
		return packed

	def UnpackSpecialTileData(self, data):
		headerUnpacker = struct.Struct('4sI')

		self.header = []
		header = headerUnpacker.unpack(data[:8])
		numberOfTiles = header[1]
		for i in range(numberOfTiles):
			tileUnpacker = struct.Struct('HHHH')

			#print(tileUnpacker.size)
			unpacked = tileUnpacker.unpack_from(data, 8 + (tileUnpacker.size * i))
			tile = Tile(unpacked[0], unpacked[1], unpacked[2], unpacked[3])
			self.specialTiles.append(tile)
		#print(header)
		#print(dataOut
		





#print(len(send_nudes))

icons_path = os.path.dirname(__file__) + "/icons/"

# Apparently this isn't necessary here???
# if (sys.platform == "darwin"):
# 	icons_path += "/icons/"
# else:
# 	icons_path += "/icons/"

#print(icons_path + " PLOOPA LOOPA")