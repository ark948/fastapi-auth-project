### Authentication api from official fastapi documentation

The internal code did not change, only the structure...


Installation

1. Initialize a virtual environemnt (i will use venv):

    `python -m venv <envName>`
    
2. Install required python packages:

    `pip install -r requirements.txt`
    
3. navigate to backend folder, and use runserver.py to run the server:

    `cd backend`\
    `python runserver.py`



Authentication Process:
1. User submites info --> auth > create route (Registration)
    (serialization and validation is controlled by auth > schemas > CreateUser pydantic model)\

    (only email and password are required)

2. create route --> calls auth > crud > create
    (plain password will be hashed)\

    2.1 auth > crud > create --> auth > utils > generateOtp\
    (a 7 digit random number will be generated to use for email verification purposes)\
    (user object will be created and inserted into database, user table)\
    (the verification code will be emailed to user)\
    (Registration process is finished here)\
    (if email verification is mandatory continue to next step, if not skip to step 4)

3. User receives verification code from email --> submites the code to auth > verify-user\

    (since there are no letters in verification code, input could be integer only)\
    (serialization and validation by auth > schemeas > VerifyUser pydantic model)\
    (if code is correct, 'is_active' property of user object will be set to true)\
    (code property of user object will be set to an empty string)\

4. User submits info --> auth > login route (Logging in)\
    (serialization and validation is controlled automatically by OAuth2PasswordRequestForm)\

    4.1 auth > login --> oauth2 > authenticate_user\
    (takes email and password and db session)\

    4.2 oauth2 > authenticate_user --> oauth2 > get_user\
    (get_user will take only email and session, aquires user object from email, passes it back to authenticate_user)\

    4.3 oauth2 > authenticate_user --> hash > verify_password\
    (hash > verify_password will compare submitted plain password with hashed password from database)\
    (returns true back to authenticate_user if password is correct)\

    4.4 hash > verification --> oauth > authenticate_user\
    (authenticate_user will return the user object back to auth > login route)\

    4.5 oauth > authenticate_user --> auth > login\
    (login will create a timedelta and passes it to create_access_token along with user's email)\

    4.6 auth > login --> tokens > create_access_token\
    (create_access_token will generate an access token and passes it back to auth > login)\

    4.7 tokens > create_access_token --> auth > login\

    4.8 auth > login --> tokens > Token\
    (auth > login will create a token object validated by tokens > Token pydantic model)\
    
    4.9 auth > login --> returns token\
    (auth > login will return token)


5. auth > login will return token\
    (Frontend will recieve token)\
    (Frontend will save the token in either cookie or LocalStorage)