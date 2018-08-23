from pyb import UART
import json
import time

class Network():

	def __init__(self):
		self.network = UART(6, 115200, read_buf_len=200)
	
	def count(self):
		return self.network.any()
	
	def receive(self):
		time.sleep_ms(100)
		count = self.count()
		data = self.network.read(count).decode()
		data = data.strip()
		return eval(data)
	
	def send(self,data):
		ss = json.dumps(data)
		self.network.write(ss)
