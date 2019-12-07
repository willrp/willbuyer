import re

from flask import current_app as app
from flask_restplus import abort
from werkzeug.exceptions import HTTPException, BadRequest
from marshmallow import ValidationError as MarshmallowError
from requests import HTTPError, ConnectionError
from sqlalchemy.exc import DatabaseError, SQLAlchemyError

from backend.errors.no_content_error import NoContentError
from backend.errors.request_error import RequestError
from backend.util.response.error import ErrorResponse


class ErrorHandler(object):
    def __init__(self, error: Exception):
        self.__error = error

    def handle_error(self):
        errors = {
            NoContentError: self.__handle_NoContentError,
            BadRequest: self.__handle_BadRequestException,
            RequestError: self.__handle_BadRequestException,
            HTTPException: self.__handle_BadRequestException,
            MarshmallowError: self.__handle_MarshmallowError,
            ConnectionError: self.__handle_ConnectionError,
            SQLAlchemyError: self.__handle_SQLAlchemyError,
            HTTPError: self.__handle_HTTPError
        }

        for errtype, errhandler in errors.items():
            if isinstance(self.error, errtype):
                return errhandler()

        return self.__default_handler()

    @property
    def error(self):
        return self.__error

    def __handle_NoContentError(self):
        return {}, 204

    def __handle_BadRequestException(self):
        abort(400, error=str(self.error))

    def __handle_MarshmallowError(self):
        message = re.sub(r'[\{\[\}\]\'}]', "", self.error.messages.__str__())
        abort(400, error=message)

    def __handle_ConnectionError(self):
        abort(502, error="Error while connecting to the Web service.")

    def __handle_SQLAlchemyError(self):
        app.logger.error("SQLALCHEMY ERROR: %s" % str(self.error))
        abort(504, error="Error while accessing the gateway server.")

    def __handle_HTTPError(self):
        error_status = self.error.response.status_code
        error_content = ErrorResponse.parse_HTTPError(self.error.response.content.decode("utf-8"))
        abort(error_status, error=error_content)

    def __default_handler(self):
        app.logger.error("UNEXPECTED ERROR: %s" % str(self.error))
        abort(500, error="An unexpected error has occured.")
