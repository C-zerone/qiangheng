import sys
from . import HanZiStructure
from gear import CharacterInfo

class HanZiNode:
	def __init__(self, name, characterProperty=None):
		self.name=name
		self.structureList=[]
		self.characterProperty=characterProperty

		freq=characterProperty.getFrequency()
		characterInfo=CharacterInfo.CharacterInfo(self.name, freq)
		self.characterInfo=characterInfo

	def getName(self):
		return self.name

#	def getCharacterProperty(self):
#		return self.characterProperty

	def addStructure(self, structure):
		self.structureList.append(structure)

	def setStructureList(self, structureList):
		self.structureList=structureList

	def getStructureList(self):
		return self.structureList

	def getStructureListWithCondition(self):
		return self.structureList

	def getSubStructureList(self, index):
		subStructureList=[]
		for structure in self.structureList:
			if isinstance(structure, HanZiStructure.HanZiAssemblageStructure):
				structureList=structure.getStructureList()
				subStructureList.append(structureList[index])
		return subStructureList

	def getCodeInfoList(self):
		structureList=self.getStructureListWithCondition()

		return sum(map(lambda s: s.getCodeInfoList(), structureList), [])

	def getCharacterInfo(self):
		codeInfoList=self.getCodeInfoList()
		self.characterInfo.setCodeInfoList(codeInfoList)

		return self.characterInfo

	def setNodeTree(self):
		"""設定某一個字符所包含的部件的碼"""

		structureList=self.getStructureListWithCondition()

		for structure in structureList:
			structure.setStructureTree()

	def printAllCodeInfoInStructure(self):
		structureList=self.getStructureListWithCondition()
		for struct in structureList:
			struct.printAllCodeInfo()

