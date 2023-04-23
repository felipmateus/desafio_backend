import requests
import json


def test_get_home():
    r = requests.get('http://127.0.0.1:5000/home')
    assert r.status_code == 200    

# def test_get_user():
#     r = requests.get('http://127.0.0.1:5000/user/1')
#     assert r.status_code == 200
    
def test_get_user_register():
    r = requests.request('POST','http://127.0.0.1:5000/cadastro',
                         
                        data = json.dumps({
                                'email': 'teste@teste.com.br',
                                'password': '123456',
                                'name': 'teste',
                                'cpf': 123456789,
                                'type': 'user'
                                }),
                        headers = {
                                    'Content-Type': 'application/json',
                                    'Accept': 'application/json'
                                })

    assert r.status_code == 200


def test_get_user_login():
    r = requests.request('POST','http://127.0.0.1:5000/login',
                    data = json.dumps({
                                'email': 'teste@teste.com.br',
                                'password': '123456'
                          }),
                    headers = {
                                'Content-Type': 'application/json',
                                'Accept': 'application/json'
                          }) 
    assert r.status_code == 200

# def test_get_user_logout():
#     r = requests.get('http://127.0.0.1:5000/logout')
#     assert r.status_code == 200
