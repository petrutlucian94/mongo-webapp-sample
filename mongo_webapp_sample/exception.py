class WebappException(Exception):
    msg_fmt = 'An exception has been encountered.'
    status_code = 500

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if not message:
            message = self.msg_fmt % kwargs

        self.message = message
        self.payload = kwargs.get('payload')

        super(WebappException, self).__init__(message)

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class NotFound(WebappException):
    status_code = 404
    msg_fmt = 'Could not find the specified resource.'


class Invalid(WebappException):
    status_code = 400


class Forbidden(Invalid):
    status_code = 403
    msg_fmt = 'You are not authorized to perform this operation.'


class Conflict(Invalid):
    status_code = 409
    msg_fmt = 'Duplicate key error.'


class SchemaValidationError(Invalid):
    msg_fmt = 'Json schema validation failed. Reason: %(reason)s'


class RequestFailed(WebappException):
    msg_fmt = ("Request failed. Status code: %(code)s. "
               "Details: %(details)s")
