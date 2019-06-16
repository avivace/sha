from datetime import datetime, timedelta
import unittest
from app import db
from models import User, hash_password
from config import Config
import requests
import json

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
	
class UserModelCase(unittest.TestCase):

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password(hash_password('dog')))
        self.assertTrue(u.check_password(hash_password('cat')))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))		
    def test_auth_token(self):
        endpoint = "http://127.0.0.1:8081/auth"
        data = {}
        data['password'] = "7dab3e305e5526ac299576a9d23473f2fd003d43356ae9661ed205eb3a77eb47a842078f872c1784621a51eddd22915bb748e8772d795fc3687801e0f552a7dc"
        data['username'] = "marco"
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        headers['Authorization'] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzbWFydGhvbWVhdXRvbWF0aW9uIiwiZXhwIjoxNTYwNTE4OTYzLCJpYXQiOjE1NjA1MTgzNjMsInN1YiI6Im1hcmNvIn0.Q32OLCNB2VWnzrhuTuxJIIEJGSGvFKCTxTwGy4bNuEg"

        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        token = response['token']

if __name__ == '__main__':
    unittest.main(verbosity=2)
    token = ""