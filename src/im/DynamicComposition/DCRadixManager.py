from .DCCodeInfo import DCCodeInfo
from .DCCodeInfoEncoder import DCCodeInfoEncoder
from ..base.RadixManager import RadixParser
from .Calligraphy import Pane
from .Calligraphy import Stroke
from .Calligraphy import StrokeGroup
import copy

class DCRadixParser(RadixParser):
	TAG_RADIX_SET='字根集'
	TAG_RADIX='字根'
	TAG_STROKE_GROUP='筆劃組'
	TAG_GEOMETRY='幾何'
	TAG_SCOPE='範圍'
	TAG_STROKE='筆劃'
	TAG_NAME='名稱'
	TAG_EXTRA_SCOPE='補充範圍'

	TAG_CODE_INFORMATION='編碼資訊'
	ATTRIB_CODE_EXPRESSION='資訊表示式'

	TAG_CHARACTER_SET='字符集'
	TAG_CHARACTER='字符'

	TAG_NAME='名稱'

	def __init__(self, nameInputMethod, codeInfoEncoder):
		RadixParser.__init__(self, nameInputMethod, codeInfoEncoder)
		self.strokeGroupDB={}

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		strokeGroupNode=elementCodeInfo.find(DCRadixParser.TAG_STROKE_GROUP)
		[strokeGroupName, strokeGroup]=self.parseStrokeGroup(strokeGroupNode)

		codeInfo=self.getEncoder().generateDefaultCodeInfo(strokeGroup)

		extraScopeNode=elementCodeInfo.find(DCRadixParser.TAG_EXTRA_SCOPE)
		if extraScopeNode!=None:
			extraPane=self.parseExtraScope(extraScopeNode)

			codeInfo.setExtraPane(extraPane)
		return codeInfo

	def parseRadixInfo(self, rootNode):
		radixSetNode=rootNode.find(DCRadixParser.TAG_RADIX_SET)
		if radixSetNode is not None:
			radixNodeList=radixSetNode.findall(DCRadixParser.TAG_RADIX)
			for radixNode in radixNodeList:
				radixName=radixNode.get(DCRadixParser.TAG_NAME)
				strokeGroupNodeList=radixNode.findall(DCRadixParser.TAG_STROKE_GROUP)
				for strokeGroupNode in strokeGroupNodeList:
					[strokeGroupName, strokeGroup]=self.parseStrokeGroup(strokeGroupNode)
					self.strokeGroupDB[strokeGroupName]=strokeGroup

		characterSetNode=rootNode.find(DCRadixParser.TAG_CHARACTER_SET)
		characterNodeList=characterSetNode.findall(DCRadixParser.TAG_CHARACTER)
		for characterNode in characterNodeList:
			charName=characterNode.get(DCRadixParser.TAG_NAME)
			radixDescription=self.parseRadixDescription(characterNode)

			self.radixDescriptionManager.addDescription(charName, radixDescription)

	def parseExtraScope(self, extraScopeNode):
		geometryNode=extraScopeNode.find(DCRadixParser.TAG_GEOMETRY)
		pane=self.parseGeometry(geometryNode)
		return pane

	def parseGeometry(self, geometryNode):
		descriptionRegion=geometryNode.get(DCRadixParser.TAG_SCOPE)
		pane=self.parsePane(descriptionRegion)
		return pane

	def parseStrokeGroup(self, strokeGroupNode):
		strokeGroupName=strokeGroupNode.get(DCRadixParser.TAG_NAME)

		geometryNode=strokeGroupNode.find(DCRadixParser.TAG_GEOMETRY)
		pane=self.parseGeometry(geometryNode)

		strokeGroup=self.parseStroke(pane, strokeGroupNode)
		return [strokeGroupName, strokeGroup]

	def parseStroke(self, pane, strokeGroupNode):
		strokeList=[]
		strokeNodeList=strokeGroupNode.findall(DCRadixParser.TAG_STROKE)
		for strokeNode in strokeNodeList:
			description=strokeNode.attrib.get(DCRadixParser.ATTRIB_CODE_EXPRESSION, '')

			descriptionRegion=strokeNode.get(DCRadixParser.TAG_SCOPE)
			countourPane=self.parsePane(descriptionRegion)
			if len(description)>0 and description!='XXXX':
				if description[0]=='(':
					stroke=Stroke(pane, description)

					strokeName=strokeNode.get(DCRadixParser.TAG_NAME, "瑲珩預設筆劃名")
					stroke.setInstanceName(strokeName)

					stroke.transform(countourPane)
					strokeList.append(stroke)
				else:
					strokeGroupName=description
					strokeGroup=self.findStrokeGroup(strokeGroupName)
					tmpStrokeGroup=copy.deepcopy(strokeGroup)
					tmpStrokeGroup.transform(countourPane)
					strokeList.extend(tmpStrokeGroup.getStrokeList())
		strokeGroup=StrokeGroup(pane, strokeList)
		return strokeGroup

	def parsePane(self, descriptionRegion):
		left=int(descriptionRegion[0:2], 16)
		top=int(descriptionRegion[2:4], 16)
		right=int(descriptionRegion[4:6], 16)
		bottom=int(descriptionRegion[6:8], 16)
		return Pane([left, top, right, bottom])

	def findStrokeGroup(self, strokeGroupName):
		return self.strokeGroupDB.get(strokeGroupName)

