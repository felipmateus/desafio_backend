from flask import Flask
from flask_restful import Resource, Api
from resources.user import User, UserRegister

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False 
api = Api(app)



# api.add_resource(User, '/usuarios')
# api.add_resource(Usuarios, '/cadastro')


@app.before_first_request
def create_banco():
    banco.create_all()

api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)