from main import create_token, verify_signature
import pytest
from unittest import mock as mock

class TestChallenge4:
    token = b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsYW5ndWFnZSI6IlB5dGhvbiJ9.sM_VQuKZe_VTlqfS3FlAm8XLFhgvQQLk2kkRTpiXq7M'
    secret = "acelera"

    def test_create_token(self):
        assert create_token({"language": "Python"}, self.secret) == self.token

    def test_valid_signature(self):
        decoded = verify_signature(self.token, self.secret)
        assert decoded.get('language') == 'Python'

    def test_invalid_secret(self):
        decoded = verify_signature(self.token, "acelera123")
        assert decoded.get('error') == 2

    @pytest.mark.parametrize(
        "token",
        ['testasd']
    )
    def test_verify_signature_fail_by_token(self, token):
        decoded = verify_signature(token, self.secret)
        assert decoded.get('error') == 2

    @pytest.mark.parametrize(
        "token",
        [b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsYW5ndWFnZSI6IlJ1YnkifQ.IhyzOvcnUI0vJXPPIG6TkcG3kgN-sCfU5n-XG8jTzRU']
    )
    def test_verify_signature_fail_by_value(self, token):
        decoded = verify_signature(token, self.secret)
        assert decoded.get('language') != 'Python'

    @mock.patch('main.jwt')
    def test_exception(self, mock_jwt):
        mock_jwt.decode.side_effect=Exception
        
        with pytest.raises(Exception):
            verify_signature(self.token, self.secret)
        
