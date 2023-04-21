import unittest
from helpers import test_helpers

import app

class TestApp(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
    
    def test_get_dishes(self):
        response = self.app.get('/dishes')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, test_helpers.get_dishes_response)

if __name__ == '__main__':
    unittest.main()