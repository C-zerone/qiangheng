from injector import inject

from model.BaseCoding import CodeInfoEncoder

class CodeInfoInterpreter:
	@inject
	def __init__(self, codeInfoEncoder: CodeInfoEncoder):
		self.codeInfoEncoder = codeInfoEncoder

	def interpretCodeInfo(self, codeInfo):
		return codeInfo.toCode()

	def encodeToCodeInfo(self, operator, codeInfoList):
		codeInfo=self.codeInfoEncoder.setByComps(operator, codeInfoList)
		return codeInfo

	def interpretCodeInfoList(self, codeInfoList):
		codeList=[]
		for codeInfo in codeInfoList:
			characterCode=self.interpretCodeInfo(codeInfo)
			variance=codeInfo.variance
			if characterCode:
				codeList.append([characterCode, variance])

		return codeList
