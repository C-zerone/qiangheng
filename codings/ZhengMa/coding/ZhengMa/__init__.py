from coding.Base import CodingType

from .ZhengMa import ZhengMaInfo as CodingInfo
from .ZhengMa import ZMCodeInfoEncoder as CodeInfoEncoder
from .ZhengMa import ZMRadixParser as CodingRadixParser

codingType = CodingType.Input
codingMethodName = "zm"
codingMethodDir = "gen/qhdata/{method}/".format(method=codingMethodName)
CodingComponentFileList = [
	codingMethodDir + 'style.yaml',
]
CodingSubstituteFileList = [
	codingMethodDir + 'substitute.yaml',
]
CodingRadixFileList = [
	codingMethodDir + 'radix/CJK.yaml',
	codingMethodDir + 'radix/CJK-A.yaml',
	codingMethodDir + 'radix/adjust.yaml'
]

if __name__=='__main__':
	pass

