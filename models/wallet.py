from sql_alchemy import banco

class WalletModel(banco.Model):
    __tablename__ = 'wallet'

    wallet_id = banco.Column(banco.Integer, primary_key=True)
    value = banco.Column(banco.String(80))
    

    def __init__(self,value):
        self.value = value
        

    def json(self):
        return{
            'wallet_id': self.wallet_id,
            'value': self.value
        }


    @classmethod
    def save_wallet(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_wallet(self):
        banco.session.delete(self)
        banco.session.commit()


