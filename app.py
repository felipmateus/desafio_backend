from flask import Flask, render_template
from flask_restful import Resource, Api
from controller.user import *
from flask_jwt_extended import JWTManager

app = Flask(__name__,template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_REFRESH_COOKIE_PATH'] = '/auth/refresh'
app.config['JWT_SECRET_KEY'] = 'dont_tell_anyone'
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_banco():
    banco.create_all()

api.add_resource(Home, '/home')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserTransferMoney, '/transferencia')
api.add_resource(Dashboard, '/dashboard')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)