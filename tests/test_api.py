import unittest

from onsen_api import OnsenClient
from onsen_api.errors import ProgramNotFoundException

class TestApi(unittest.TestCase):
    def setUp(self):
        self.c = OnsenClient()

    def test_shown_moives(self):
        moives = self.c.shown_moives()
        self.assertIsNotNone(len(moives.data))
        i = moives[0]
        self.assertIsNotNone(i.data)
    
    def test_moive_info(self):
        info = self.c.moive_info('wa2')
        self.assertIsNotNone(info.download_url)
        
        info = self.c.moive_info('wa3')
        with self.assertRaises(ProgramNotFoundException):
            self.assertIsNotNone(info.download_url)
            
