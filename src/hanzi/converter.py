from injector import inject

from .helper import HanZiNetworkManager
from .helper import HanZiCodeInfosComputer
from .helper import HanZiNetworkItemFactory

from model.element.enum import FontVariance

from model.StructureManager import StructureManager
from model.CharacterDescriptionManager import RadixManager
from model.tree.regexp import TreeRegExpInterpreter
from model.tree.regexp import BasicTreeProxy
from model.tree.regexp import TreeNodeGenerator

class HanZiTreeProxy(BasicTreeProxy):
	def getChildren(self, currentStructure):
		return currentStructure.getExpandedStructureList()

	def matchSingleQuickly(self, tre, currentStructure):
		treOperatorName = tre.prop.get("運算")
		expandedOperatorName = currentStructure.getExpandedOperatorName()
		return expandedOperatorName and (treOperatorName == None or treOperatorName == expandedOperatorName)

	def matchSingle(self, tre, currentStructure):
		prop = tre.prop
		isMatch = True
		if "名稱" in prop:
			expressionName = prop.get("名稱")
			isMatch = expressionName == currentStructure.getReferenceExpression()

		if "運算" in prop:
			operatorName = prop.get("運算")
			isMatch = operatorName == currentStructure.getExpandedOperatorName()

		return isMatch

class HanZiTreeNodeGenerator(TreeNodeGenerator):
	@inject
	def __init__(self, itemFactory: HanZiNetworkItemFactory):
		self.itemFactory = itemFactory

	def generateLeafNode(self, nodeName):
		return self.itemFactory.getWrapperStructureByNodeName(nodeName)

	def generateLeafNodeByReference(self, referencedTreeNode, index):
		structure=referencedTreeNode
		return self.itemFactory.getWrapperStructureByNodeName(structure.getReferencedNodeName(), index)

	def generateNode(self, operatorName, children):
		return self.itemFactory.getCompoundStructureByOperatorName(operatorName, children)

class HanZiTreeRegExpInterpreter(TreeRegExpInterpreter):
	@inject
	def __init__(self, treeNodeGenerator: HanZiTreeNodeGenerator):
		super().__init__(HanZiTreeProxy(), treeNodeGenerator)


def isBelongToFontVariance(characterFontVariance, targetFontVariance):
	if targetFontVariance == FontVariance.All:
		return True
	elif targetFontVariance == FontVariance.Traditional:
		return characterFontVariance in [FontVariance.All, FontVariance.Traditional]
	elif targetFontVariance == FontVariance.Simplified:
		return characterFontVariance in [FontVariance.All, FontVariance.Simplified]
	else:
		return False

class ComputeCharacterInfo:
	@inject
	def __init__(self,
			fontVariance: FontVariance,

			structureManager: StructureManager,
			radixManager: RadixManager,
			treInterpreter: HanZiTreeRegExpInterpreter,

			networkManager: HanZiNetworkManager,
			codeInfosComputer: HanZiCodeInfosComputer,
			itemFactory: HanZiNetworkItemFactory
			):
		self.fontVariance = fontVariance

		self.structureManager = structureManager
		self.radixManager = radixManager

		self.networkManager = networkManager
		self.codeInfosComputer = codeInfosComputer
		self.itemFactory = itemFactory

		self.treInterpreter = treInterpreter

	def compute(self, characters):
		for character in characters:
			self.constructCharacter(character)

	def constructCharacter(self, character):
		node = self.touchCharacter(character)
		nodeStructure = node.getNodeStructure()
		self.expandNodeStructure(nodeStructure)
		self.computeNode(nodeStructure)

	def queryDescription(self, characterName):
		return self.structureManager.queryCharacterDescription(characterName)

	def touchCharacter(self, character):
		return self.itemFactory.touchNode(character)

	def expandNodeStructure(self, nodeStructure):
		nodeStructureInfo = nodeStructure.getStructureInfo()

		character = nodeStructureInfo.getName()
		if self.networkManager.isNodeExpanded(character):
			return

		if self.radixManager.hasRadix(character) and len(nodeStructureInfo.getUnitStructureList())==0:
			radixInfoList=self.radixManager.getRadixCodeInfoList(character)
			for radixCodeInfo in radixInfoList:
				structure = self.itemFactory.getUnitStructure(radixCodeInfo)
				self.networkManager.addStructureIntoNode(structure, nodeStructure)

		charDesc=self.queryDescription(character)

		nodeName = character
		structDescList=charDesc.getStructureList()
		for structDesc in structDescList:
			if structDesc.isEmpty():
				continue

			characterFontVariance = structDesc.getFontVariance()
			isMainStructure = isBelongToFontVariance(characterFontVariance, self.fontVariance)

			structure=self.recursivelyConvertDescriptionToStructure(structDesc)

			templateRuleList=self.structureManager.getTemplateRules()
			self.recursivelyRearrangeStructureByTemplate(structure, templateRuleList)
			substituteRuleList=self.structureManager.getSubstituteRules()
			self.recursivelyRearrangeStructureBySubstitute(structure, substituteRuleList)

			self.networkManager.addStructureIntoNode(structure, nodeStructure)
			if isMainStructure:
				self.networkManager.setMainStructureOfNode(structure, nodeStructure)

	def recursivelyConvertDescriptionToStructure(self, structDesc):
		if structDesc.isLeaf():
			structure=self.generateReferenceLink(structDesc)
		else:
			structure=self.generateLink(structDesc)

		return structure

	def recursivelyRearrangeStructureByTemplate(self, structure, substituteRuleList):
		nodeStructure = structure.getStructureInfo().getReferencedNodeStructure()
		if nodeStructure:
			self.expandNodeStructure(nodeStructure)

		tag=structure.getTag()
		if tag.isTemplateApplied():
			return

		self.rearrangeStructure(structure, substituteRuleList)
		for childStructure in structure.getStructureList():
			self.recursivelyRearrangeStructureByTemplate(childStructure, substituteRuleList)

		tag.setTemplateApplied()

	def recursivelyRearrangeStructureBySubstitute(self, structure, substituteRuleList):
		nodeStructure = structure.getStructureInfo().getReferencedNodeStructure()
		if nodeStructure:
			self.expandNodeStructure(nodeStructure)

		tag=structure.getTag()
		if tag.isSubstituteApplied():
			return

		self.rearrangeStructure(structure, substituteRuleList)
		for childStructure in structure.getStructureList():
			self.recursivelyRearrangeStructureBySubstitute(childStructure, substituteRuleList)

		tag.setSubstituteApplied()

	def rearrangeStructure(self, structure, substituteRuleList):
		treInterpreter = self.treInterpreter
		def expandLeaf(structure):
			referenceNode = structure.getReferencedNode()
			if referenceNode:
				self.expandNodeStructure(referenceNode.getNodeStructure())

			children=structure.getStructureList()
			for child in children:
				expandLeaf(child)

		def rearrangeStructureOneTurn(structure, filteredSubstituteRuleList):
			changed=False
			for rule in filteredSubstituteRuleList:
				tre = rule.getTRE()
				result = rule.getReplacement()

				tmpStructure = treInterpreter.matchAndReplace(tre, structure, result)
				if tmpStructure!=None:
					structure.setNewStructure(tmpStructure)
					structure=tmpStructure
					changed=True
					break
			return changed

		changed=True
		while changed:
			availableRuleFilter = lambda rule: treInterpreter.matchQuickly(rule.getTRE(), structure)
			filteredSubstituteRuleList = filter(availableRuleFilter, substituteRuleList)
			changed=rearrangeStructureOneTurn(structure, filteredSubstituteRuleList)

	def generateReferenceLink(self, structDesc):
		name=structDesc.getReferenceName()
		nodeExpression=structDesc.getReferenceExpression()

		self.constructCharacter(name)

		l=nodeExpression.split(".")
		if len(l)>1:
			subIndex=int(l[1])
		else:
			subIndex=0

		return self.itemFactory.getWrapperStructureByNodeName(name, subIndex)

	def generateLink(self, structDesc):
		childStructureList = []
		childDescList=self.structureManager.queryChildren(structDesc)
		for childSrcDesc in childDescList:
			childStructure = self.recursivelyConvertDescriptionToStructure(childSrcDesc)
			childStructureList.append(childStructure)

		operator=structDesc.getOperator()

		return self.itemFactory.getCompoundStructure(operator, childStructureList)

	def computeNode(self, nodeStructure):
		self.codeInfosComputer.computeForNodeStructure(nodeStructure)

