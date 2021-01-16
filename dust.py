import serial, struct, os, time
from datetime import datetime, time as t

PORT = '/dev/ttyUSB0'
UNPACK_PAT = '<ccHHHcc'

with serial.Serial(PORT, 9600, bytesize=8, parity='N', stopbits=1) as ser:
	while True:
		data = ser.read(10)
		unpack = struct.unpack('<ccHHHcc', data)

		now = datetime.now()
		nowTime = now.time()
		dayStr = now.strftime("%Y_%m_%d")
		filename= '/var/www/html/data/' + dayStr + '.txt'

		pm25 = unpack[2] / 10.0
		pm10 = unpack[3] / 10.0
		values = "{}: PM 2.5 = {} PM 10 = {}".format(now.strftime("%Y-%m-%d %H:%M:%S"), pm25, pm10)

		if os.path.exists(filename):
			append_write = 'a'
		else:
			append_write = 'w'

		file = open(filename, append_write)
		file.write(values + '\n')
		file.close()

        #Check values every 15 sec., at night every 60 sec.
		if nowTime >= t(23,30) or nowTime <= t(5,00):
			time.sleep(60)
		else:
			time.sleep(15)
