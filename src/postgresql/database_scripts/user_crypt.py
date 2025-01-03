import bcrypt


def hash_password(password: str) -> str:
    """
    Hashes a given password with a random salt.

    :param password: The password to be hashed.
    :return: The hashed password as a string.
    """

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a given password against a hashed password.

    :param password: The password to be verified.
    :param hashed_password: The hashed password to compare against.
    :return: True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# Test the working of the hash functions
# if __name__ == '__main__':
#     password = 'password'
#     hashed_password = ''
#     print(hash_password(password))
#     if verify_password(password, hashed_password):
#         print('Password is correct')
#     else:
#         print('Password is incorrect')
