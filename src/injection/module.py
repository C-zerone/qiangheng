from injector import Module
from injector import provider

from model.base.CodeInfoEncoder import CodeInfoEncoder
from model.base.CodingInfo import CodingInfo

from Constant import Package
from Constant import CodingRadixParser

class PackageModule(Module):
	@provider
	def provideCodingInfo(self, package: Package) -> CodingInfo:
		return package.CodingInfo()

	@provider
	def provideCodeInfoEncoder(self, codingPackage: Package) -> CodeInfoEncoder:
		return codingPackage.CodeInfoEncoder

	@provider
	def provideCodingRadixParser(self, codingPackage: Package) -> CodingRadixParser:
		return codingPackage.RadixParser()
