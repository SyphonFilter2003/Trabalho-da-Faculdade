import bcrypt

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)