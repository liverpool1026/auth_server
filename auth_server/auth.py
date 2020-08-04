import boto3
import pyotp

from collections import namedtuple

from botocore.exceptions import ClientError
from passlib.hash import pbkdf2_sha256

from typing import Optional


UserData = namedtuple("UserData", ["user_email", "user_id", "password", "mfa_key"])


class HawkvineAuthException(Exception):
    pass


def hash_password(pwd: str) -> str:
    return pbkdf2_sha256.hash(pwd)


def get_current_mfa_code(key: str) -> str:
    if len(key) != 16:
        raise HawkvineAuthException()
    else:
        return pyotp.TOTP(key).now()


def verify_mfa_code(key: str, entry: str) -> bool:
    if entry == get_current_mfa_code(key):
        return True
    else:
        return False


def verify_password(password: str, expected: str) -> bool:
    return hash_password(hash_password(password)) == expected


def verify_user(user_email: str, password: str, entry: str) -> Optional[int]:
    user_data = grab_user_data(user_email)

    if user_data:
        if verify_password(password, user_data.password):
            if verify_mfa_code(user_data.mfa_key, entry):
                return user_data.user_id
    return False


def grab_user_data(user_email: str) -> Optional[UserData]:
    aws_context = boto3.resource("dynamodb", region_name="ap-southeast-2")
    try:
        user_data = aws_context.Table("UserData").get_item(
            Key={"user_email": user_email,}
        )
        if "Item" in user_data:
            return UserData(
                user_email=user_email,
                user_id=user_data["Item"]["user_id"],
                password=user_data["Item"]["password"],
                mfa_key=user_data["Item"]["mfa_key"],
            )
    except ClientError as e:
        return None
    return None


