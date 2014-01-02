import requests
import settings


class ChickenAPI(object):

    base_url = settings.API_BASE_URL

    @classmethod
    def add_data(cls, data_string):
        response = requests.put(ChickenAPI.base_url + '/add_data', data_string)
        return response