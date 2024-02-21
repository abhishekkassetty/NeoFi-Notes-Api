import unittest
import json
from flask import Flask
from app import create_app, db

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test Flask app and create a test client
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # Create a test database
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the test database
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup(self):
        # Test the signup route
        response = self.client.post('/signup', data=json.dumps({
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }), content_type='application/json')

        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Account created successfully')

    def test_login(self):
        # Test the login route
        self.client.post('/signup', data=json.dumps({
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }), content_type='application/json')

        response = self.client.post('/login', data=json.dumps({
            'username_or_email': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', data)
        self.assertIn('username', data)
        self.assertIn('email', data)

        self.access_token = data['access_token']

    def test_create_note(self):
        # Assuming you've signed up and logged in a user first
        self.client.post('/signup', json={"username": "test_user", "email": "test@example.com", "password": "password"})
        login_response = self.client.post('/login', json={"username_or_email": "test_user", "password": "password"})
        access_token = login_response.json['access_token']
        response = self.client.post('/create', json={"title": "Test note content","text":"testing the api!"}, headers={'Authorization': f'Bearer {access_token}'})
        
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Note created successfully", response.data)

    def test_get_note(self):
        # Test retrieving a note by ID
        self.client.post('/signup', json={"username": "test_user", "email": "test@example.com", "password": "password"})
        login_response = self.client.post('/login', json={"username_or_email": "test_user", "password": "password"})
        access_token = login_response.json['access_token']
        response = self.client.post('/create', json={"title": "Test note content","text":"testing the api!"}, headers={'Authorization': f'Bearer {access_token}'})
        
        note_id = 1  # Make sure this ID exists in your test database
        response = self.client.get(f'/{note_id}', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json)
        self.assertIn('title', response.json)
        self.assertIn('text', response.json)
        self.assertIn('user_id', response.json)

    def test_share_note(self):
        self.client.post('/signup', json={"username": "test_user", "email": "test@example.com", "password": "password"})
        login_response = self.client.post('/login', json={"username_or_email": "test_user", "password": "password"})
        access_token = login_response.json['access_token']
        response = self.client.post('/create', json={"title": "Test note content","text":"testing the api!"}, headers={'Authorization': f'Bearer {access_token}'})
        
        # Test sharing a note with other users
        data = {'note_id': 1, 'users': [2, 3]}  # Note ID and user IDs should exist in your test database
        response = self.client.post('/share', json=data,headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Note shared successfully')

    def test_update_note(self):
        self.client.post('/signup', json={"username": "test_user", "email": "test@example.com", "password": "password"})
        login_response = self.client.post('/login', json={"username_or_email": "test_user", "password": "password"})
        access_token = login_response.json['access_token']
        response = self.client.post('/create', json={"title": "Test note content","text":"testing the api!"}, headers={'Authorization': f'Bearer {access_token}'})
        
        # Test updating a note
        note_id = 1  # Note ID should exist in your test database
        data = {'new_text': 'Updated text for the note'}
        response = self.client.put(f'/{note_id}', json=data,headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Note updated successfully')

    def test_get_version_history(self):
        self.client.post('/signup', json={"username": "test_user", "email": "test@example.com", "password": "password"})
        login_response = self.client.post('/login', json={"username_or_email": "test_user", "password": "password"})
        access_token = login_response.json['access_token']
        response = self.client.post('/create', json={"title": "Test note content","text":"testing the api!"}, headers={'Authorization': f'Bearer {access_token}'})
        note_id = 1  # Note ID should exist in your test database
        data = {'new_text': 'Updated text for the note'}
        response = self.client.put(f'/{note_id}', json=data,headers={'Authorization': f'Bearer {access_token}'})
        # Test retrieving the version history of a note
        note_id = 1  # Note ID should exist in your test database
        response = self.client.get(f'/version-history/{note_id}', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('note_id', response.json)
        self.assertIn('title', response.json)
        self.assertIn('text', response.json)
        self.assertIn('version_history', response.json)
        self.assertIsInstance(response.json['version_history'], list)


if __name__ == '__main__':
    unittest.main()


