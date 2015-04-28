from model.base.CodeInfo import CodeInfo
from model.calligraphy.Calligraphy import Pane
from model.calligraphy.Calligraphy import StrokeGroup

class DCStrokeGroup(StrokeGroup):
	def __init__(self, contourPane, strokeList):
		super().__init__(contourPane, strokeList)
		self.extraPaneDB={DCCodeInfo.PANE_NAME_DEFAULT : Pane.DEFAULT_PANE}

	def setExtraPaneDB(self, extranPaneDB):
		self.extraPaneDB=extranPaneDB
		self.extraPaneDB[DCCodeInfo.PANE_NAME_DEFAULT]=Pane.DEFAULT_PANE

	def setExtraPane(self, paneName, extraPane):
		self.extraPaneDB[paneName]=extraPane

	def getExtraPane(self, paneName):
		return self.extraPaneDB.get(paneName, None)


class DCCodeInfo(CodeInfo):
	PANE_NAME_DEFAULT="瑲珩預設範圍名稱"

	PANE_NAME_LOOP="回"
	PANE_NAME_QI="起"
	PANE_NAME_LIAO="廖"
	PANE_NAME_DAO="斗"
	PANE_NAME_ZAI="載"

	PANE_NAME_MU_1="畞:1"
	PANE_NAME_MU_2="畞:2"

	PANE_NAME_YOU_1="幽:1"
	PANE_NAME_YOU_2="幽:2"

	PANE_NAME_LIANG_1="㒳:1"
	PANE_NAME_LIANG_2="㒳:2"

	PANE_NAME_JIA_1="夾:1"
	PANE_NAME_JIA_2="夾:2"

	PANE_NAME_ZUO_1="㘴:1"
	PANE_NAME_ZUO_2="㘴:2"

	STROKE_GROUP_NAME_DEFAULT="瑲珩預設筆劃組名稱"

	STROKE_GROUP_NAME_LOOP="回"
	STROKE_GROUP_NAME_QI="起"
	STROKE_GROUP_NAME_LIAO="廖"
	STROKE_GROUP_NAME_DAO="斗"
	STROKE_GROUP_NAME_ZAI="載"

	STROKE_GROUP_NAME_MU="畞"
	STROKE_GROUP_NAME_YOU="幽"
	STROKE_GROUP_NAME_LIANG="㒳"
	STROKE_GROUP_NAME_JIA="夾"
	STROKE_GROUP_NAME_ZUO="㘴"

	def __init__(self, strokeGroupDB):
		super().__init__()

		self.strokeGroupDB=strokeGroupDB

	@staticmethod
	def generateDefaultCodeInfo(strokeGroupDB):
		codeInfo=DCCodeInfo(strokeGroupDB)
		return codeInfo

	def toCode(self):
		strokeList=self.getStrokeGroup().getStrokeList()
		codeList=[self.encodeStroke(stroke) for stroke in strokeList]
		return ';'.join(codeList)

	def encodeStroke(self, stroke):
		def encodePoints(points):
			point = points[0]
			isCurve = point[0]
			assert isCurve is False
			pointExpressionList = ["0000{0[0]:02X}{0[1]:02X}".format(point[1]), ]

			for point in points[1:]:
				isCurve = point[0]
				if isCurve:
					pointExpressionList.append("0002{0[0]:02X}{0[1]:02X}".format(point[1]))
				else:
					pointExpressionList.append("0001{0[0]:02X}{0[1]:02X}".format(point[1]))
			return ",".join(pointExpressionList)

		def toValid(point):
			x, y = point
			newX = max(0, min(0xFF, x))
			newY = max(0, min(0xFF, y))
			return (newX, newY)

		points=stroke.getPoints()
		newPoints = [(isCurve, toValid(point)) for (isCurve, point) in points]
		return encodePoints(newPoints)

	def setExtraPane(self, strokeGroupName, paneName, extraPane):
		strokeGroup=self.getStrokeGroup(strokeGroupName)

		if strokeGroup==None:
			strokeGroup=self.getStrokeGroup()

		strokeGroup.setExtraPane(paneName, extraPane)

	def getExtraPane(self, strokeGroupName, paneName):
		strokeGroup=self.getStrokeGroup(strokeGroupName)

		if strokeGroup==None:
			strokeGroup=self.getStrokeGroup()

		return strokeGroup.getExtraPane(paneName)

	def getStrokeGroup(self, strokeGroupName=STROKE_GROUP_NAME_DEFAULT):
		return self.strokeGroupDB.get(strokeGroupName)

	def getCopyOfStrokeGroup(self, strokeGroupName=STROKE_GROUP_NAME_DEFAULT):
		strokeGroup=self.getStrokeGroup(strokeGroupName)
		if strokeGroupName!=DCCodeInfo.STROKE_GROUP_NAME_DEFAULT and strokeGroup==None:
			strokeGroup=self.getStrokeGroup(DCCodeInfo.STROKE_GROUP_NAME_DEFAULT)
		return strokeGroup.clone()

	def getStrokeCount(self):
		return self.getStrokeGroup().getCount()

	def transform(self, pane):
		self.getStrokeGroup().transform(pane)
