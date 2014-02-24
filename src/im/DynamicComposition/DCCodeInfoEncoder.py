from .DCCodeInfo import DCCodeInfo
from ..base.CodeInfoEncoder import CodeInfoEncoder
from ..base.CodeInfo import CodeInfo
from calligraphy.Calligraphy import Pane
from calligraphy.Calligraphy import StrokeGroup

import sys

class DCCodeInfoEncoder(CodeInfoEncoder):
	@classmethod
	def generateDefaultCodeInfo(cls, strokeGroupDB):
		return DCCodeInfo.generateDefaultCodeInfo(strokeGroupDB)


	@classmethod
	def isAvailableOperation(cls, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getStrokeCount()>0, codeInfoList))
		return isAllWithCode

	@classmethod
	def mergeStrokeGroupListToDB(cls, strokeGroupList):
		resultStrokeList=[]
		for strokeGroup in strokeGroupList:
			resultStrokeList.extend(strokeGroup.getStrokeList())
		pane=Pane.DEFAULT_PANE
		strokeGroup=StrokeGroup(pane, resultStrokeList)
		strokeGroupDB={DCCodeInfo.STROKE_GROUP_NAME_DEFAULT : strokeGroup}
		return strokeGroupDB

	@classmethod
	def extendStrokeGroupNameList(cls, strokeGroupNameList, codeInfoList):
		lenNameList=len(strokeGroupNameList)
		lenCodeInfoList=len(codeInfoList)
		extendingList=[]
		if lenCodeInfoList>lenNameList:
			diff=lenCodeInfoList-lenNameList
			extendingList=[DCCodeInfo.STROKE_GROUP_NAME_DEFAULT for i in range(diff)]
		return strokeGroupNameList+extendingList

	@classmethod
	def splitLengthToList(cls, length, weightList):
		totalWeight=sum(weightList)
		unitLength=length*1./totalWeight

		pointList=[]
		newStrokeGroupList=[]
		base=0
		for weight in weightList:
			pointList.append(int(base))
			base=base+unitLength*weight
		pointList.append(base)
		return pointList

	@classmethod
	def encodeByEmbed(cls, codeInfoList, strokeGroupNameList, paneNameList):
		if len(codeInfoList)<2:
			return cls.encodeAsInvalidate(codeInfoList)

		containerCodeInfo=codeInfoList[0]

		strokeGroupNameList=cls.extendStrokeGroupNameList(strokeGroupNameList, codeInfoList)

		newStrokeGroupList=[]
		paneNameList=[DCCodeInfo.PANE_NAME_DEFAULT]+paneNameList
		for [paneName, strokeGroupName, codeInfo] in zip(paneNameList, strokeGroupNameList, codeInfoList):
			extraPane=containerCodeInfo.getExtraPane(paneName)
			assert extraPane!=None, "extraPane 不應為 None 。%s: %s"%(paneName, str(containerCodeInfo))

			strokeGroup=codeInfo.getCopyOfStrokeGroup(strokeGroupName)
			strokeGroup.transform(extraPane)
			newStrokeGroupList.append(strokeGroup)

		strokeGroupDB=cls.mergeStrokeGroupListToDB(newStrokeGroupList)
		codeInfo=cls.generateDefaultCodeInfo(strokeGroupDB)
		return codeInfo


	@classmethod
	def encodeAsTurtle(cls, codeInfoList):
		"""運算 "龜" """
		print("不合法的運算：龜", file=sys.stderr)
		codeInfo=cls.encodeAsInvalidate(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsLoong(cls, codeInfoList):
		"""運算 "龍" """
		print("不合法的運算：龍", file=sys.stderr)
		codeInfo=cls.encodeAsInvalidate(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsEast(cls, codeInfoList):
		"""運算 "東" """
		print("不合法的運算：東", file=sys.stderr)
		codeInfo=cls.encodeAsInvalidate(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsEqual(cls, codeInfoList):
		"""運算 "爲" """
		firstCodeInfo=codeInfoList[0]
		return firstCodeInfo


	@classmethod
	def encodeAsLoop(cls, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		codeInfo=cls.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_LOOP], [DCCodeInfo.PANE_NAME_LOOP])
		if firstCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.PANE_NAME_QI, firstCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI))
		return codeInfo

	@classmethod
	def encodeAsSilkworm(cls, codeInfoList):
		weightList=list(map(lambda x: x.getStrokeCount()+1, codeInfoList))
		pointList=cls.splitLengthToList(Pane.HEIGHT, weightList)

		strokeGroupNameList=cls.extendStrokeGroupNameList(['蚕'], codeInfoList)

		newStrokeGroupList=[]
		for [pointStart, pointEnd, strokeGroupName, codeInfo] in zip(pointList[:-1], pointList[1:], strokeGroupNameList, codeInfoList):
			pane=Pane([0, pointStart, Pane.X_MAX, pointEnd])

			newStrokeGroup=codeInfo.getCopyOfStrokeGroup(strokeGroupName)
			newStrokeGroup.transform(pane)
			newStrokeGroupList.append(newStrokeGroup)
		strokeGroupDB=cls.mergeStrokeGroupListToDB(newStrokeGroupList)
		codeInfo=cls.generateDefaultCodeInfo(strokeGroupDB)

		lastCodeInfo=codeInfoList[-1]
		if lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.PANE_NAME_QI, lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI))

		return codeInfo

	@classmethod
	def encodeAsGoose(cls, codeInfoList):
		weightList=list(map(lambda x: x.getStrokeCount(), codeInfoList))
		pointList=cls.splitLengthToList(Pane.WIDTH, weightList)

		strokeGroupNameList=cls.extendStrokeGroupNameList(['鴻'], codeInfoList)

		newStrokeGroupList=[]
		for [pointStart, pointEnd, strokeGroupName, codeInfo] in zip(pointList[:-1], pointList[1:], strokeGroupNameList, codeInfoList):
			pane=Pane([pointStart, 0, pointEnd, Pane.Y_MAX])

			newStrokeGroup=codeInfo.getCopyOfStrokeGroup(strokeGroupName)
			newStrokeGroup.transform(pane)
			newStrokeGroupList.append(newStrokeGroup)

		strokeGroupDB=cls.mergeStrokeGroupListToDB(newStrokeGroupList)
		codeInfo=cls.generateDefaultCodeInfo(strokeGroupDB)
		return codeInfo

	@classmethod
	def encodeAsQi(cls, codeInfoList):
		return cls.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_QI], [DCCodeInfo.PANE_NAME_QI])

	@classmethod
	def encodeAsLiao(cls, codeInfoList):
		codeInfo=cls.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_LIAO], [DCCodeInfo.PANE_NAME_LIAO])

		lastCodeInfo=codeInfoList[-1]
		if lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.PANE_NAME_QI, lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI))
		return codeInfo

	@classmethod
	def encodeAsZai(cls, codeInfoList):
		return cls.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_ZAI], [DCCodeInfo.PANE_NAME_ZAI])

	@classmethod
	def encodeAsDou(cls, codeInfoList):
		return cls.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_DOU], [DCCodeInfo.PANE_NAME_DOU])


	@classmethod
	def encodeAsMu(cls, codeInfoList):
		return cls.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_MU], [DCCodeInfo.PANE_NAME_MU_1, DCCodeInfo.PANE_NAME_MU_2])

	@classmethod
	def encodeAsZuo(cls, codeInfoList):
		return cls.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_ZUO], [DCCodeInfo.PANE_NAME_ZUO_1, DCCodeInfo.PANE_NAME_ZUO_2])

	@classmethod
	def encodeAsYou(cls, codeInfoList):
		return cls.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_YOU], [DCCodeInfo.PANE_NAME_YOU_1, DCCodeInfo.PANE_NAME_YOU_2])

	@classmethod
	def encodeAsLiang(cls, codeInfoList):
		return cls.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_LIANG], [DCCodeInfo.PANE_NAME_LIANG_1, DCCodeInfo.PANE_NAME_LIANG_2])

	@classmethod
	def encodeAsJia(cls, codeInfoList):
		return cls.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_JIA], [DCCodeInfo.PANE_NAME_JIA_1, DCCodeInfo.PANE_NAME_JIA_2])

