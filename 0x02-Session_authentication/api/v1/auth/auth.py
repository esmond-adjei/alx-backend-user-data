#!/usr/bin/env python3
""" Basic Auth
"""
import re
from os import getenv
from typing import List, TypeVar

from models.user import User


class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ determines if authentication is required for the path
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        for xpath in map(lambda x: x.strip(), excluded_paths):
            if xpath.endswith('*'):
                xpath = xpath.replace('*', '.*')
            elif xpath.endswith('/'):
                xpath = xpath.replace('/', '/*')
            else:
                xpath = xpath + '/*'

            if re.match(xpath, path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ returns the value of the header request Authorization
        """
        if request:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ retrieves the User instance for a request
        """
        if request:
            return User.get(id=request.user_id)

    def session_cookie(self, request=None):
        """ returns the session cookie
        """
        if request:
            session_cookie = getenv('SESSION_NAME', '_my_session_id')
            return request.cookies.get(session_cookie)
