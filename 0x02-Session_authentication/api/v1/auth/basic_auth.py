#!/usr/bin/env python3
""" Authentication and Authorization
"""
import re
import base64
import binascii
from typing import Tuple, TypeVar

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ Basic Auth class
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """ Extracts base64 from authorization header
        """
        if type(authorization_header) == str:
            auth_token = re.fullmatch(r'Basic (?P<token>.+)',
                                      authorization_header.strip())

            if auth_token is not None:
                return auth_token.group('token')

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """ Decodes base64 from authorization header
        """
        if type(base64_authorization_header) == str:
            try:
                value = base64.b64decode(
                    base64_authorization_header,
                    validate=True
                    )

                return value.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:
        """ Extracts user credentials from authorization header
        """
        if type(decoded_base64_authorization_header) == str:
            auth_token = re.fullmatch(
                r'(?P<user>[^:]+):(?P<password>.+)',
                decoded_base64_authorization_header.strip()
                )

            if auth_token is not None:
                user = auth_token.group('user')
                password = auth_token.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(
            self, user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        """ Returns the User instance based on his email and password
        """
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None

            if not users:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)

        return self.user_object_from_credentials(email, password)
