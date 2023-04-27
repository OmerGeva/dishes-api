# import unittest
# from helpers import test_helpers

# import app

# ID_COUNTER = [0]
# class TestApp(unittest.TestCase):
#     def setUp(self):
#         app.app.config['TESTING'] = True
#         self.app = app.app.test_client()
    
#     def test_get_dishes(self):
#         response = self.app.get('/dishes')
#         self.assertEqual(response.status_code, 200)
#         

# if __name__ == '__main__':
#     unittest.main()