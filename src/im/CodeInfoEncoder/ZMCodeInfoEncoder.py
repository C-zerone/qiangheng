from ..CodeInfo.ZMCodeInfo import ZMCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder
from gear import Operator

class ZMCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateDefaultCodeInfo(self, rtlist):
		codeInfo=ZMCodeInfo(None, rtlist, None)
		return codeInfo

	def generateCodeInfo(self, propDict):
		[isSupportCharacterCode, isSupportRadixCode]=CodeInfoEncoder.computeSupportingFromProperty(propDict)
		extra_code=propDict.get('補充資訊')
		str_rtlist=propDict.get('資訊表示式')

		zm_code=''
		zm_extra=extra_code
		zm_single=propDict.get('獨體編碼')
		rtlist=[]
		if str_rtlist!=None:
			rtlist=str_rtlist.split(',')

		codeInfo=ZMCodeInfo(zm_single, rtlist, zm_extra, isSupportCharacterCode, isSupportRadixCode)
		return codeInfo

	def interprettCharacterCode(self, codeInfo):
		singletonCode=codeInfo.getSingletonCode()
		if singletonCode:
			return singletonCode

		rtlist=codeInfo.getRtList()
		codeList=self.convertRadixListToCodeList(rtlist)
		ans=self.computeCharacterCode(codeList)
		extraCode=codeInfo.getExtraCode()
		if extraCode:
			ans+=extraCode
		return ans

	def convertRadixListToCodeList(self, radixList):
		return sum([ZMCodeInfo.radixToCodeDict.get(radix, [radix]) for radix in radixList], [])

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=codeInfoList and all(map(lambda x: x.getZMProp(), codeInfoList))
		return isAllWithCode

	def encodeAsTurtle(self, codeInfoList):
		"""運算 "龜" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """

		rtlist=sum(map(lambda c: c.getZMProp(), codeInfoList), [])

		rtlist=rtlist if len(rtlist)<=4 else rtlist[:2]+rtlist[-2:]
		codeInfo=self.generateDefaultCodeInfo(rtlist)
		return codeInfo

	def encodeAsEast(self, codeInfoList):
		"""運算 "東" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo


	def encodeAsHan(self, codeInfoList):
		"""運算 "爲" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		newCodeInfoList=[secondCodeInfo, firstCodeInfo]
		codeInfo=self.encodeAsLoong(newCodeInfoList)
		return codeInfo


	def encodeAsGoose(self, codeInfoList):
		"""運算 "鴻" """

		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		newCodeInfoList=codeInfoList
		if firstCodeInfo.getRtList()[0]==ZMCodeInfo.RADIX_彳 and lastCodeInfo.getRtList()[0]==ZMCodeInfo.RADIX_亍:
			newCodeInfo=self.generateDefaultCodeInfo([ZMCodeInfo.RADIX_行])
			newCodeInfoList=[newCodeInfo]+codeInfoList[1:-1]
		codeInfo=self.encodeAsLoong(newCodeInfoList)
		return codeInfo


	def encodeAsYou(self, codeInfoList):
		"""運算 "幽" """

		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		newCodeInfoList=[secondCodeInfo, thirdCodeInfo, firstCodeInfo]
		codeInfo=self.encodeAsLoong(newCodeInfoList)
		return codeInfo

	def encodeAsLiang(self, codeInfoList):
		"""運算 "㒳" """

		rtlist=sum(map(lambda c: c.getZMProp(), codeInfoList), [])

		rtlist=rtlist if len(rtlist)<=4 else rtlist[:2]+rtlist[-2:]
		codeInfo=self.generateDefaultCodeInfo(rtlist[:1])
		return codeInfo

	def computeCharacterCode(self, rtlist):
		ans=''
		tmp_rtlist=rtlist
		if len(tmp_rtlist)==0:
			return None
		elif len(tmp_rtlist)==1:
			ans=rtlist[0]
		elif len(tmp_rtlist)==2:
			if len(tmp_rtlist[0])==1 and len(tmp_rtlist[1])==1:
				ans=''.join(rtlist[0:2])
				ans=rtlist[0][0]+rtlist[-1][0]+'vv'
			else:
				ans=(rtlist[0]+rtlist[-1])[:4]
		elif len(tmp_rtlist)==3:
			if len(tmp_rtlist[0])==1:
				ans=rtlist[0][0]+rtlist[1][0]+rtlist[-1][0:2]
			elif len(tmp_rtlist[0])==2:
				ans=rtlist[0][0:2]+rtlist[-2][0]+rtlist[-1][0]
			elif len(tmp_rtlist[0])==3:
				ans=rtlist[0][0:3]+rtlist[-1][0]
			else:
				# 錯誤處理
				ans=rtlist[0][0:4]
		elif len(tmp_rtlist)>=4:
			if len(tmp_rtlist[0])==1:
				ans=rtlist[0][0]+rtlist[1][0]+rtlist[-2][0]+rtlist[-1][0]
			elif len(tmp_rtlist[0])==2:
				ans=rtlist[0][0:2]+rtlist[-2][0]+rtlist[-1][0]
			elif len(tmp_rtlist[0])==3:
				ans=rtlist[0][0:3]+rtlist[-1][0]
			else:
				# 錯誤處理
				ans=rtlist[0][0:4]
		else:
			ans=''
		return ans

