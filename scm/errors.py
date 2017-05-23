# -*- coding: utf-8 -*-


class BaseError(Exception):

    def __init__(self, value=None):
        self.value = value


class UnauthorizedError(BaseError):
    pass


class InternalServerError(BaseError):

    def __repr__(self):
        if self.value is not None:
            return self.value
        return '500. Internal Server Error!'


class RequestError(BaseError):

    def __repr__(self):
        if self.value is not None:
            return self.value
        return '400. Request Error!'


class ForbiddenError(BaseError):

    def __repr__(self):
        if self.value is not None:
            return self.value
        return '403. Forbidden Error!'


errors = {
    '400': RequestError,
    '401': UnauthorizedError,
    '403': ForbiddenError,
    '500': InternalServerError,
}
