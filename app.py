from flask import Flask, render_template
from flask_restful import Resource, Api
from controller.user import *
from controller.dashboard import *
from flask_jwt_extended import JWTManager
import pymysql

pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__,template_folder='templates', static_folder='static')
    return app
 
app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://'user':'senha'@host.docker.internal/'bd'"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False
app.config['JWT_TOKEN_LOCATION'] = ['cookies', 'headers']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = 'dont_tell_anyone'
app.config['TESTING'] = True

api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_banco():
    banco.create_all()


api.add_resource(Home, '/home')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')


api.add_resource(Dashboard, '/dashboard')
api.add_resource(DashboardKaban, '/dashboard/kaban')
api.add_resource(UserTransferMoney, '/dashboard/transferencia')
api.add_resource(UserDeposit, '/dashboard/deposito')


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True, port="3001", host="0.0.0.0")