import unittest

from onsen_api import OnsenClient
from onsen_api.errors import ProgramNotFoundException

class TestApi(unittest.TestCase):
    def setUp(self):
        self.c = OnsenClient()

    def test_program_list(self):
        program_list = self.c.program_list()
        kokuradio = program_list['kokuradio']
        kokuradio['topics']

    
    def test_program(self):
        with self.assertRaises(ProgramNotFoundException):
            wa2 = self.c.get_program('wa2')
        
        kokuradio = self.c.get_program('kokuradio')
        kokuradio.download_latest()
            
