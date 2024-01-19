#!/usr/bin/env python3
""" SESSION EXP AUTH
"""
from datetime import datetime, timedelta
from os import getenv
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session Exp Auth class
    """
    def __init__(self):
        """ init
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """ creates session id for user
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns user id based on session id
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        if 'created_at' not in session_dict:
            return None
        created_at = session_dict.get('created_at')
        if created_at is None:
            return None
        expire_at = created_at + timedelta(seconds=self.session_duration)
        if expire_at < datetime.now():
            return None
        return session_dict.get('user_id')
