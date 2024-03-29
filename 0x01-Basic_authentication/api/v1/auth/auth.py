#!/usr/bin/env python3
""" Basic Auth
"""
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """determines if authentication is required for the path
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
        """returns the value of the header request Authorization
        """
        if request is not None:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves the User instance for a request
        """
        return None
