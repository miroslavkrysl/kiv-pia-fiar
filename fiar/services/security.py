from passlib.hash import bcrypt


class HashService:

    @staticmethod
    def hash_secret(secret: str) -> str:
        return bcrypt.hash(secret)

    @staticmethod
    def verify_secret(secret: str, hash: str) -> bool:
        return bcrypt.verify(secret, hash)
