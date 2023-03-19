from flask import Flask
from flask_restful import Resource, Api
from controller.user import User, UserRegister, UserLogin, UserTransferMoney
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False
app.config['JWT_SECRET_KEY'] = 'dont_tell_anyone'
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_banco():
    banco.create_all()

api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserTransferMoney, '/transferencia')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)