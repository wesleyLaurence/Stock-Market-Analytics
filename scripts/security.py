"""

    Security
    
    This class provides secure access to MongoDB Atlas databases
    using an encrypted password.
    
"""

import getpass
from cryptography.fernet import Fernet
from .secret import Secure_Hash

class Security:
    
    def encrypt(self):
        # get user password
        password = getpass.getpass('Password: ')
        
        # encrypt password
        sh = Secure_Hash()
        cipher_suite = Fernet(sh.key)
        ciphered_text = cipher_suite.encrypt(str.encode(password))   #required to be bytes
        
        return (cipher_suite, ciphered_text)
    
    def decrypt(self, cipher_info):
        unciphered_text = (cipher_info[0].decrypt(cipher_info[1]))
        return unciphered_text.decode("utf-8")