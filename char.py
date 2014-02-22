
class Char:
	def __init__(self, char, prop):
		self.char=char

		self.structure=prop[0]

		self._cangjie=None
		self._array=None
		self._dayi=None
		self._boshiamy=None
		self._boshiamy_supplement=None
		self._zhengma=None
		self._zhengma_type=None

		if len(prop)>=8:
			self.setIMproperty(prop)

	def __str__(self):
		return self.char

	def __repr__(self):
		return str(self)

	def setIMproperty(self, prop):
		self.setCJProp(prop[1])
		self.setARProp(prop[2])
		self.setDYProp(prop[3])
		self.setBSProp(prop[4], prop[5])
		self.setZMProp(prop[6], prop[7])

	def setCJProp(self, cj_incode):
		if cj_incode=='XXXX':
			self._cangjie=None
		else:
			self._cangjie=cj_incode

	def getCJProp(self):
		return self._cangjie

	def setARProp(self, ar_incode):
		if ar_incode=='XXXX':
			self._array=None
		else:
			self._array=ar_incode

	def getARProp(self):
		return self._array

	def setDYProp(self, dy_incode):
		if dy_incode=='XXXX':
			self._dayi=None
		else:
			self._dayi=dy_incode

	def getDYProp(self):
		return self._dayi

	def setBSProp(self, bs_incode, bs_spcode):
		if bs_incode=='XXXX' or bs_spcode=='XXXX':
			self._boshiamy=None
			self._boshiamy_supplement=None
		else:
			self._boshiamy=bs_incode
			self._boshiamy_supplement=bs_spcode

	def getBSProp(self):
		return [self._boshiamy, self._boshiamy_supplement]

	def setZMProp(self, zm_incode, zm_intype):
		if zm_incode=='XXXX' or zm_intype=='XXXX':
			self._zhengma=None
			self._zhengma_type=None
		else:
			self._zhengma=zm_incode
			self._zhengma_type=zm_intype

	def getZMProp(self):
		return [self._zhengma, self._zhengma_type]

	@property
	def cj(self):
		return self._cangjie

	@property
	def ar(self):
		return self._array

	@property
	def dy(self):
		return self._dayi

	@property
	def bs(self):
		if self._boshiamy==None or self._boshiamy_supplement==None:
			return None
		if len(self._boshiamy)<3:
			return self._boshiamy+self._boshiamy_supplement
		else:
			return self._boshiamy

	@property
	def zm(self):
		if self._zhengma==None:
			return None
		else:
			return self._zhengma

if __name__=='__main__':
	c=Char('王', ['(龜)', 'hn', 'sl', '/c', 'k', 'l', 'qy', '12'])
	print('倉頡', c.cj)
	print('行列', c.ar)
	print('大易', c.dy)
	print('嘸蝦米', c.bs, c.bssp)
	print('鄭碼', c.zm, c.zmtp)

