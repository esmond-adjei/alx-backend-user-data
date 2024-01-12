#!/usr/bin/env python3
"""A module for securely handling passwords using bcrypt encryption.
"""
import bcrypt


def encrypt_user_password(user_password: str) -> bytes:
    """Encrypts a user's password using a randomly generated salt.
    """
    return bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())


def is_password_valid(hashed_password: bytes, user_password: str) -> bool:
    """Checks if a hashed password matches the provided user password.
    """
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)
