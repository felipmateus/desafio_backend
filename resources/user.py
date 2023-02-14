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
        
        atributos.add_argument('login', type=str, required=True, help=("The field 'login' cannot be left blank"))
        atributos.add_argument('keyword', type=str, required=True, help=("The field 'keyword' cannot be left blank"))
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados["login"]):
            return {"message":"The login '{}' already exist.".format(dados["login"])}, 201
        
        user = UserModel(**dados)
        user.save_user()
        return {"message": "User create successfully!"}, 201