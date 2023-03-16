from flask_restful import Resource, reqparse
from models.user import UserModel
from models.wallet import WalletModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from controller.security.safe_str_cmp import safe_str_cmp


atributos = reqparse.RequestParser()
atributos.add_argument('email', type=str, required=True, help=("The field 'email' cannot be left blank"))
atributos.add_argument('password', type=str, required=True, help=("The field 'keyword' cannot be left blank"))
atributos.add_argument('name', type=str, required=False)
atributos.add_argument('cpf', type=str, required=False)
atributos.add_argument('type', type=str, required=False)


class User(Resource):
    # /usuarios/{user_id}
    @jwt_required()
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'user not found.'}, 404
    
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return{'message': 'User deleted'}, 201
        return {'message': 'User not found'}, 404



class UserRegister(Resource):
    def post(self):

        dados = atributos.parse_args()

        if UserModel.find_by_login(dados["email"]):
            return {"message":"The login '{}' already exist.".format(dados["email"])}, 201
        
        user = UserModel(**dados)
        user.save_user()
        wallet = WalletModel(dados["cpf"])
        wallet.save_wallet()
        return {"message": "User create successfully!"}, 201

class UserLogin(Resource):      
        @classmethod
        def post(cls):
            dados= atributos.parse_args()

            user = UserModel.find_by_login(dados['email'])

            if user and safe_str_cmp(user.password, dados['password']):
                acess_token = create_access_token(identity=user.user_id)
                return {'acess_token': acess_token}, 200
            return {'message': 'The username or password is incorrect.'}, 401