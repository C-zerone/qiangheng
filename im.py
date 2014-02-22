
class NoneIM:
	"輸入法"

	class CharInfo:
		def __init__(self, charname, parseans, prop):
			self.charname=charname
			self.operator=parseans[0]
			self.operandlist=parseans[1]

			self.showFlag=False if len(self.charname)>1 else True
			self.noneFlag=True

		def __str__(self):
			return self.charname

		def __repr__(self):
			return str(self)

		def isToShow(self):
			return self.showFlag

		def isToSetTree(self):
			# 若非空且之前没設過值
			return (not self.isNone) and (not self.isSeted)

		def setByComps(self, complist):
			pass

		@property
		def isNone(self):
			# 是否為空
			return self.noneFlag

		@property
		def isSeted(self):
			# 是否之前設過值，會被覆蓋
			return False
	CharInfo.NoneChar=CharInfo('[瑲珩預設空字符]', ['龜', []], [])
	CharInfo.NoneChar.noneFlag=True

	def __init__(self):
		self.keyMaps=[]
		self.nameDict={
				'cn':'空',
				'tw':'空',
				'hk':'空',
				'en':'None',
				}
		self.iconfile="empty.png"
		self.maxkeylength=0

	def getName(self, localization):
		return self.nameDict.get(localization, "")

	def getIconFileName(self):
		return self.iconfile

	def getMaxKeyLength(self):
		return self.maxkeylength

	def getKeyList(self):
		return "".join(list(zip(*self.keyMaps))[0])

	def setTable(self, tb):
		self.tb=tb
		self.method='T'

	def setStruct(self, chdict):
		self.chdict=chdict
		self.method='D'

	def genIMMapping(self):
		if self.method=='D':
			table=[]
			for chname, ch in self.chdict.items():
				self.setCharTree(ch)
				code=self.getCode(ch)
				if ch.isToShow() and code:
					table.append([code, chname])
				else:
					pass
#					print("Debug", chname)
		elif self.method=='T':
			table=self.tb
		else:
			table=[]
		return table

	def getCode(self, ch):
		pass

	def setCharTree(self, ch):
		if not ch.isToSetTree():
			return

		complist=self.getAllComp(ch)

		for tmpch in complist:
			self.setCharTree(tmpch)

		ch.setByComps(complist)

	def getAllComp(self, ch):
#		['水', '林', '爻', '卅', '丰', '鑫', '卌', '圭', '燚',]
#		['好', '志',
#		'回', '同', '函', '區', '左',
#		'起', '廖', '載', '聖', '句',
#		'夾', '衍', '衷',]
#		['纂', '膷',]
		chdict=self.chdict
		if ch.operator in ['龜']:
			return []
		elif ch.operator in ['水']:
			x=chdict.get(ch.operandlist[0], None)
			return [x]
		elif ch.operator in ['好', '志', '回', '同', '函', '區', '載', '廖', '起', '句', '夾']:
			x=chdict.get(ch.operandlist[0], None)
			y=chdict.get(ch.operandlist[1], None)
			return [x, y]
		elif ch.operator in ['算', '湘', '霜', '想', '怡', '穎',]:
			x=chdict.get(ch.operandlist[0], None)
			y=chdict.get(ch.operandlist[1], None)
			z=chdict.get(ch.operandlist[2], None)
			return [x, y, z]
		elif ch.operator in ['纂',]:
			x=chdict.get(ch.operandlist[0], None)
			y=chdict.get(ch.operandlist[1], None)
			z=chdict.get(ch.operandlist[2], None)
			w=chdict.get(ch.operandlist[3], None)
			return [x, y, z, w]
		elif ch.operator in ['林', '爻']:
			x=chdict.get(ch.operandlist[0], None)
			return [x, x]
		elif ch.operator in ['卅', '鑫']:
			x=chdict.get(ch.operandlist[0], None)
			return [x, x, x]
		elif ch.operator in ['燚',]:
			x=chdict.get(ch.operandlist[0], None)
			return [x, x, x, x]
		else:
			return []

class CangJie(NoneIM):
	"倉頡輸入法"

	class CJCharInfo(NoneIM.CharInfo):
		def __init__(self, charname, parseans, prop):
			NoneIM.CharInfo.__init__(self, charname, parseans, prop)
			self._cj_incode=None	# 當獨體使用
			self._cj_rtcode=None	# 當部件使用
			if len(prop)>=2:
				self.setCJProp(prop[0], prop[1])
			self.noneFlag=False
			self.setedFlag=False

		def setCJProp(self, cj_incode, cj_rtcode):
			if cj_incode=='XXXX':
				self._cj_incode=None
			else:
				self._cj_incode=cj_incode

			if cj_rtcode=='XXXX':
#				self._cj_rtcode=None
				# 目前先假設跟 _cj_incode 一樣
				if cj_incode=='XXXX':
					self._cj_rtcode=None
				else:
					self._cj_rtcode=cj_incode
			else:
				self._cj_rtcode=cj_rtcode

		def getCJProp(self):
			return [self._cj_incode, self._cj_rtcode]

		def setCJByComps(self, prelist, postlist):
			def CJCombideCode(first, second):
				tmpfirst=first if len(first)<=2 else first[0]+first[-1]
				tmpsecond=second if len(second)<=2 else second[0]+second[-1]
				anscode=tmpfirst+tmpsecond
				anscode=anscode if len(anscode)<=3 else anscode[0:2]+anscode[-1]
				return anscode

			def getCJRootCodeAsBody(rtcodelist):
				tmpcode=rtcodelist[0]
				tmpcode=tmpcode if len(tmpcode)<=3 else tmpcode[0:2]+tmpcode[-1]
				for rtcode in rtcodelist[1:]:
					tmpcode=CJCombideCode(tmpcode, rtcode)
				return tmpcode

			cjlist=[list(map(lambda c: c.getCJProp()[1], prelist)),
					list(map(lambda c: c.getCJProp()[1], postlist))]
			if cjlist[0] and cjlist[1] and all(cjlist[0]) and all(cjlist[1]):
				headcode=getCJRootCodeAsBody(cjlist[0])
				headcode=headcode if len(headcode)<=2 else headcode[0]+headcode[-1]
				bodycode=getCJRootCodeAsBody(cjlist[1])
				cjcode=headcode+bodycode
				cjbodycode=CJCombideCode(headcode, bodycode)
				self.setCJProp(cjcode, cjbodycode)

		@property
		def cj(self):
			return self._cj_incode

		@property
		def isSeted(self):
			return bool(self._cj_incode)

	def __init__(self):
		self.keyMaps=[
			['a', '日',],
			['b', '月',],
			['c', '金',],
			['d', '木',],
			['e', '水',],
			['f', '火',],
			['g', '土',],
			['h', '竹',],
			['i', '戈',],
			['j', '十',],
			['k', '大',],
			['l', '中',],
			['m', '一',],
			['n', '弓',],
			['o', '人',],
			['p', '心',],
			['q', '手',],
			['r', '口',],
			['s', '尸',],
			['t', '廿',],
			['u', '山',],
			['v', '女',],
			['w', '田',],
			['x', '難',],
			['y', '卜',],
			['z', '符',],
			]
		self.nameDict={
				'cn':'仓颉',
				'tw':'倉頡',
				'hk':'倉頡',
				'en':'CangJie',
				}
		self.iconfile="CangJie.png"
		self.maxkeylength=5

	def getCode(self, ch):
		if ch.cj:
			return ch.cj

	def getCJPrePostList(self, ch):
		"""傳回倉頡的字首及字尾的部件串列"""
		chdict=self.chdict
		prelist=[]
		postlist=[]
		if ch.operator in ['龜']:
			prelist=[]
			postlist=[]
		elif ch.operator in ['水']:
			x=chdict.get(ch.operandlist[0], None)
			prelist=[x]
			postlist=[]
		elif ch.operator in ['好', '志', '回', '同', '函', '區', '載', '廖', '起', '句', '夾']:
			x=chdict.get(ch.operandlist[0], None)
			y=chdict.get(ch.operandlist[1], None)
			prelist=[x]
			postlist=[y]
		elif ch.operator in ['算', '湘', '霜', '怡',]:
			x=chdict.get(ch.operandlist[0], None)
			y=chdict.get(ch.operandlist[1], None)
			z=chdict.get(ch.operandlist[2], None)
			prelist=[x]
			postlist=[y, z]
		elif ch.operator in ['想', '穎',]:
			x=chdict.get(ch.operandlist[0], None)
			y=chdict.get(ch.operandlist[1], None)
			z=chdict.get(ch.operandlist[2], None)
			prelist=[x, y]
			postlist=[z]
		elif ch.operator in ['林', '爻']:
			x=chdict.get(ch.operandlist[0], None)
			prelist=[x]
			postlist=[x]
		elif ch.operator in ['卅', '鑫']:
			x=chdict.get(ch.operandlist[0], None)
			prelist=[x]
			postlist=[x, x]
		elif ch.operator in ['燚',]:
			x=chdict.get(ch.operandlist[0], None)
			prelist=[x, x]
			postlist=[x, x]
		elif ch.operator in ['纂',]:
			x=chdict.get(ch.operandlist[0], None)
			y=chdict.get(ch.operandlist[1], None)
			z=chdict.get(ch.operandlist[2], None)
			w=chdict.get(ch.operandlist[3], None)
			prelist=[x]
			postlist=[y, z, w]
		else:
			prelist=[]
			postlist=[]
		return [prelist, postlist]

	def setCharTree(self, ch):
		"""設定某一個字符所包含的部件的碼"""

		if not ch.isToSetTree():
			# 如果有值，代表事先指定或之前設定過。
			return

		prelist, postlist=self.getCJPrePostList(ch)
		complist=[prelist, postlist]

		for tmpch in prelist+postlist:
			self.setCharTree(tmpch)

		ch.setCJByComps(prelist, postlist)

class Array(NoneIM):
	"行列輸入法"

	class ARCharInfo(NoneIM.CharInfo):
		def __init__(self, charname, parseans, prop):
			NoneIM.CharInfo.__init__(self, charname, parseans, prop)
			self._ar_incode=None
			if len(prop)>=1:
				self.setARProp(prop[0])
			self.noneFlag=False
			self.setedFlag=False

		def setARProp(self, ar_incode):
			if ar_incode=='XXXX':
				self._ar_incode=None
			else:
				self._ar_incode=ar_incode

		def getARProp(self):
			return self._ar_incode

		def setByComps(self, complist):
			arlist=list(map(lambda c: c.getARProp(), complist))
			if complist and all(arlist):
				cat="".join(arlist)
				ar=cat[:3]+cat[-1] if len(cat)>4 else cat
				self.setARProp(ar)

		@property
		def ar(self):
			return self._ar_incode

		@property
		def isSeted(self):
			return bool(self._ar_incode)

	def __init__(self):
		self.keyMaps=[
			['a', '1-',],
			['b', '5v',],
			['c', '3v',],
			['d', '3-',],
			['e', '3^',],
			['f', '4-',],
			['g', '5-',],
			['h', '6-',],
			['i', '8^',],
			['j', '7-',],
			['k', '8-',],
			['l', '9-',],
			['m', '7v',],
			['n', '6v',],
			['o', '9^',],
			['p', '0^',],
			['q', '1^',],
			['r', '4^',],
			['s', '2-',],
			['t', '5^',],
			['u', '7^',],
			['v', '4v',],
			['w', '2^',],
			['x', '2v',],
			['y', '6^',],
			['z', '1v',],
			['.', '9v',],
			['/', '0v',],
			[';', '0-',],
			[',', '8v',],
			]
		self.nameDict={
				'cn':'行列',
				'tw':'行列',
				'hk':'行列',
				'en':'Array',
				}
		self.iconfile="Array.png"
		self.maxkeylength=4

	def getCode(self, ch):
		if ch.ar:
			return ch.ar

class DaYi(NoneIM):
	"大易輸入法"

	class DYCharInfo(NoneIM.CharInfo):
		def __init__(self, charname, parseans, prop):
			NoneIM.CharInfo.__init__(self, charname, parseans, prop)
			self._dy_incode=None
			if len(prop)>=1:
				self.setDYProp(prop[0])
			self.noneFlag=False
			self.setedFlag=False

		def setDYProp(self, dy_incode):
			if dy_incode=='XXXX':
				self._dy_incode=None
			else:
				self._dy_incode=dy_incode

		def getDYProp(self):
			return self._dy_incode

		def setByComps(self, complist):
			dylist=list(map(lambda c: c.getDYProp(), complist))
			if complist and all(dylist):
				cat="".join(dylist)
				dy=cat[:3]+cat[-1] if len(cat)>4 else cat
				self.setDYProp(dy)

		@property
		def dy(self):
			return self._dy_incode

		@property
		def isSeted(self):
			return bool(self._dy_incode)

	def __init__(self):
		self.keyMaps=[
			[',', '力',],
			['.', '點',],
			['/', '竹',],
			['0', '金',],
			['1', '言',],
			['2', '牛',],
			['3', '目',],
			['4', '四',],
			['5', '王',],
			['6', '門',],
			['7', '田',],
			['8', '米',],
			['9', '足',],
			[';', '虫',],
			['A', '人',],
			['B', '馬',],
			['C', '七',],
			['D', '日',],
			['E', '一',],
			['F', '土',],
			['G', '手',],
			['H', '鳥',],
			['I', '木',],
			['J', '月',],
			['K', '立',],
			['L', '女',],
			['M', '雨',],
			['N', '魚',],
			['O', '口',],
			['P', '耳',],
			['Q', '石',],
			['R', '工',],
			['S', '革',],
			['T', '糸',],
			['U', '艸',],
			['V', '禾',],
			['W', '山',],
			['X', '水',],
			['Y', '火',],
			['Z', '心',],
			]
		self.nameDict={
				'cn':'大易',
				'tw':'大易',
				'hk':'大易',
				'en':'DaYi',
				}
		self.iconfile="DaYi.png"
		self.maxkeylength=4

	def getCode(self, ch):
		if ch.dy:
			return ch.dy

class Boshiamy(NoneIM):
	"嘸蝦米輸入法"

	class BSCharInfo(NoneIM.CharInfo):
		def __init__(self, charname, parseans, prop):
			NoneIM.CharInfo.__init__(self, charname, parseans, prop)
			self._bs_incode=None
			self._bs_spcode=None
			if len(prop)>=2:
				self.setBSProp(prop[0], prop[1])
			self.noneFlag=False
			self.setedFlag=False

		def setBSProp(self, bs_incode, bs_spcode):
			if bs_incode=='XXXX' or bs_spcode=='XXXX':
				self._bs_incode=None
				self._bs_spcode=None
			else:
				self._bs_incode=bs_incode
				self._bs_spcode=bs_spcode

		def getBSProp(self):
			return [self._bs_incode, self._bs_spcode]

		def setByComps(self, complist):
			bslist=list(map(lambda c: c.getBSProp()[0], complist))
			if complist and all(bslist):
				cat="".join(bslist)
				bs_incode=(cat[:3]+cat[-1]) if len(cat)>4 else cat
				bs_spcode=complist[-1].getBSProp()[1]
				self.setBSProp(bs_incode, bs_spcode)

		@property
		def bs(self):
			if self._bs_incode==None or self._bs_spcode==None:
				return None
			if len(self._bs_incode)<3:
				return self._bs_incode+self._bs_spcode
			else:
				return self._bs_incode

		@property
		def isSeted(self):
			return bool(self._bs_incode)

	def __init__(self):
		self.keyMaps=[
			['a', 'Ａ',],
			['b', 'Ｂ',],
			['c', 'Ｃ',],
			['d', 'Ｄ',],
			['e', 'Ｅ',],
			['f', 'Ｆ',],
			['g', 'Ｇ',],
			['h', 'Ｈ',],
			['i', 'Ｉ',],
			['j', 'Ｊ',],
			['k', 'Ｋ',],
			['l', 'Ｌ',],
			['m', 'Ｍ',],
			['n', 'Ｎ',],
			['o', 'Ｏ',],
			['p', 'Ｐ',],
			['q', 'Ｑ',],
			['r', 'Ｒ',],
			['s', 'Ｓ',],
			['t', 'Ｔ',],
			['u', 'Ｕ',],
			['v', 'Ｖ',],
			['w', 'Ｗ',],
			['x', 'Ｘ',],
			['y', 'Ｙ',],
			['z', 'Ｚ',],
			]
		self.nameDict={
				'cn':'呒蝦米',
				'tw':'嘸蝦米',
				'hk':'嘸蝦米',
				'en':'Boshiamy',
				}
		self.iconfile="Boshiamy.png"
		self.maxkeylength=4

	def getCode(self, ch):
		if ch.bs:
			return ch.bs

class ZhengMa(NoneIM):
	"鄭碼輸入法"

	class ZMCharInfo(NoneIM.CharInfo):
		def __init__(self, charname, parseans, prop):
			NoneIM.CharInfo.__init__(self, charname, parseans, prop)
			self._zm_rtlist=[]
			self._zm_incode=None
			self._zm_tpcode=None
			if len(prop)>=1:
				str_rtlist=prop[0]
				if str_rtlist=='XXXX':
					self.setZMProp([])
				else:
					self.setZMProp(str_rtlist.split(','))
			self.noneFlag=False
			self.setedFlag=False

		def setZMProp(self, zm_rtlist):
			self._zm_rtlist=zm_rtlist

		def getZMProp(self):
			return self._zm_rtlist

		def setByComps(self, complist):
			if all(complist):
				rtlist=sum(map(lambda c: c.getZMProp(), complist), [])
				if complist and all(rtlist):
					rtlist=rtlist if len(rtlist)<=4 else rtlist[:2]+rtlist[-2:]
					self.setZMProp(rtlist)

		@property
		def zm(self):
			ans=''
			tmp_rtlist=self._zm_rtlist
			if len(tmp_rtlist)==0:
				return None
			elif len(tmp_rtlist)==1:
				ans=self._zm_rtlist[0]
			elif len(tmp_rtlist)==2:
				if len(tmp_rtlist[0])==1 and len(tmp_rtlist[1])==1:
					ans=''.join(self._zm_rtlist[0:2])
					ans=self._zm_rtlist[0][0]+self._zm_rtlist[-1][0]+'vv'
				else:
					ans=(self._zm_rtlist[0]+self._zm_rtlist[-1])[:4]
			elif len(tmp_rtlist)==3:
				if len(tmp_rtlist[0])==1:
					ans=self._zm_rtlist[0][0]+self._zm_rtlist[1][0]+self._zm_rtlist[-1][0:2]
				elif len(tmp_rtlist[0])==2:
					ans=self._zm_rtlist[0][0:2]+self._zm_rtlist[-2][0]+self._zm_rtlist[-1][0]
				elif len(tmp_rtlist[0])==3:
					ans=self._zm_rtlist[0][0:3]+self._zm_rtlist[-1][0]
			elif len(tmp_rtlist)==4:
				if len(tmp_rtlist[0])==1:
					ans=self._zm_rtlist[0][0]+self._zm_rtlist[1][0]+self._zm_rtlist[-2][0]+self._zm_rtlist[-1][0]
				elif len(tmp_rtlist[0])==2:
					ans=self._zm_rtlist[0][0:2]+self._zm_rtlist[-2][0]+self._zm_rtlist[-1][0]
				elif len(tmp_rtlist[0])==3:
					ans=self._zm_rtlist[0][0:3]+self._zm_rtlist[-1][0]
			else:
				ans=''
			return ans

		@property
		def isSeted(self):
			return bool(self._zm_rtlist)

	def __init__(self):
		self.keyMaps=[
			['a', 'Ａ',],
			['b', 'Ｂ',],
			['c', 'Ｃ',],
			['d', 'Ｄ',],
			['e', 'Ｅ',],
			['f', 'Ｆ',],
			['g', 'Ｇ',],
			['h', 'Ｈ',],
			['i', 'Ｉ',],
			['j', 'Ｊ',],
			['k', 'Ｋ',],
			['l', 'Ｌ',],
			['m', 'Ｍ',],
			['n', 'Ｎ',],
			['o', 'Ｏ',],
			['p', 'Ｐ',],
			['q', 'Ｑ',],
			['r', 'Ｒ',],
			['s', 'Ｓ',],
			['t', 'Ｔ',],
			['u', 'Ｕ',],
			['v', 'Ｖ',],
			['w', 'Ｗ',],
			['x', 'Ｘ',],
			['y', 'Ｙ',],
			['z', 'Ｚ',],
			]
		self.nameDict={
				'cn':'郑码',
				'tw':'鄭碼',
				'hk':'鄭碼',
				'nn':'Boshiamy',
				}
		self.iconfile="ZhengMa.png"
		self.maxkeylength=4

	def getCode(self, ch):
		if ch.zm:
			return ch.zm

if __name__=='__main__':
	pass

