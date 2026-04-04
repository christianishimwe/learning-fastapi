from passlib.context import CryptContext
pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_content.hash(password)

# takes in a plain password and a hashed password and returns true if they match, false otherwise


def verify_password(plain_password, hashed_password):
    return pwd_content.verify(plain_password, hashed_password)
