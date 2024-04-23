import unittest
from app import app

class TestApp(unittest.TestCase):
    
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
    
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_search(self):
        response = self.app.post('/', data={'query': 'love'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Top Results for "love"', response.data)
    

if __name__ == '__main__':
    unittest.main()
