# from pwdlib import PasswordHash

# password_hash = PasswordHash.recommended()


# def hash_password(password: str) -> str:
#     return password_hash.hash(password)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return password_hash.verify(plain_password, hashed_password)


from pwdlib import PasswordHash
from jose import jwt

password_hash = PasswordHash.recommended()

SECRET_KEY = "legal-contract-secret-key-2026"
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt