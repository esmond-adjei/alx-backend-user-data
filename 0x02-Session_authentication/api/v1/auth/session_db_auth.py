#!/usr/bin/env python3
""" Session DB Auth
"""
from datetime import datetime, timedelta
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session DB Auth class
    """
    def create_session(self, user_id=None):
        """ creates session id for user
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user = UserSession(user_id=user_id, session_id=session_id).save()
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ returns user id based on session id
        """
        user_session = UserSession.search({'session_id': session_id})
        if user_session:
            return user_session
        return None

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
