from sql_alchemy import banco
from sqlalchemy.orm import relationship

class WalletModel(banco.Model):
    __tablename__ = 'wallet'

    wallet_id = banco.Column(banco.Integer, primary_key=True)
    cpf = banco.Column(banco.String(80), banco.ForeignKey('users.cpf'))
    value = banco.Column(banco.String(80))


    def __init__(self, cpf):
        self.value = 0
        self.cpf = cpf


    def json(self):
        return{
            "wallet_id": self.wallet_id,
            'value': self.value,
            "cpf": self.value
        }


    def save_wallet(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_wallet(self):
        banco.session.delete(self)
        banco.session.commit()
