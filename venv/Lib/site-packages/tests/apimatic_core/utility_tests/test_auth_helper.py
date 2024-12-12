from apimatic_core.utilities.auth_helper import AuthHelper


class TestAuthHelper:

    def test_base64_encoded_none_value(self):
        actual_base64_encoded_value = AuthHelper.get_base64_encoded_value()
        expected_base64_encoded_value = None
        assert actual_base64_encoded_value == expected_base64_encoded_value

    def test_base64_encoded_provided_none_values(self):
        actual_base64_encoded_value = AuthHelper.get_base64_encoded_value(None, None)
        expected_base64_encoded_value = None
        assert actual_base64_encoded_value == expected_base64_encoded_value

        actual_base64_encoded_value = AuthHelper.get_base64_encoded_value('test_username', None)
        expected_base64_encoded_value = None
        assert actual_base64_encoded_value == expected_base64_encoded_value

    def test_base64_encoded_value(self):
        actual_base64_encoded_value = AuthHelper.get_base64_encoded_value('test_username', 'test_password')
        expected_base64_encoded_value = 'dGVzdF91c2VybmFtZTp0ZXN0X3Bhc3N3b3Jk'
        assert actual_base64_encoded_value == expected_base64_encoded_value

    def test_token_expiry(self):
        current_utc_timestamp = AuthHelper.get_current_utc_timestamp()
        actual_token_expiry_value = AuthHelper.get_token_expiry(current_utc_timestamp, 5)
        expected_token_expiry_value = current_utc_timestamp + int(5)
        assert actual_token_expiry_value == expected_token_expiry_value

    def test_token_is_expired(self):
        past_timestamp = AuthHelper.get_current_utc_timestamp() - 5
        actual_token_expired = AuthHelper.is_token_expired(past_timestamp)
        expected_token_expired = True
        assert actual_token_expired == expected_token_expired

    def test_token_is_expired_with_clock_skew(self):
        past_timestamp = AuthHelper.get_current_utc_timestamp() + 5
        actual_token_expired = AuthHelper.is_token_expired(past_timestamp, 10)
        expected_token_expired = True
        assert actual_token_expired == expected_token_expired

    def test_token_is_not_expired_with_clock_skew(self):
        past_timestamp = AuthHelper.get_current_utc_timestamp() + 5
        actual_token_expired = AuthHelper.is_token_expired(past_timestamp, 3)
        expected_token_expired = False
        assert actual_token_expired == expected_token_expired

        past_timestamp = AuthHelper.get_current_utc_timestamp() + 5
        actual_token_expired = AuthHelper.is_token_expired(past_timestamp, 5)
        expected_token_expired = False
        assert actual_token_expired == expected_token_expired

    def test_token_is_not_expired(self):
        past_timestamp = AuthHelper.get_current_utc_timestamp() + 5
        actual_token_expired = AuthHelper.is_token_expired(past_timestamp)
        expected_token_expired = False
        assert actual_token_expired == expected_token_expired



