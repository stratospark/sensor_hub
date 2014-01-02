import serial
import time
from xbee import ZigBee

last_signal = 0
last_message = None

def print_data(data):
  global last_signal
  global last_message
  if data['id'] == 'rx':
    last_message = data
    print time.strftime('%Y-%m-%d %H:%M:%S')
    xbee.send('at', command='DB')
  elif data['id'] == 'at_response' and data['command'] == 'DB':
    print "Signal Strength:"
    print "-%ddBm" % ord(data['parameter'])
    last_signal = ord(data['parameter'])
    FILE.write('%s,%s,%s\r\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), '-%d'%(last_signal), last_message['rf_data'].strip('\r\n')))
    FILE.flush()

  print data

FILE = open('chickens.txt', 'a')

ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=0)
xbee = ZigBee(ser, escaped=True, callback=print_data)

while True:
  try:
    time.sleep(0.001)
  except KeyboardInterrupt:
    break

xbee.halt()
ser.close()

