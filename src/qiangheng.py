#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from parser import ConfigParser
from optparse import OptionParser
from state import StateManager
from im.IMMgr import IMMgr
from description.CharacterDescriptionManager import CharacterDescriptionManager
from hanzi.HanZiNetwork import HanZiNetwork

class QiangHeng:
	def __init__(self, options):
		inputMethod=options.input_method
		toTemplateList = [
			'gen/qhdata/main/template.xml',
		]
		toComponentList = [
			'gen/qhdata/main/frequency/CJK.xml',
			'gen/qhdata/main/frequency/CJK-A.xml',

			'gen/qhdata/main/CJK.xml',
			'gen/qhdata/main/CJK-A.xml',
			'gen/qhdata/main/component/CJK.xml',
			'gen/qhdata/main/component/CJK-A.xml',
			'gen/qhdata/main/style.xml',
			'gen/qhdata/%s/style.xml'%inputMethod,
			'gen/qhdata/%s/component/CJK.xml'%inputMethod,
			'gen/qhdata/%s/component/CJK-A.xml'%inputMethod,
		]
		isYaml = inputMethod != "dc"
		toCodeList = [
			('gen/qhdata/%s/radix/CJK.yaml' if isYaml else 'gen/qhdata/%s/radix/CJK.xml')%inputMethod,
			('gen/qhdata/%s/radix/CJK-A.yaml' if isYaml else 'gen/qhdata/%s/radix/CJK-A.xml')%inputMethod,
		]
		imPackage=IMMgr.getIMPackage(inputMethod)

		output_format=options.output_format
		isFormatXML=(output_format=='xml')
		isFormatYAML=(output_format=='yaml')
		isFormatTXT=(output_format=='text')
		isFormatQuiet=(output_format=='quiet')

		quiet=options.quiet or isFormatQuiet
		isToOutput=not quiet

		StateManager.setIMPackage(imPackage)

		StateManager.getCodeInfoManager().loadRadix(toCodeList)

		operationManager=StateManager.getOperationManager()
		self.descMgr=CharacterDescriptionManager(operationManager)
		self.descMgr.loadData(toTemplateList, toComponentList)

		self.hanziNetwork=HanZiNetwork.construct(self.descMgr)

		codeMappingInfoList=self.genIMMapping()
#		sortedCodeMappingInfoList=codeMappingInfoList
		sortedCodeMappingInfoList=sorted(codeMappingInfoList, key=lambda y: y.getKey())

		if isToOutput:
			if isFormatXML:
				from writer import XmlWriter
				writer = XmlWriter.XmlWriter()
			elif isFormatYAML:
				from writer import YamlWriter
				writer = YamlWriter.YamlWriter()
			elif isFormatTXT:
				from writer import TxtWriter
				writer = TxtWriter.TxtWriter()
			else:
				from writer import TxtWriter
				writer = TxtWriter.TxtWriter()
		else:
			# 不輸出結果
			from writer import QuietWriter
			writer = QuietWriter.QuietWriter()

		imInfo=imPackage.IMInfo()
		writer.write(imInfo, sortedCodeMappingInfoList)

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
	oparser.add_option("-i", "--im", "--input-method", dest="input_method", help="輸入法", default="cj")
	oparser.add_option("--format", type="choice", choices=["xml", "yaml", "text", "quiet"], dest="output_format", help="輸出格式，可能的選項有：xml、yaml、text、quiet", default="text")
	oparser.add_option("-q", "--quiet", action="store_true", dest="quiet")
	(options, args) = oparser.parse_args()

	qiangheng=QiangHeng(options)

if __name__ == "__main__":
	main()

