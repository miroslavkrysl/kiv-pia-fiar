from typing import Optional

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


class TokenService:
    """
    Creating and verifying of time-based signed tokens.
    """

    def __init__(self, key: str):
        self.serializer = URLSafeTimedSerializer(key)

    def make_token(self, data: object) -> str:
        """
        Create a token by serializing and signing given data together
        with current timestamp.
        :param data: Any object that will be serialized into the token.
        :return: String with serialized token.
        """
        return self.serializer.dumps(data)

    def decode_token(self, token: str, max_age: int) -> Optional[object]:
        """
        Deserialize data from signed timed token and check expiration time.
        :param max_age: Max age of the token in seconds.
        :param token: The timed token.
        :return: Deserialized data or None if token is invalid or expired.
        """
        try:
            return self.serializer.loads(token, max_age)
        except (BadSignature, SignatureExpired) as e:
            return None
