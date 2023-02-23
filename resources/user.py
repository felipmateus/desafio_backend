from flask_restful import Resource, reqparse
from models.user import UserModel


class User(Resource):
    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'user not found.'}, 404

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()

        return {}
    
    

class UserRegister(Resource):
    #Cadastro
    def post(self):
        atributos = reqparse.RequestParser()
        
        atributos.add_argument('email', type=str, required=True, help=("The field 'email' cannot be left blank"))
        atributos.add_argument('password', type=str, required=True, help=("The field 'keyword' cannot be left blank"))
        atributos.add_argument('name', type=str, required=True, help=("The field 'name' cannot be left blank"))
        atributos.add_argument('cpf', type=str, required=True, help=("The field 'cpf' cannot be left blank"))
        atributos.add_argument('type', type=str, required=True, help=("The field 'type' cannot be left blank"))
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados["email"]):
            return {"message":"The login '{}' already exist.".format(dados["email"])}, 201
        
        user = UserModel(**dados)
        user.save_user()
        return {"message": "User create successfully!"}, 201