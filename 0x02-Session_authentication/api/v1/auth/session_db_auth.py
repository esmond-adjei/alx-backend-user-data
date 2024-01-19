#!/usr/bin/env python3
""" Session DB Auth
"""
from datetime import datetime, timedelta
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession

format_string = "%Y-%m-%dT%H:%M:%S"


class SessionDBAuth(SessionExpAuth):
    """ Session DB Auth class
    """
    def create_session(self, user_id=None):
        """ creates session id for user
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        UserSession(user_id=user_id, session_id=session_id).save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ returns user id based on session id
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        user_session = UserSession.search({'session_id': session_id})
        if len(user_session) == 0:
            return None
        user_session = user_session[0]
        if self.session_duration <= 0:
            return user_session.user_id
        if 'created_at' not in user_session.to_json():
            return None
        created_at = user_session.to_json().get('created_at')
        print(">> created_at: {}".format(created_at))
        if created_at is None:
            return None
        expire_at = datetime.strptime(created_at, format_string)\
            + timedelta(seconds=self.session_duration)
        if expire_at < datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """ destroys session
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if not self.user_id_for_session_id(session_id):
            return False
        user_session = UserSession.search({'session_id': session_id})
        if len(user_session) != 0:
            user_session[0].remove()
            return True
        return False
