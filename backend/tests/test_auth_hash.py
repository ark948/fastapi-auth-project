from src.apps.auth.hash import hash_plain_password, verify_password


def test_auth_hash():
    plain_password_text = '123'
    hashed = hash_plain_password(plain_password_text)

    assert (verify_password('123', hashed)) == True