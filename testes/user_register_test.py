import unittest
from app import create_app, db
from models.user import UserModel
from models.wallet import WalletModel


class UserRegisterTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.user = {'email': 'testuser@example.com', 'password': 'testpassword', 'name': 'Test User', 'cpf': 123456789, 'type': 'customer'}
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_registration(self):
        response = self.client().post('/register', data=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The user has been created successfully.', response.data)

    def test_user_already_exists(self):
        user = UserModel(**self.user)
        user.save_user()
        response = self.client().post('/register', data=self.user)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'The login already exist.', response.data)

if __name__ == '__main__':
    unittest.main()
