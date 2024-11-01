import random

def generateOtp():
    otp = ""
    for i in range(7):
        otp += str(random.randint(1, 9))
    return otp