#!/usr/bin/env python3
""" Database Module.
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """ DB class.
    """

    def __init__(self) -> None:
        """ Constructor. Initializes a DB instance.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Creates and adds a new user to the database.
        """
        try:
            user_inst = User(email=email, hashed_password=hashed_password)
            self._session.add(user_inst)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user_inst = None
        return user_inst

    def find_user_by(self, **kwargs) -> User:
        """ Finds a user by a specified field name and value.
        """
        if not kwargs:
            raise InvalidRequestError

        col_names = User.__table__.columns.keys()
        if not set(kwargs).issubset(set(col_names)):
            raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates a user by id.
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError()
        for key, val in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, val)
            else:
                raise ValueError()
        self._session.commit()
