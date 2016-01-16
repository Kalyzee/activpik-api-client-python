import unittest
from activpik_client import Oauth2ClientCredentialsAuth, ActivpikClient

from mock import patch, Mock

from requests.models import Request, Response

class Oauth2ClientCredentialsAuthTest(unittest.TestCase):

    def setUp(self):
        self._access_token_url = "http://super-domaine.com/access_token"
        self._client_id = "super_client_id"
        self._client_secret = "super_client_secret"
        self._oauth2_client = Oauth2ClientCredentialsAuth(self._access_token_url, self._client_id, self._client_secret)


    @patch('requests.post')
    def test_get_access_token(self, mock_request):    
        mock_request.return_value = Mock()
        mock_request.return_value.status_code = 200
        mock_request.return_value.json = Mock()
        mock_request.return_value.json.return_value = {"access_token" : "2222"}
        r = Request()
        self._oauth2_client.__call__(r)
        self.assertEquals("OAuth 2222", r.headers["Authorization"])
        mock_request.assert_called_once_with(self._access_token_url, data={"grant_type": "client_credentials", "client_id": self._client_id, "client_secret": self._client_secret})
        
    @patch('requests.post')
    def test_get_access_token_error(self, mock_request):
        mock_request.return_value = Mock()
        mock_request.return_value.status_code = 400
        r = Request()
        self.assertRaises(Exception, lambda : self._oauth2_client.__call__(r))        
       

    @patch('requests.post')
    def test_get_access_token_error(self, mock_request):
        mock_request.return_value = Mock()
        mock_request.return_value.status_code = 200
        mock_request.return_value.json = Mock()
        mock_request.return_value.json.return_value = {"access_token" : "2222"}
        r = Request()
        self._oauth2_client.__call__(r)
        self.assertEquals("OAuth 2222", r.headers["Authorization"])
        self._oauth2_client.__call__(r)
        self.assertEquals("OAuth 2222", r.headers["Authorization"])
        mock_request.assert_called_once_with(self._access_token_url, data={"grant_type": "client_credentials", "client_id": self._client_id, "client_secret": self._client_secret})
        


class ActivpikClientTest(unittest.TestCase):

    def setUp(self):
        self._client = ActivpikClient("super_client_id", "super_client_secret")

    @patch('requests.post')
    def test_add_media(self, mock_request_post):
        raise NotImplementedError()

    def test_get_media(self):
        raise NotImplementedError()

    def test_get_medias(self):
        raise NotImplementedError()

    def test_transcribe_media(self):
        raise NotImplementedError()

    def test_get_transcription_status(self):
        raise NotImplementedError()

    def test_get_timecoded_named_entities_for_media(self):
        raise NotImplementedError()

    def test_get_timecoded_named_entities(self):
        raise NotImplementedError()

if __name__ == '__main__':
    unittest.main()
