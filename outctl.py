from pyb import Pin

class Outctl():

	def __init__(self):
		self.relay = Pin('Y7', Pin.OUT_PP)
		self.alarm = Pin('Y8', Pin.OUT_PP)
		self.led1 = Pin('Y3', Pin.OUT_PP)
		self.led2 = Pin('Y4', Pin.OUT_PP)
	
	def high(self,str):
		if str == 'relay':
			self.relay.high()
		elif str == 'alarm':
			self.alarm.high()
		elif str == 'led1':
			self.led1.high()
		elif str == 'led2':
			self.led2.high()
		else:
			pass
	
	def low(self,str):
		if str == 'relay':
			self.relay.low()
		elif str == 'alarm':
			self.alarm.low()
		elif str == 'led1':
			self.led1.low()
		elif str == 'led2':
			self.led2.low()
		else:
			pass
