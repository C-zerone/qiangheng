from .CharInfo import CharInfo

class ARCharInfo(CharInfo):
	def setPropDict(self, propDict):
		str_rtlist=propDict.get('資訊表示式')
		if str_rtlist!=None:
			self.setARProp(str_rtlist)

	def setByComps(self, operator, complist):
		arlist=list(map(lambda c: c.getARProp(), complist))
		if complist and all(arlist):
			cat="".join(arlist)
			ar=cat[:3]+cat[-1] if len(cat)>4 else cat
			self.setARProp(ar)

	@property
	def code(self):
		return self._ar_incode

	def setDataEmpty(self):
		CharInfo.setDataEmpty(self)
		self._ar_incode=None

	def setSingleDataEmpty(self):
		pass

	def setARProp(self, ar_incode):
		if ar_incode!=None:
			self.setDataInitialized()
			self._ar_incode=ar_incode

	def getARProp(self):
		return self._ar_incode

