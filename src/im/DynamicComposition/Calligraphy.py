import re
import sys

class StrokeAction:
	ACTION_START="0000"
	ACTION_END="0001"
	ACTION_CURVE="0002"

	ActionStrToNumDict={
		ACTION_START : 0,
		ACTION_END : 1,
		ACTION_CURVE : 2,
	}

	ActionNumToStrDict={
		0: ACTION_START,
		1: ACTION_END,
		2: ACTION_CURVE,
	}

	def __init__(self, action, point):
		self.action=action
		self.point=point

	@staticmethod
	def fromDescription(description):
		actionStr=description[0:4]
		action=StrokeAction.ActionStrToNumDict[actionStr]
		x=int(description[4:6], 16)
		y=int(description[6:8], 16)
		point=(x, y)
		return StrokeAction(action, point)

	def getCode(self, pane):
		(x, y)=pane.transformPoint(self.point)
		code="%02X%02X"%(x, y)
		return StrokeAction.ActionNumToStrDict[self.action]+code

class Pane:
	WIDTH=0x100
	HEIGHT=0x100
	X_MAX=0xFF
	Y_MAX=0xFF

	DEFAULT_REGION=[0, 0, X_MAX, Y_MAX]

	def __init__(self, region=DEFAULT_REGION):
		[left, top, right, bottom]=region
		self.left=left
		self.top=top
		self.right=right
		self.bottom=bottom

		self.name="預設範圍"

		self.setup()

	def clone(self):
		return Pane(self.getAsList())

	def setup(self):
		self.hScale=self.width*1./Pane.WIDTH
		self.vScale=self.height*1./Pane.HEIGHT

	@property
	def width(self):
		return self.right-self.left+1

	@property
	def height(self):
		return self.bottom-self.top+1

	def setName(self, name):
		self.name=name

	def getName(self):
		return self.name

	def getAsList(self):
		return [self.left, self.top, self.right, self.bottom]

	def getLeft(self):
		return self.left

	def getTop(self):
		return self.top

	def getRight(self):
		return self.right

	def getBottom(self):
		return self.bottom

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height

	def getHScale(self):
		return self.hScale

	def getVScale(self):
		return self.vScale

	def transformPoint(self, point):
		[x, y]=point
		left=self.getLeft()
		top=self.getTop()

		hScale=self.getHScale()
		vScale=self.getVScale()

		newX=int(x*hScale)+left
		newY=int(y*vScale)+top

		return (newX, newY)

	def transformPane(self, pane):
		(left, top)=self.transformPoint((pane.left, pane.top))
		(right, bottom)=self.transformPoint((pane.right, pane.bottom))

		pane.left=left
		pane.top=top
		pane.right=right
		pane.bottom=bottom

		pane.setup()

Pane.DEFAULT_PANE=Pane()

class Writing:
	def __init__(self, contourPane):
		self.boundaryPane=Pane.DEFAULT_PANE
		self.contourPane=contourPane

	def getBoundaryPane(self):
		return self.boundaryPane

	def getContourPane(self):
		return self.contourPane

	# 多型
	def transform(self, pane):
		pass

class Stroke(Writing):
	STROKE_NAMES=[
#		"XXXX",

		"點", "長頓點",

		"橫", "橫鉤", "橫折", "橫折橫",
		"橫折鉤", "橫撇", "橫曲鉤",
		"橫撇橫折鉤", "橫斜鉤",
		"橫折橫折",

		"豎", "豎折", "豎挑", "豎橫折",
		"豎橫折鉤", "豎曲鉤", "豎鉤",
		"臥鉤", "斜鉤", "彎鉤",

		"撇", "撇頓點", "撇橫", "撇挑",
		"撇折", "豎撇", "挑", "挑折",
		"捺",

		"挑捺",	# 例子：乀
		"橫捺",	# 例子：乁
		"圓",	# 例子：㔔
	]

	DEFAULT_INSTANCE_NAME='瑲珩預設筆劃名'

	def __init__(self, contourPane, strokeName, actionList):
		super().__init__(contourPane)

		assert (strokeName in Stroke.STROKE_NAMES), "不認得的筆畫名稱: %s"%strokeName

		self.setInstanceName(Stroke.DEFAULT_INSTANCE_NAME)

		self.typeName=strokeName

		self.actionList=actionList

	def clone(self):
		return Stroke(self.contourPane.clone(), self.typeName, self.actionList)

	def getInstanceName(self):
		return self.name

	def setInstanceName(self, name):
		self.name=name

	def getTypeName(self):
		return self.typeName

	def getCode(self):
		codeList=[action.getCode(self.contourPane) for action in self.actionList]
		return ','.join(codeList)

	# 多型
	def transform(self, pane):
		pane.transformPane(self.contourPane)

class StrokeGroup(Writing):
	def __init__(self, contourPane, strokeList):
		super().__init__(contourPane)

		self.strokeList=strokeList

	def clone(self):
		strokeList=[s.clone() for s in self.strokeList]
		return StrokeGroup(self.contourPane, strokeList)

	def getStrokeList(self):
		return self.strokeList

	def getCount(self):
		return len(self.strokeList)

	def getCode(self):
		strokeList=self.getStrokeList()
		codeList=[stroke.getCode() for stroke in strokeList]
		return ','.join(codeList)

	# 多型
	def transform(self, pane):
		for stroke in self.strokeList:
			stroke.transform(pane)

