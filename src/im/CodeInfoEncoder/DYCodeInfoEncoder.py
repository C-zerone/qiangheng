from gear.CodeInfoEncoder import CodeInfoEncoder

class DYCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def setByComps(self, codeInfo, operator, codeInfoList):
		dylist=list(map(lambda c: c.getDYProp(), codeInfoList))
		if codeInfoList and all(dylist):
			cat="".join(dylist)
			dy=cat[:3]+cat[-1] if len(cat)>4 else cat
			codeInfo.setDYProp(dy)

