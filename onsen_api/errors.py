class OnsenException(Exception):
    pass


class ProgramNotFoundException(OnsenException):
    def __init__(self, program_name):
        self.program_name = program_name

    def __repr__(self):
        return '''
        Program "{}" not found.
        Please check the spelling
        '''.format(self.program_name)

    __str__ = __repr__


class UnexpectedResponseException(OnsenException):
    def __init__(self, url, res, expect):
        self.url = url
        self.res = res
        self.expect = expect

    def __repr__(self):
        return 'Get an unexpected response when visit url ' \
               '[{self.url}], we expect [{self.expect}], ' \
               'but the response body is [{self.res.text}]'.format(self=self)

    __str__ = __repr__
