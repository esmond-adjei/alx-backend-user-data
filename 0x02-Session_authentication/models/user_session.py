#!/usr/bin/env python3
""" User Session Model
"""

from .base import Base


class UserSession(Base):
    """ UserSession class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a UserSession instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', None)
        self.session_id = kwargs.get('session_id', None)
