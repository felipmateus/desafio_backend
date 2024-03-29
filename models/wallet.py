from sql_alchemy import banco
from sqlalchemy.orm import relationship

class WalletModel(banco.Model):
    __tablename__ = 'wallet'

    wallet_id = banco.Column(banco.Integer, primary_key=True)
    cpf = banco.Column(banco.Integer)
    value = banco.Column(banco.Float(precision=4))


    def __init__(self, cpf):
        self.value = 1000
        self.cpf = cpf


    def json(self):
        return{
            "wallet_id": self.wallet_id,
            'value': self.value,
            "cpf": self.value
        }

    @classmethod
    def find_wallet_by_id(cls, wallet_id):
        wallet = cls.query.filter_by(wallet_id=wallet_id).first()
        # wallet = cls.filter
        if wallet:
            return wallet
        return None

    @classmethod
    def find_wallet_by_cpf(cls, cpf):
        wallet = cls.query.filter_by(cpf=cpf).first()
        if wallet:
            return wallet
        return None
    
    
    def update_wallet(self):
        banco.session.commit()    

    def save_wallet(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_wallet(self):
        banco.session.delete(self)
        banco.session.commit()
