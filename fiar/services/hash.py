from passlib.hash import bcrypt_sha256


class HashService:
    """
    Hashing and verifying.
    """

    def hash(self, secret: str) -> str:
        """
        Create a hash of the given secret.
        :param secret: The secret string.
        :return: Hash string.
        """
        return bcrypt_sha256.hash(secret)

    def verify(self, secret: str, hash: str) -> bool:
        """
        Verify if the hashed secret equals the given hash.
        :param secret: Secret string.
        :param hash: Hash string.
        :return: True if hashes matches, false otherwise.
        """
        return bcrypt_sha256.verify(secret, hash)
