import sys
import Constant
import yaml

from coding.Base import CodingRadixParser

from model.element.enum import FontVariance

from model.element.SubstituteRule import SubstituteRule
from model.element.CharacterDescription import CharacterDescription
from model.helper import StructureDescriptionGenerator
from model.helper import RadixDescription
from model.helper import RadixCodeInfoDescription

from injector import inject

from parser import TreeParser

class QHTreeParser:
	@inject
	def __init__(self, nodeGenerator: StructureDescriptionGenerator):
		self.treeParser = TreeParser
		self.treeParser.nodeGenerator = nodeGenerator

	def parse(self, expression):
		return self.treeParser.parse(expression)

class QHSubstituteRuleParser:
	@inject
	def __init__(self):
		pass

	def loadSubstituteRules(self, filename):
		node=yaml.load(open(filename), yaml.SafeLoader)
		ruleSetNode=node.get(Constant.TAG_RULE_SET)

		if not ruleSetNode:
			return []

		substituteRules=[]
		for node in ruleSetNode:
			matchPattern=node.get(Constant.TAG_MATCH)
			replacePattern=node.get(Constant.TAG_SUBSTITUTE)

			substitueRule=SubstituteRule(matchPattern, replacePattern)
			substituteRules.append(substitueRule)

		return substituteRules

class QHParser:
	@inject
	def __init__(self, treeParser: QHTreeParser):
		self.treeParser = TreeParser

	def parseStructure(self, structureExpression):
		return self.treeParser.parse(structureExpression)

	def loadCharDescriptionByParsingYAML(self, rootNode):
		charGroupNode = rootNode.get(Constant.TAG_CHARACTER_SET)
		charGroupNode = charGroupNode if charGroupNode is not None else []

		charDescList = []
		for node in charGroupNode:
			charName=node.get(Constant.TAG_NAME)

			charDesc=CharacterDescription(charName)

			structureList = self.loadStructureSet(node)
			charDesc.setStructureList(structureList)

			charDescList.append(charDesc)
		return charDescList

	def loadStructureSet(self, charNode):
		structureList=[]
		if Constant.TAG_STRUCTURE_SET in charNode:
			nodeStructureList=charNode.get(Constant.TAG_STRUCTURE_SET)

			for structureDict in nodeStructureList:
				structureExpression = structureDict[Constant.TAG_STRUCTURE]

				fontVariance = FontVariance.All
				if Constant.TAG_FONT_VARIANCE in structureDict:
					fontVarianceDescription = structureDict[Constant.TAG_FONT_VARIANCE]
					fontVariance = self.convertDescriptionToFontVariance(fontVarianceDescription)

				structureDesc = self.parseStructure(structureExpression)
				structureDesc.changeFontVariance(fontVariance)

				structureList.append(structureDesc)

		return structureList

	def loadCharacters(self, filename):
		node=yaml.load(open(filename), yaml.SafeLoader)
		return self.loadCharDescriptionByParsingYAML(node)

	def convertDescriptionToFontVariance(self, description):
		if not description:
			return FontVariance.All
		elif description in Constant.LIST__FONT_VARIANCE__TRADITIONAL:
			return FontVariance.Traditional
		elif description in Constant.LIST__FONT_VARIANCE__SIMPLIFIED:
			return FontVariance.Simplified
		else:
			return FontVariance.All

class QHRadixParser:
	TAG_CODE_INFORMATION='編碼資訊'
	TAG_CODE='編碼'

	@inject
	def __init__(self, codingRadixParser: CodingRadixParser):
		self.codingRadixParser = codingRadixParser

	def loadRadix(self, radixFileList):
		radixDescriptionList = self.parse(radixFileList)
		return radixDescriptionList

	def convertRadixDescToCodeInfoList(self, radixDesc):
		radixCodeInfoList=[]
		tmpRadixCodeInfoList=radixDesc.getRadixCodeInfoDescriptionList()
		for radixInfo in tmpRadixCodeInfoList:
			codeInfo=self.convertRadixDescToCodeInfoWithAttribute(radixInfo)
			if codeInfo:
				radixCodeInfoList.append(codeInfo)
		return radixCodeInfoList

	def convertRadixDescToCodeInfoWithAttribute(self, radixDesc):
		codeInfo=self.codingRadixParser.convertRadixDescToCodeInfo(radixDesc)

		codeVariance=radixDesc.getCodeVarianceType()
		isSupportCharacterCode=radixDesc.isSupportCharacterCode()
		isSupportRadixCode=radixDesc.isSupportRadixCode()
		codeInfo.setCodeInfoAttribute(codeVariance, isSupportCharacterCode, isSupportRadixCode)

		return codeInfo

	def convertElementToRadixInfo(self, elementCodeInfo):
		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo

		codeElementCodeInfo=elementCodeInfo
		radixInfoDescription=RadixCodeInfoDescription(infoDict, codeElementCodeInfo)
		return radixInfoDescription

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=CodeInfo()
		return codeInfo

	def parse(self, toRadixList):
		totalRadixDescriptionList = []
		for filename in toRadixList:
			radixDescriptionList = self.parseRadixFromYAML(filename)
			totalRadixDescriptionList.extend(radixDescriptionList)

		return totalRadixDescriptionList

	def parseRadixFromYAML(self, filename):
		rootNode=yaml.load(open(filename), Loader=yaml.SafeLoader)

		return self.parseRadixInfo(rootNode)

	def parseRadixInfo(self, rootNode):
		radixDescriptionList = []
		characterSetNode=rootNode.get(Constant.TAG_CHARACTER_SET)
		for characterNode in characterSetNode:
			charName=characterNode.get(Constant.TAG_NAME)
			radixDescription=self.parseRadixDescription(characterNode)
			radixDescriptionList.append(radixDescription)
		return radixDescriptionList

	def parseRadixDescription(self, nodeCharacter):
		radixCodeInfoDescList=[]
		toOverridePrev=("是" == nodeCharacter.get("覆蓋"))
		radixName=nodeCharacter.get(Constant.TAG_NAME)
		for elementCodeInfo in nodeCharacter.get(QHRadixParser.TAG_CODE_INFORMATION):
			radixCodeInfoDesc=self.convertElementToRadixInfo(elementCodeInfo)
			radixCodeInfoDescList.append(radixCodeInfoDesc)
		return RadixDescription(radixName, radixCodeInfoDescList, toOverridePrev)

	def parseFileType(self, rootNode):
		fileType=rootNode.get(Constant.TAG_FILE_TYPE)
		return fileType

	def parseInputMethod(self, rootNode):
		nameInputMethod=rootNode.get(Constant.TAG_INPUT_METHOD)
		return nameInputMethod

