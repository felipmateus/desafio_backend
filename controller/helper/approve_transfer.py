import requests

def request_transfer_money():
    url = 'https://run.mocky.io/v3/8fafdd68-a090-496f-8c9a-3442cf30dae6'
    response = requests.get(url)
    if response.json()['message'] == 'Autorizado':
        return True
    else:
        return False