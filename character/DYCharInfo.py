from .CharInfo import CharInfo

class DYCharInfo(CharInfo):
	def setPropDict(self, propDict):
		str_rtlist=propDict.get('資訊表示式')
		if str_rtlist!=None:
			self.setDYProp(str_rtlist)

	def setByComps(self, operator, complist):
		dylist=list(map(lambda c: c.getDYProp(), complist))
		if complist and all(dylist):
			cat="".join(dylist)
			dy=cat[:3]+cat[-1] if len(cat)>4 else cat
			self.setDYProp(dy)

	@property
	def code(self):
		return self._dy_incode

	def setDataEmpty(self):
		CharInfo.setDataEmpty(self)
		self._dy_incode=None

	def setSingleDataEmpty(self):
		pass

	def setDYProp(self, dy_incode):
		if dy_incode!=None:
			self.setDataInitialized()
			self._dy_incode=dy_incode

	def getDYProp(self):
		return self._dy_incode

