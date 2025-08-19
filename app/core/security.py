import string
from passlib.context import CryptContext
from sqlalchemy.util import deprecated
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def generate_random_password(size: int) -> str:

    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))