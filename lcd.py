from pyb import UART

class Lcd():

	def __init__(self):
		self.lcd = UART(1, 9600)
	
	def send_real(self, v, c, t):
		if self.lcd.any():
			self.lcd.read(self.lcd.any())
		v = v.split('.')[0]
		c = c.split('.')[0]
		t = t.split('.')[0]
		self.lcd.write('main.v.val=%s' % v)
		self.lcd.writechar(255)
		self.lcd.writechar(255)
		self.lcd.writechar(255)
		self.lcd.write('main.c.val=%s' % c)
		self.lcd.writechar(255)
		self.lcd.writechar(255)
		self.lcd.writechar(255)
		self.lcd.write('main.t.val=%s' % t)
		self.lcd.writechar(255)
		self.lcd.writechar(255)
		self.lcd.writechar(255)
	
	def send_stand(self, vv, cc):
		if self.lcd.any():
			self.lcd.read(self.lcd.any())
		vv = vv.split('.')[0]
		cc = cc.split('.')[0]
		self.lcd.write('main.vv.val=%s' % vv)
		self.lcd.writechar(255)
		self.lcd.writechar(255)
		self.lcd.writechar(255)
		self.lcd.write('main.cc.val=%s' % cc)
		self.lcd.writechar(255)
		self.lcd.writechar(255)
		self.lcd.writechar(255)
