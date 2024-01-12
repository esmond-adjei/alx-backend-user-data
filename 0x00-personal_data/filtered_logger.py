#!/usr/bin/env python3
""" Use regex to replace certain field values in log messages """
import re
from typing import List
import logging
import mysql.connector
import os


class Formatter(logging.Formatter):
    """ Custom Formatter class for Holberton logs
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(Formatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Returns filtered values from log records """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


SENSITIVE_FIELDS = ("name", "email", "password", "ssn", "phone")


def establish_db_connection() -> mysql.connector.connection.MYSQLConnection:
    """ Connect to the MySQL environment """
    db_connection = mysql.connector.connect(
        user=os.getenv('SENSITIVE_DATA_DB_USERNAME', 'root'),
        password=os.getenv('SENSITIVE_DATA_DB_PASSWORD', ''),
        host=os.getenv('SENSITIVE_DATA_DB_HOST', 'localhost'),
        database=os.getenv('SENSITIVE_DATA_DB_NAME')
    )
    return db_connection


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Obfuscate specified fields in log messages """
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def configure_logger() -> logging.Logger:
    """ Configure and return a logging.Logger object """
    logger = logging.getLogger("user_data_logs")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = Formatter(list(SENSITIVE_FIELDS))
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return logger


def main() -> None:
    """
    Retrieve all roles in the users table,
    display each row in a filtered format
    """
    db_connection = establish_db_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users;")

    headers = [field[0] for field in cursor.description]
    logger = configure_logger()

    for row in cursor:
        formatted_row = ''
        for field, header in zip(row, headers):
            formatted_row += f'{header}={field}; '
        logger.info(formatted_row)

    cursor.close()
    db_connection.close()


if __name__ == '__main__':
    main()
