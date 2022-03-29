import time
import calendar
from passlib.context import CryptContext
from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException
import secrets


class Hash():
    def bcrypt(password: str):
        return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)

    def verify(plain_password: str, hashed_password: str):
        return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(plain_password, hashed_password)


def email_validation(email, exc: bool = True):
    try:
        valid = validate_email(email)
        email = valid.email
        return email
    except EmailNotValidError as e:
        if exc:
            raise HTTPException(status_code=400, detail=str(e))
        print("Email not validated!")


def get_timestamp():
    localtime = time.localtime()
    timestamp = calendar.timegm(localtime)
    return timestamp


def generate_filename(extension: str, counter: int, timestamp: str = get_timestamp(), secret_token: str = None):
    # token_name, variable for generated random string using secrets module (ex: 9f94dfb1264e165bafb0d854d6ddac.jpg)
    if secret_token:
        token_name = f"{secret_token}_{timestamp}_{counter}.{extension}"
    else:
        token_name = f"{secrets.token_hex(10)}_{timestamp}_{counter}.{extension}"
    return token_name
