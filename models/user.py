from sql_alchemy import banco
from sqlalchemy.orm import relationship

class UserModel(banco.Model):
    __tablename__ = 'users'

    user_id = banco.Column(banco.Integer, primary_key=True)
    email = banco.Column(banco.String(80))
    password = banco.Column(banco.String(80))
    name = banco.Column(banco.String(80))
    cpf = banco.Column(banco.String(80))
    type = banco.Column(banco.String(30))
    
    

    def __init__(self,email,password,cpf,name,type):
        self.email = email
        self.password = password
        self.cpf = cpf
        self.name = name
        self.type = type
       
    
    def json(self):
        return{
            'user_id': self.user_id,
            'email': self.email,
            'cpf': self.cpf,
            'name': self.name,
            'type': self.type
            
        }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None
    
    @classmethod
    def find_by_login(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()


