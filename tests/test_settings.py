from mock import patch
import settings


class TestSettings(object):

    def test_pi_environment(self):
        with patch.dict('settings.os.environ', {'USER': 'pi'}):
            settings.API_BASE_URL.find('localhost') == -1

    def test_local_environment(self):
        with patch.dict('settings.os.environ', {'USER': 'notpi'}):
            settings.API_BASE_URL.find('localhost') >= 0
