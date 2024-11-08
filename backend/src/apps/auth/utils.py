import random
from datetime import datetime, timedelta
import jwt

from src.apps.auth.constants import (
    SECRET_KEY, ALGORITHM
)



def generateOtp() -> str:
    otp = ""
    for i in range(7):
        otp += str(random.randint(1, 9))
    return otp