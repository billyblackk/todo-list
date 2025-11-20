from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


# Used when creating a new user
def get_password_hash(password: str) -> str:
    if isinstance(password, bytes):
        password = password.decode("utf-8")
    return pwd_context.hash(password)


# Used when logging in
def verify_password(plain_password: str, hashed_password: str) -> bool:
    if isinstance(plain_password, bytes):
        plain_password = plain_password.decode("utf-8")
    return pwd_context.verify(plain_password, hashed_password)
