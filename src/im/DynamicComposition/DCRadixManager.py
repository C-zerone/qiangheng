from .DCCodeInfo import DCCodeInfo
from .DCCodeInfoEncoder import DCCodeInfoEncoder
from ..base.RadixManager import RadixManager
from .Stroke import Stroke
import Constant

class DCRadixManager(RadixManager):
	def __init__(self):
		RadixManager.__init__(self)

	def createEncoder(self):
		return DCCodeInfoEncoder()

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)

		self.setCodeInfoAttribute(codeInfo, radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getElement()

		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo.attrib

		strokeList=[]
		description=infoDict.get('資訊表示式', '')
		if len(description)>0 and description!='XXXX':
			strokeDescriptionList=description.split(DCCodeInfo.STROKE_SEPERATOR)
			strokeList=[]
			for d in strokeDescriptionList:
				stroke=Stroke(d)
				strokeList.append(stroke)

		codeInfo=DCCodeInfo(strokeList)
		return codeInfo

