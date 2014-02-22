import sys
import copy

from ..CodeInfo.BSCodeInfo import BSCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class BSCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict):
		[isSupportCharacterCode, isSupportRadixCode]=CodeInfoEncoder.computeSupportingFromProperty(propDict)
		_bs_single=propDict.get('獨體編碼')
		str_incode=propDict.get('資訊表示式')
		str_spcode=propDict.get('嘸蝦米補碼')
		_code_list=None
		if str_incode!=None and str_spcode!=None:
			_code_list=str_incode.split(',')

		codeInfo=BSCodeInfo(_bs_single, _code_list, str_spcode, isSupportCharacterCode, isSupportRadixCode)
		return codeInfo

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getBSProp()[0], codeInfoList))
		return isAllWithCode

	def encodeAsTurtle(self, codeInfoList):
		"""運算 "龜" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """

		bslist=list(map(lambda c: c.getBSProp()[0], codeInfoList))
		bs_code_list=BSCodeInfoEncoder.computeBoshiamyCode(bslist)
		bs_spcode=codeInfoList[-1].getBSProp()[1]

		codeInfo=self.generateDefaultCodeInfo()
		codeInfo.setBSProp(bs_code_list, bs_spcode)
		return codeInfo

	def encodeAsEast(self, codeInfoList):
		"""運算 "東" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsSilkworm(self, codeInfoList):
		"""運算 "蚕" """
		bsCodeList=list(map(lambda c: c.getBSProp()[0], codeInfoList))
		tmpBsCodeList=BSCodeInfoEncoder.mergeRadixAsSilkworm(bsCodeList)

		bs_code_list=BSCodeInfoEncoder.computeBoshiamyCode(tmpBsCodeList)
		bs_spcode=codeInfoList[-1].getBSProp()[1]

		codeInfo=self.generateDefaultCodeInfo()
		codeInfo.setBSProp(bs_code_list, bs_spcode)
		return codeInfo

	def encodeAsGoose(self, codeInfoList):
		"""運算 "蚕" """
		bsCodeList=list(map(lambda c: c.getBSProp()[0], codeInfoList))
		tmpBsCodeList=BSCodeInfoEncoder.mergeRadixAsGoose(bsCodeList)

		bs_code_list=BSCodeInfoEncoder.computeBoshiamyCode(tmpBsCodeList)
		bs_spcode=codeInfoList[-1].getBSProp()[1]

		codeInfo=self.generateDefaultCodeInfo()
		codeInfo.setBSProp(bs_code_list, bs_spcode)
		return codeInfo

	def encodeAsHan(self, codeInfoList):
		"""運算 "函" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		newCodeInfoList=[secondCodeInfo, firstCodeInfo]
		codeInfo=self.encodeAsLoong(newCodeInfoList)
		return codeInfo


	def encodeAsZhe(self, codeInfoList):
		"""運算 "這" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		codeInfo=self.encodeAsLoong([secondCodeInfo, firstCodeInfo])
		return codeInfo

	def encodeAsYou(self, codeInfoList):
		"""運算 "幽" """

		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		newCodeInfoList=[secondCodeInfo, thirdCodeInfo, firstCodeInfo]
		codeInfo=self.encodeAsLoong(newCodeInfoList)
		return codeInfo

	@staticmethod
	def computeBoshiamyCode(bsCodeList):
		bslist=list(sum(bsCodeList, []))
		bs_code_list=(bslist[:3]+bslist[-1:]) if len(bslist)>4 else bslist
		return bs_code_list

	@staticmethod
	def mergeRadixAsSilkworm(bsCodeList):
		tmpBsCodeList=copy.copy(bsCodeList)

		numBsCode=len(tmpBsCodeList)
		for i in range(numBsCode-1):
			bsCodePrev=tmpBsCodeList[i]
			bsCodeNext=tmpBsCodeList[i+1]
			if len(bsCodePrev)>0 and len(bsCodeNext)>0:
				if bsCodePrev[-1]==BSCodeInfo.RADIX_E2 and bsCodeNext[0]==BSCodeInfo.RADIX_E1:
					tmpBsCodeList[i]=bsCodePrev[:-1]+[BSCodeInfo.RADIX_E2_E1]
					tmpBsCodeList[i+1]=bsCodeNext[1:]

		# 合併字根後，有些字根列可能為空，如：戓
		tmpBsCodeList=filter(lambda x: len(x)>0, tmpBsCodeList)

		return tmpBsCodeList

	@staticmethod
	def mergeRadixAsGoose(bsCodeList):
		tmpBsCodeList=copy.copy(bsCodeList)

		numBsCode=len(tmpBsCodeList)
		for i in range(numBsCode-1):
			bsCodePrev=tmpBsCodeList[i]
			bsCodeNext=tmpBsCodeList[i+1]
			if len(bsCodePrev)>0 and len(bsCodeNext)>0:
				if bsCodePrev[0]==BSCodeInfo.RADIX_M1 and bsCodeNext[0]==BSCodeInfo.RADIX_E2_E1:
					tmpBsCodeList[i]=[BSCodeInfo.RADIX_M1_E2_E1]+bsCodePrev[1:]
					tmpBsCodeList[i+1]=bsCodeNext[1:]

		# 合併字根後，有些字根列可能為空，如：戓
		tmpBsCodeList=filter(lambda x: len(x)>0, tmpBsCodeList)

		return tmpBsCodeList

