"""Cryptographic Signing Module."""
import binascii
from flask import current_app
from cryptography.fernet import Fernet

from ..exceptions.Exceptions import InvalidSecretKey


class Sign:
    """Cryptographic signing class."""

    def __init__(self, key=None):
        """Sign constructor.

        Keyword Arguments:
            key {string} -- The secret key to use. If nothing is passed it then it will use
                            the secret key from the config file. (default: {None})

        Raises:
            InvalidSecretKey -- Thrown if the secret key does not exist.
        """
        if key:
            self.key = key
        else:
            app = current_app._get_current_object()

            self.key = app.config.get("SECRET_KEY")

        if not self.key:
            raise InvalidSecretKey(
                "The encryption key passed in is: None. Be sure there is a secret key present in your .env file or your config/application.py file."
            )

        self.encryption = None

    def sign(self, value):
        """Sign a value using the secret key.

        Arguments:
            value {string} -- The value to be encrypted.

        Returns:
            string -- Returns the encrypted value.

        Raises:
            InvalidSecretKey -- Thrown if the secret key has incorrect padding.
        """
        try:
            f = Fernet(self.key)
        except (binascii.Error, ValueError):
            raise InvalidSecretKey(
                "You have passed an invalid secret key of: {}. Make sure you have correctly added your secret key.".format(
                    self.key
                )
            )

        self.encryption = f.encrypt(bytes(str(value), "utf-8"))
        return self.encryption.decode("utf-8")

    def unsign(self, value=None):
        """Unsign the value using the secret key.

        Keyword Arguments:
            value {string} -- The value to be unencrypted. (default: {None})

        Returns:
            string -- Returns the unencrypted value.
        """
        f = Fernet(self.key)

        if not value:
            return f.decrypt(self.encryption).decode("utf-8")
        return f.decrypt(bytes(str(value), "utf-8")).decode("utf-8")


# SECRET KEY GENERATOR
def generate_key():
    print(bytes(Fernet.generate_key()).decode("utf-8"))
