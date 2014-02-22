from .CharInfo import CharInfo

class CJCharInfo(CharInfo):
	def __init__(self, propDict={}):
		super().__init__(propDict)

		self.setFlag=False

		self._cj_direction=None	# 組件的方向
		self._cj_single=None	# 當此字為獨體時的碼。
		self._cj_body=None	# 當此字為字身時的碼。
		self._cj_radix_list=[]	# 組件

		self._cj_single=propDict.get('獨體編碼')
		str_rtlist=propDict.get('資訊表示式')
		if str_rtlist!=None:
			self.setCJProp(str_rtlist)

	def setCJProp(self, cj_info_code):
		dir_code='*'
		radix_list=[]

		codeList=cj_info_code.split('=')

		if len(codeList)>0:
			x_code=codeList[0]
			if len(x_code)>0:
				dir_code=x_code[0]
				if dir_code not in ['|', '-', '*', '@']:
					dir_code='*'

				radix_list=x_code[1:].split(',')

		self._cj_radix_list=radix_list
		self._cj_direction=dir_code
		self._cj_body=self.computeBodyCode(self._cj_radix_list, dir_code)

		self.setFlag=True

	def getCJProp(self):
		return [self._cj_direction, self._cj_radix_list]

	def setByComps(self, operator, complist):
		# 計算倉頡碼時，需要知道此字的組成方向
		direction=operator.getDirection()

		ansRadixList=[]
		for tmpchinfo in complist:
			tmpDirCode, tmpRadixList=tmpchinfo.getCJProp()
#			if tmpDirCode=='*':
			if tmpDirCode in ['*', '@']:
				ansRadixList.append(tmpchinfo._cj_body)
			elif tmpDirCode==direction:
				# 同向
				ansRadixList.extend(tmpRadixList)
			else:
				# 不同向
				ansRadixList.append(tmpchinfo._cj_body)

		self.setCJProp(direction+','.join(ansRadixList))

	@property
	def cj(self):
		if self._cj_single:
			return self._cj_single
		else:
			return CJCharInfo.computeTotalCode(self._cj_radix_list, self._cj_direction).lower()

	def getCode(self):
		if self.cj: return self.cj

	@staticmethod
	def computeHeadTailCode(code, headCount):
		frontCode=code[:headCount]
		rearCode=code[headCount:]

		# 以大寫來表示重要的尾碼
		xTailCode=list(filter(lambda x: x.isupper(), rearCode))
		if len(xTailCode)>0:
			# 重要的尾碼
			tailCode=xTailCode[-1]
		elif len(rearCode)>0:
			tailCode=rearCode[-1]
		else:
			tailCode=''

		return frontCode+tailCode

	@staticmethod
	def computeHeadCode(code):
		headCode=CJCharInfo.computeHeadTailCode(code, 1)
		return headCode

	@staticmethod
	def computeBodyCode(codeList, direction='*'):
		def convertAllToHeadTail(l):
			pass

		bodyCode=''
		if len(codeList)==0:
			bodyCode=''
		elif len(codeList)==1:
			bodyCode=CJCharInfo.computeHeadTailCode(codeList[0], 2)
		else:
			tmpCodeList=codeList

			# 調整特徵碼
			if direction=='@':
				tmpCodeList=codeList[:1]+[CJCharInfo.computeHeadCode(x).lower() for x in codeList[1:]]
			else:
				tmpCodeList=[CJCharInfo.computeHeadCode(x).lower() for x in codeList[:-1]]+codeList[-1:]

			tmpHeadCode=CJCharInfo.computeHeadCode(tmpCodeList[0])
			tmpCodeList=tmpCodeList[1:]

			if len(tmpHeadCode)==2:
				if len(tmpCodeList)>0:
					tmpBodyCode=CJCharInfo.computeHeadTailCode(tmpCodeList[-1], 0)
				else:
					tmpBodyCode=''
			elif len(tmpHeadCode)==1:
				tmpHeadCode2=CJCharInfo.computeHeadCode(tmpCodeList[0])
				tmpCodeList=tmpCodeList[1:]

				if len(tmpCodeList)>0:
					tmpBodyCode2=CJCharInfo.computeHeadTailCode(tmpCodeList[-1], 0)
				else:
					tmpBodyCode2=''
				tmpBodyCode=CJCharInfo.computeHeadTailCode(tmpHeadCode2+tmpBodyCode2, 1)
			else:
				# 理論上錯誤
				tmpBodyCode=''
			bodyCode=tmpHeadCode+tmpBodyCode
		return bodyCode

	@staticmethod
	def computeTotalCode(codeList, direction='*'):
		if len(codeList)==1:
			totalCode=CJCharInfo.computeHeadTailCode(codeList[0], 3)
		elif len(codeList)>1:
			totalCode=CJCharInfo.computeHeadCode(codeList[0])+CJCharInfo.computeBodyCode(codeList[1:], direction)
		else:
			totalCode=''
		return totalCode

