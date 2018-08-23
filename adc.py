from pyb import ADC,Pin
import pyb

class Adc():

	def __init__(self):
		self.adv = ADC(Pin('X11'))
		self.adc = ADC(Pin('X12'))
		self.adt = pyb.ADCAll(12)
	
	def read_ad(self):
		v = self.adv.read()
		c = self.adc.read()
		t = self.adt.read_core_temp()
		v = 100/4096*v
		c = 600/4096*c
		return ('%.2f' % v, '%.2f' % c, '%.2f' % t)
