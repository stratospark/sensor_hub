from mock import patch
from chicken_api import ChickenAPI


class TestChickenAPI():

    @patch('chicken_api.requests')
    def test_add_data(self, mock_requests):
        mock_requests.put.return_value.status_code = 200
        mock_requests.put.return_value.text = 'OK'

        data_string = '2013-11-25 11:09:34,-91,D1,M1'
        response = ChickenAPI.add_data(data_string)

        mock_requests.put.assert_called_with(ChickenAPI.base_url + '/add_data', data_string)
        assert response.status_code == 200
        assert response.text == 'OK'