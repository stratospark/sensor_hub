from mock import patch
import pytest
from requests.exceptions import ConnectionError
from xbee_api_watcher import XbeeAPIWatcher


class TestXbeeAPIWatcher(object):

    @patch('__builtin__.open')
    @patch('xbee_api_watcher.serial')
    @patch('xbee_api_watcher.ZigBee')
    def setup(self, mock_zigbee, mock_serial, mock_open):
        self.mock_open = mock_open
        self.mock_serial = mock_serial
        self.mock_zigbee = mock_zigbee
        self.watcher = XbeeAPIWatcher()

    def teardown(self):
        pass

    def test_init(self):
        self.mock_open.assert_called_with('chickens.txt', 'a')
        self.mock_serial.Serial.assert_called_with('/dev/ttyAMA0', 9600, timeout=0)
        self.mock_zigbee.assert_called_with(self.watcher.ser, escaped=True)

    def test_stop(self):
        self.watcher.stop()
        assert self.watcher.xbee.halt.called
        assert self.watcher.ser.close.called

    @pytest.mark.timeout(1)
    @patch.object(XbeeAPIWatcher, '_process_message')
    def test_start(self, mock_process):
        mock_process.side_effect = KeyboardInterrupt()

        self.watcher.start()
        assert self.watcher.xbee.wait_read_frame.called

    def _handle_test_messages(self, mock_time, mock_logger, data_string):
        mock_time.strftime.return_value = '2013-12-01 12:12:12'
        row = {'id': 'rx',
               'parameter': 'blah',
               'rf_data': 'D1,M1'}
        self.watcher._process_message(row)
        assert self.watcher.last_message == row
        mock_logger.info.assert_called_with(mock_time.strftime.return_value)
        self.watcher.xbee.send.assert_called_with('at', command='DB')

        row = {'id': 'at_response',
               'command': 'DB',
               'parameter': 'A'}

        self.watcher._process_message(row)
        mock_logger.info.assert_called_with('Signal Strength: -65dBm')
        self.watcher.FILE.write.assert_called_with('%s\r\n' % data_string)

    @pytest.mark.timeout(1)
    @patch('xbee_api_watcher.logger')
    @patch('xbee_api_watcher.time')
    @patch('xbee_api_watcher.ChickenAPI')
    def test_process_data_rx_and_db(self, mock_chicken_api, mock_time, mock_logger):
        data_string = '2013-12-01 12:12:12,-65,D1,M1'
        self._handle_test_messages(mock_time, mock_logger, data_string)
        mock_chicken_api.add_data.assert_called_with(data_string)

    @pytest.mark.timeout(1)
    @patch('xbee_api_watcher.logger')
    @patch('xbee_api_watcher.time')
    @patch('xbee_api_watcher.ChickenAPI')
    def test_process_data_rx_and_db_and_api_fails(self, mock_chicken_api, mock_time, mock_logger):
        data_string = '2013-12-01 12:12:12,-65,D1,M1'

        error = ConnectionError()
        mock_chicken_api.add_data.side_effect = error

        self._handle_test_messages(mock_time, mock_logger, data_string)
        mock_logger.error.assert_called_with(error)

