import serial
import time
from xbee import ZigBee
import logging
from chicken_api import ChickenAPI


logger = logging.getLogger(__name__)


class XbeeAPIWatcher(object):
    def __init__(self):
        self.FILE = open('chickens.txt', 'a')
        self.ser = None
        self.xbee = None
        self.last_message = None
        self.last_signal = None

        self._setup_serial()

    def _setup_serial(self):
        self.ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=0)
        self.xbee = ZigBee(self.ser, escaped=True)

    def _process_message(self, message):
        if message['id'] == 'rx':
            self.last_message = message
            logger.info(time.strftime('%Y-%m-%d %H:%M:%S'))
            self.xbee.send('at', command='DB')
            # wait for signal strength response
        elif message['id'] == 'at_response' and message['command'] == 'DB':
            logger.info('Signal Strength: -%ddBm' % ord(message['parameter']))
            self.last_signal = ord(message['parameter'])
            data_string = '%s,%s,%s' % (time.strftime('%Y-%m-%d %H:%M:%S'),
                                            '-%d' % self.last_signal,
                                            self.last_message['rf_data'].strip('\r\n'))
            self.FILE.write('%s\r\n' % data_string)
            self.FILE.flush()
            ChickenAPI.add_data(data_string)


    def start(self):
        while True:
            try:
                response = self.xbee.wait_read_frame()
                self._process_message(response)
            except KeyboardInterrupt:
                break

    def stop(self):
        self.xbee.halt()
        self.ser.close()


if __name__ == '__main__':
    watcher = XbeeAPIWatcher()
    watcher.start()
    # last_signal = 0
    # last_message = None
    #
    # def print_data(data):
    #     global last_signal
    #     global last_message
    #     if data['id'] == 'rx':
    #         last_message = data
    #         print time.strftime('%Y-%m-%d %H:%M:%S')
    #         xbee.send('at', command='DB')
    #     elif data['id'] == 'at_response' and data['command'] == 'DB':
    #         print "Signal Strength:"
    #         print "-%ddBm" % ord(data['parameter'])
    #         last_signal = ord(data['parameter'])
    #         FILE.write('%s,%s,%s\r\n' % (
    #         time.strftime('%Y-%m-%d %H:%M:%S'), '-%d' % (last_signal), last_message['rf_data'].strip('\r\n')))
    #         FILE.flush()
    #
    #     print data
    #
    # FILE = open('chickens.txt', 'a')
    #
    # ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=0)
    # xbee = ZigBee(ser, escaped=True, callback=print_data)
    #
    # while True:
    #     try:
    #         time.sleep(0.001)
    #     except KeyboardInterrupt:
    #         break
    #
    # xbee.halt()
    # ser.close()
