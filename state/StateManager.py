
# 視此模式為獨體模式（Singleton）。

STATE_QUANTITY_NONE=0
STATE_QUANTITY_FIRST=1
STATE_QUANTITY_ALL=2

__state_Quantity=STATE_QUANTITY_NONE
__state_IMModule=None

def __init__(self):
	pass

def setQuantity(quantity):
	global __state_Quantity
	__state_Quantity=quantity

def getQuantity():
	return __state_Quantity

def setIMModule(imModule):
	global __state_IMModule
	__state_IMModule=imModule

def getIMModule():
	return __state_IMModule

