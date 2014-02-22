#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

#from xml.etree import ElementTree as ET
import lxml.etree as ET
from optparse import OptionParser
from state import StateManager
from im.IMMgr import IMMgr
from description.CharacterDescriptionManager import CharacterDescriptionManager
from hanzi.HanZiNetwork import HanZiNetwork

class QiangHeng:
	def __init__(self, options):
		configFile=options.config_file
		xml_format=options.xml_format
		quiet=options.quiet
		isToOutput=not quiet

		configList=self.readConfig(configFile)
		[imProp, toTemplateList, toComponentList, toCodeList]=configList

		imPackage=IMMgr.getIMPackage(imProp)
		StateManager.setIMPackage(imPackage)

		StateManager.getCodeInfoManager().loadRadix(toCodeList)

		operationManager=StateManager.getOperationManager()
		self.descMgr=CharacterDescriptionManager(operationManager)
		self.descMgr.loadData(toTemplateList, toComponentList)

		self.hanziNetwork=HanZiNetwork.construct(self.descMgr)

		codeMappingInfoList=self.genIMMapping()
		if isToOutput:
			if xml_format:
				imInfo=imPackage.IMInfo()
				self.toXML(imInfo, codeMappingInfoList)
			else:
				self.toTXT(codeMappingInfoList)
		else:
			# 不輸出結果
			pass

	def readConfig(self, configFileName):
		f=open(configFileName, encoding='utf-8-sig')
		xmlNode=ET.parse(f)
		rootNode=xmlNode.getroot()

		configNode=rootNode.find('設定')
		imNode=configNode.find('輸入法')
		imProp=imNode.attrib

#		configFileNode=rootNode.find('設定檔')
		[toTemplateList, toComponentList, toCodeList]=self.getConfigFiles(configFileName)

		return [imProp, toTemplateList, toComponentList, toCodeList]

	def getConfigFiles(self, configFileName):
		f=open(configFileName, encoding='utf-8-sig')
		xmlNode=ET.parse(f)
		rootNode=xmlNode.getroot()
		configFileNode=rootNode.find('設定檔')

		importNodeList=configFileNode.findall('匯入')

		templateNodeList=configFileNode.findall('範本')
		componentNodeList=configFileNode.findall('部件')
		radixNodeList=configFileNode.findall('字根')

		rootDirPrefix=configFileNode.get('資料目錄')

		toComponentList=[]
		toTemplateList=[]
		toCodeList=[]

		for node in importNodeList:
			fileName=rootDirPrefix+node.get('檔案')
			[tmpToTemplateList, tmpToComponentList, tmpToCodeList]= \
				self.getConfigFiles(fileName)
			toComponentList.extend(tmpToComponentList)
			toTemplateList.extend(tmpToTemplateList)
			toCodeList.extend(tmpToCodeList)

		tmpToComponentList=[rootDirPrefix+node.get('檔案') for node in componentNodeList]
		tmpToTemplateList=[rootDirPrefix+node.get('檔案') for node in templateNodeList]
		tmpToCodeList=[rootDirPrefix+node.get('檔案') for node in radixNodeList]

		toComponentList.extend(tmpToComponentList)
		toTemplateList.extend(tmpToTemplateList)
		toCodeList.extend(tmpToCodeList)

		return [toTemplateList, toComponentList, toCodeList]


	def toXML(self, imInfo, codeMappingInfoList):
		keyMaps=imInfo.getKeyMaps()

		rootNode=ET.Element("輸入法")

		# 名稱
		nameNode=ET.SubElement(rootNode, "輸入法名稱",
			attrib={
				"EN":imInfo.getName('en'),
				"TW":imInfo.getName('tw'),
				"CN":imInfo.getName('cn'),
				"HK":imInfo.getName('hk'),
#				"SG":imInfo.getName('sg'),
				})

		# 屬性
		propertyNode=ET.SubElement(rootNode, "屬性",
			attrib={
				"最大按鍵數":"%s"%imInfo.getMaxKeyLength()
				})

		# 按鍵與顯示的對照表
		keyMapsNode=ET.SubElement(rootNode, "按鍵對應集")
		for key, disp in keyMaps:
			ET.SubElement(keyMapsNode, "按鍵對應", attrib={"按鍵":key, "顯示":disp})

		# 對照表
		charGroup=ET.SubElement(rootNode, "對應集")
		for x in sorted(codeMappingInfoList, key=lambda y: y.getKey()):
			attrib={"按鍵序列":x.getCode(), "字符":x.getName(), "頻率":x.getFrequency(), "類型":x.getVariance()}
			ET.SubElement(charGroup, "對應", attrib)
		xmlNode=ET.ElementTree(rootNode)
		print(ET.tounicode(xmlNode, pretty_print=True))
#		ET.dump(xmlNode)
#		xmlNode.write(sys.stdout)

	def toTXT(self, codeMappingInfoList):
		table="\n".join(sorted(map(lambda x : '{0}\t{1}'.format(*x.getKey()), codeMappingInfoList)))
		print(table)

	def genIMMapping(self):
		characterFilter=lambda charName: (len(charName)==1)
#		targetCharacterList=[]
		targetCharacterList=filter(characterFilter, self.descMgr.getAllCharacters())
		table=[]
		for charName in sorted(targetCharacterList):
#			print("<-- %s -->"%charName, sys.stderr)
			characterInfo=self.hanziNetwork.getCharacterInfo(charName)
			table.extend(characterInfo.getCodeMappingInfoList())
		return table

def main():
	oparser = OptionParser()
	oparser.add_option("-c", "--config", dest="config_file", help="輸入法設定檔", default="qhdata/config/default.xml")
	oparser.add_option("--xml", action="store_true", dest="xml_format")
	oparser.add_option("--text", action="store_false", dest="xml_format")
	oparser.add_option("-q", "--quiet", action="store_true", dest="quiet")
	(options, args) = oparser.parse_args()

	qiangheng=QiangHeng(options)

if __name__ == "__main__":
	main()

