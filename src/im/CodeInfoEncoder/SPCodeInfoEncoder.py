from ..CodeInfo.SPCodeInfo import SPCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class SPCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=SPCodeInfo(propDict, codeVariance)
		return codeInfo

	def isAvailableOperation(self, operator, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getCharacterCode(), codeInfoList))
		return isAllWithCode

	def encodeAsTurtle(self, codeInfo, operator, codeInfoList):
		"""運算 "龜" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsLoong(self, codeInfo, operator, codeInfoList):
		"""運算 "龍" """

		codeInfo.setCharacterCode('YYYY')

	def encodeAsEast(self, codeInfo, operator, codeInfoList):
		"""運算 "東" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsEqual(self, codeInfo, operator, codeInfoList):
		"""運算 "爲" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

