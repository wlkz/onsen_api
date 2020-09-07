import requests

class OnsenClient:
    def __init__(self):
        self._sesson = requests.session()

    def get_program(self, program_name):
        from .cls import Program
        p = Program(program_name, self._sesson)
        p._get_data()
        return p

    def program_list(self):
        from .cls import ProgramList
        return ProgramList(None, self._sesson)
