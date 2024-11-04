from src.apps.auth.utils import generateOtp


def test_generate_one_time_password():
    vcode = generateOtp()
    assert len(vcode) == 7
    assert type(vcode) == str