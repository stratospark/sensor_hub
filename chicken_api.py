import requests


class ChickenAPI(object):

    base_url = 'http://localhost:8000'

    @classmethod
    def add_data(cls, data_string):
        response = requests.put(ChickenAPI.base_url + '/add_data', data_string)
        return response