import _thread
import time
import json
from pyb import Timer
import os

from adc import Adc
from lcd import Lcd
from scan import Scan
from outctl import Outctl
from networks import Network

adc = Adc()
lcd = Lcd()
scan = Scan()
outctl = Outctl()
network = Network()

up_state_cnt = 0 #上位机状态计数器
file_flag = 0 #是否写入文件
adc_freq = 1000 #adc采样频率
voltage_b = 0
current_b = 0
warnvalue = 10
warntime = 20
stopvalue = 20
stoptime = 20
time_now = ''


def up_state(tt):
	global up_state_cnt, file_flag
	state = 0
	while True:
		time.sleep(120)
		if state == 0:
			up_state_cnt += 1
			if up_state_cnt > 10:
				up_state_cnt = 11
				state = 1
		elif state == 1:
			file_flag = 1
			if up_state_cnt == 0:
				file_flag = 0
				state = 0

def scan_check(tt):
	lock = _thread.allocate_lock()
	while True:
		if scan.count():
			time.sleep_ms(200)
			data = scan.receive()
			lock.acquire()
			network.send(data)
			lock.release()
		time.sleep(1)

def adc_process(tt):
	lock = _thread.allocate_lock()
	if  'data.json' in os.listdir():
		state_file = 2
	else:
		state_file = 0
	warning = 0
	def warn_flag(t):
		nonlocal warning
		warning = 1
	stoping = 0
	def stop_flag(t):
		nonlocal stoping
		stoping = 1
	state_warn = 0
	state_stop = 0
	while True:
		v,c,t = adc.read_ad()
		lock.acquire()
		lcd.send_real(v,c,t)
		lock.release()
		data = {'voltage': v, 'current': c, 'temp': t}
		if state_file == 0:
			lock.acquire()
			outctl.high('led2')
			network.send(data)
			lock.release()
			outctl.low('led2')
			if file_flag == 1:
				state_file = 1
				f = open('/sd/data.json', 'w')
		elif state_file == 1:
			data.update({'time':time_now})
			f.write(json.dumps(data)+'\n')
			f.flush()
			if file_flag == 0:
				f.close()
				state_file = 2
		elif state_file == 2:
			lock.acquire()
			outctl.high('led2')
			f = open('/sd/data.json', 'r')
			try:
				while True:
					if not f.readline():
						break
					data = f.readline()
					data = eval(data.strip())
					network.send(data)
				#for line in f.readlines():
				#	data = eval(line.strip())
				#	network.send(data)
			except:
				pass
			f.close()
			outctl.low('led2')
			os.remove('/sd/data.json')
			lock.release()
			state_file = 0
		#报警处理
		if state_warn == 0:
			if float(v) > voltage_b*(1+warnvalue/100) or float(c) > current_b*(1+warnvalue/100):
				tim1 = Timer(1, freq=(1/warntime), callback=warn_flag)
				state_warn = 1
		elif state_warn == 1:
			if float(v) < voltage_b*(1+warnvalue/100) and float(c) < current_b*(1+warnvalue/100):
				tim1.deinit()
				state_warn = 0
			elif warning == 1:
				outctl.high('alarm')
				state_warn = 2
		elif state_warn == 2:
			if float(v) < voltage_b*(1+warnvalue/100) and float(c) < current_b*(1+warnvalue/100):
				tim1.deinit()
				state_warn = 0
				warning = 0
				outctl.low('alarm')
		#停机处理
		if state_stop == 0:
			if float(v) > voltage_b*(1+stopvalue/100) or float(c) > current_b*(1+stopvalue/100):
				tim2 = Timer(2, freq=(1/stoptime), callback=stop_flag)
				state_stop = 1
		elif state_stop == 1:
			if float(v) < voltage_b*(1+stopvalue/100) and float(c) < current_b*(1+stopvalue/100):
				tim2.deinit()
				state_stop = 0
			elif stoping == 1:
				outctl.high('relay')
				state_stop = 2
		elif state_stop == 2:
			#if float(v) < voltage_b*(1+stopvalue/100):
			#	tim2.deinit()
			#	state_stop = 0
			#	stoping = 0
			pass#停止关机
		time.sleep_ms(int(1000/adc_freq))

def up_process(tt):
	global up_state_cnt, adc_freq, voltage_b, current_b, warnvalue, warntime, stopvalue, stoptime, time_now
	lock = _thread.allocate_lock()
	while True:
		if network.count():
			try:
				data = network.receive()
				if 'voltage' in data:
					voltage_b = float(data['voltage'])
					current_b = float(data['current'])
					warnvalue = float(data['warnvalue'])
					warntime = float(data['warntime'])
					stopvalue = float(data['stopvalue'])
					stoptime = float(data['stoptime'])
					vv = data['voltage']
					cc = data['current']
					lock.acquire()
					lcd.send_stand(vv, cc)
					lock.release()
					up_state_cnt = 0
				elif 'warnvalue' in data:
					warnvalue = float(data['warnvalue'])
					warntime = float(data['warntime'])
					stopvalue = float(data['stopvalue'])
					stoptime = float(data['stoptime'])
					up_state_cnt = 0
				elif 'time' in data:
					time_now = data['time']
					up_state_cnt = 0
				elif 'freq' in data:
					adc_freq = float(data['freq'])
					up_state_cnt = 0
			except:
				pass
		time.sleep_ms(500)

def main():
	global voltage_b, current_b, warnvalue, warntime, stopvalue, stoptime
	outctl.high('led1')
	while True:
		if scan.count():
			data = scan.receive()
			network.send(data)
			break
	while True:
		if network.count():
			try:
				data = network.receive()
				voltage_b = float(data['voltage'])
				current_b = float(data['current'])
				warnvalue = float(data['warnvalue'])
				warntime = float(data['warntime'])
				stopvalue = float(data['stopvalue'])
				stoptime = float(data['stoptime'])
				vv = data['voltage']
				cc = data['current']
				lcd.send_stand(vv, cc)
				break
			except:
				pass
	#开始多线程
	_thread.start_new_thread(up_state, (1,))
	_thread.start_new_thread(scan_check, (1,))
	_thread.start_new_thread(adc_process, (1,))
	_thread.start_new_thread(up_process, (1,))

main()
