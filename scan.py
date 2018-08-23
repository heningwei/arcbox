from pyb import UART
import time

class Scan():

	def __init__(self):
		self.scan = UART(3, 9600, read_buf_len=100)
	
	def count(self):
		return self.scan.any()
	
	def receive(self):
		time.sleep_ms(100)
		count = self.count()
		data = self.scan.read(count).decode()
		return {'code':data}
