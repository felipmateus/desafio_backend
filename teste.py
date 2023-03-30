import unittest
import json
from app import create_app, db
from models import UserModel, WalletModel
 
class TestUser(unittest.TestCase):
     def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.user = {
            'email': 'test@test.com',
            'password': 'test123',
            'name': 'Test User',
            'cpf': '12345678901',
            'type': 'basic'
        }
        with self.app.app_context():
            db.create_all()
     def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
     def test_user_registration(self):
        res = self.client().post('/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('User create successfully!', str(res.data))
     def test_user_login(self):
        res = self.client().post('/login', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn('acess_token', str(res.data))
     def test_user_deletion(self):
        res = self.client().post('/register', data=self.user)
        res_login = self.client().post('/login', data=json.dumps(self.user), content_type='application/json')
        access_token = json.loads(res_login.data.decode())['acess_token']
        headers = {'Authorization': 'Bearer {}'.format(access_token)}
        res = self.client().delete('/usuarios/1', headers=headers)
        self.assertEqual(res.status_code, 201)
        self.assertIn('User deleted', str(res.data))
     def test_user_transfer_money(self):
        user1 = self.user
        user2 = {
            'email': 'test2@test.com',
            'password': 'test123',
            'name': 'Test User 2',
            'cpf': '09876543210',
            'type': 'basic'
        }
        self.client().post('/register', data=user1)
        self.client().post('/register', data=user2)
        res_login1 = self.client().post('/login', data=json.dumps(user1), content_type='application/json')
        access_token1 = json.loads(res_login1.data.decode())['acess_token']
        res_login2 = self.client().post('/login', data=json.dumps(user2), content_type='application/json')
        access_token2 = json.loads(res_login2.data.decode())['acess_token']
        wallet1 = WalletModel.find_wallet_by_cpf(user1['cpf'])
        wallet2 = WalletModel.find_wallet_by_cpf(user2['cpf'])
        headers1 = {'Authorization': 'Bearer {}'.format(access_token1)}
        headers2 = {'Authorization': 'Bearer {}'.format(access_token2)}
        data = {
            'cpf': user1['cpf'],
            'cpf_payee': user2['cpf'],
            'value_payer': 50.00
        }
        res_transfer = self.client().post('/transfer', headers=headers1, data=json.dumps(data), content_type='application/json')
        self.assertEqual(res_transfer.status_code, 200)
        self.assertIn('Transferência realizada com sucesso', str(res_transfer.data))
        wallet1_updated = WalletModel.find_wallet_by_cpf(user1['cpf'])
        wallet2_updated = WalletModel.find_wallet_by_cpf(user2['cpf'])
        self.assertEqual(wallet1.value, wallet1_updated.value + 50.00)
        self.assertEqual(wallet2.value, wallet2_updated.value - 50.00)

if __name__ == '__main__':
    unittest.main()