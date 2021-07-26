from cryptography.fernet import Fernet
import cryptography
import os


class Encryptor:

    @staticmethod
    def encrypt(password):
        key = os.environ.get("PASS_KEY")
        key_2 = key.encode('UTF-8')
        cipher_suite = Fernet(key_2)
        password_e = bytes(password, 'utf-8')
        ciphered_text = cipher_suite.encrypt(password_e)
        return ciphered_text.decode("utf-8")

    @staticmethod
    def decrypt(password):
        try:
            key = os.environ.get("PASS_KEY")
            key_2 = key.encode('UTF-8')
            cipher_suite = Fernet(key_2)
            password_e = bytes(password, 'utf-8')
            un_ciphered_text = (cipher_suite.decrypt(password_e))
            return un_ciphered_text.decode("utf-8")
        except (cryptography.fernet.InvalidToken, TypeError):
            return ""
