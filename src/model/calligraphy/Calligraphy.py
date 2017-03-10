from xie.graphics.shape import Pane
from xie.graphics.shape import Drawing


class StrokeGroupInfo:
	def __init__(self, strokeList, bBoxPane):
		self.strokeList=strokeList
		self.bBoxPane=bBoxPane

	def getStrokeList(self):
		return self.strokeList

	def getBBoxPane(self):
		return self.bBoxPane

class StrokeGroup(Drawing):
	def __init__(self, strokeGroupInfo):
		pane=strokeGroupInfo.getBBoxPane()
		super().__init__(pane)
		self.strokeGroupInfo=strokeGroupInfo

	def clone(self):
		strokeList=[s.clone() for s in self.getStrokeList()]
		strokeGroupInfo=StrokeGroupInfo(strokeList, self.getInfoPane())
		strokeGroup=StrokeGroup(strokeGroupInfo)
		strokeGroup.setStatePane(self.getStatePane())
		return strokeGroup

	def getDrawingList(self):
		return self.getStrokeList()

	def getStrokeList(self):
		return self.strokeGroupInfo.getStrokeList()

	def getCount(self):
		return len(self.getStrokeList())

	@staticmethod
	def generateStrokeGroup(sg, pane):
		strokeGroup=sg.clone()

		newSgTargetPane=pane
		sgTargetPane=strokeGroup.getStatePane()
		sgInfoPane=strokeGroup.getInfoPane()
		for drawing in strokeGroup.getDrawingList():
			sTargetPane=drawing.getStatePane()
			sInfoPane=drawing.getInfoPane()
			drawing.transformBy(sgInfoPane, newSgTargetPane)

		strokeGroup.setStatePane(newSgTargetPane)
		strokeGroup.setInfoPane(newSgTargetPane)

		return strokeGroup

	@staticmethod
	def generateStrokeGroupInfo(strokeGroupPanePair):
		def computeBBox(paneList):
			left=min(map(lambda pane: pane.getLeft(), paneList))
			top=min(map(lambda pane: pane.getTop(), paneList))
			right=max(map(lambda pane: pane.getRight(), paneList))
			bottom=max(map(lambda pane: pane.getBottom(), paneList))
			return Pane(left, top, right, bottom)

		resultStrokeList=[]
		paneList=[]
		for strokeGroup, pane in strokeGroupPanePair:
			strokeGroup=StrokeGroup.generateStrokeGroup(strokeGroup, pane)
			resultStrokeList.extend(strokeGroup.getStrokeList())
			paneList.append(strokeGroup.getInfoPane())

		pane=computeBBox(paneList)
		strokeGroupInfo=StrokeGroupInfo(resultStrokeList, pane)

		return strokeGroupInfo

