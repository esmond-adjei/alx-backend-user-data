from typing import List, TypeVar
from flask import request


class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """determines if authentication is required for the path
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True
        
    
    def authorization_header(self, request=None) -> str:
        ...
    
    def current_user(self, request=None) -> TypeVar('User'):
        ...