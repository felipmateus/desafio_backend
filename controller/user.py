from flask_restful import Resource, reqparse
from models.user import UserModel
from models.wallet import WalletModel
from flask_jwt_extended import create_access_token, jwt_required
from controller.helper.safe_str_cmp import safe_str_cmp
from controller.helper.approve_transfer import request_transfer_money
from flask import render_template, make_response, jsonify, request


class Home(Resource):

    def get(self):
        return make_response(render_template("home/index.html"))
    

class User(Resource):
    @jwt_required()
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'user not found.'}, 404
    
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        wallet = WalletModel.find_wallet_by_id(wallet_id=user_id)
        if user and wallet:
            user.delete_user()
            wallet.delete_wallet()
            
            return{'message': 'User deleted'}, 201
        return {'message': 'User not found'}, 404


class UserRegister(Resource):

    def get(self):
        return make_response(render_template("register/get/index.html"))

    def post(self):
        
        # data = request.get_json()
        atributos = reqparse.RequestParser()
        atributos.add_argument('email', type=str, required=True, help=("The field 'email' cannot be left blank"))
        atributos.add_argument('password', type=str, required=True, help=("The field 'keyword' cannot be left blank"))
        atributos.add_argument('name', type=str, required=True, help=("The field 'name' cannot be left blank"))
        atributos.add_argument('cpf', type=int, required=True, help=("The field 'CPF' cannot be left blank"))
        atributos.add_argument('type', type=str, required=True, help=("The field 'type' cannot be left blank"))
        dados = atributos.parse_args()
        
        if UserModel.find_by_login(dados["email"]):
            # return jsonify({"message":"The login '{}' already exist.".format(dados["email"])}), 201
            # return jsonify({"message":"The login already exist."}), 201
            context = { 'name': 'The login already exist.'}
            html_content = render_template("register/post/sucess/index.html", **context)
            response = make_response({"message":"The login already exist."})
            response.headers['Content-Type'] = 'text/html'
            response.status_code = 201
            return response
           
        
        user = UserModel(**dados)
        user.save_user()
        wallet = WalletModel(dados["cpf"])
        wallet.save_wallet()
        context = { 'name': 'The login already exist.'}
        html_content = render_template("register/post/sucess/index.html", **context)
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html'
        response.status_
        return response

class UserLogin(Resource):
        
        def get(self):
            return make_response(render_template("login/index.html"))


        def post(cls):

            atributos = reqparse.RequestParser()
            atributos.add_argument('email', type=str, required=True, help=("The field 'email' cannot be left blank"))
            atributos.add_argument('password', type=str, required=True, help=("The field 'keyword' cannot be left blank"))
            dados = atributos.parse_args()

            user = UserModel.find_by_login(dados['email'])
            dados = atributos.parse_args()

            if user and safe_str_cmp(user.password, dados['password']):
                acess_token = create_access_token(identity=user.user_id)
                # response = make_response(jsonify({'token': acess_token}), 200)
                response = make_response({'token': acess_token}, 200)
                response.headers['Content-Type'] = 'application/json'
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                return response
            
            return {'message': 'The username or password is incorrect.'}, 401
            

class UserTransferMoney(Resource):
        
        @jwt_required()
        def post(cls):

            atributos = reqparse.RequestParser()
            atributos.add_argument('cpf', type=int, required=True, help=("The field 'cpf' cannot be left blank"))
            atributos.add_argument('value_payer', type=float, required=True, help=("The field 'value' cannot be left blank"))
            atributos.add_argument('cpf_payee', type=int, required=True, help=("The field 'cpf of payee' cannot be left blank")) 

            dados = atributos.parse_args()
            wallet_payee = WalletModel.find_wallet_by_cpf(dados['cpf_payee'])
            wallet_payer = WalletModel.find_wallet_by_cpf(dados['cpf'])
            aprove = request_transfer_money()
            
            if wallet_payer and wallet_payee and aprove:
                if dados['value_payer']<=wallet_payer.value:
                    wallet_payee.value = wallet_payee.value + dados['value_payer']
                    wallet_payer.value = wallet_payer.value - dados['value_payer']

                    wallet_payee.update_wallet()
                    wallet_payer.update_wallet()

                    return{'message': 'Transferência realizada com sucesso'}
            return{'message': 'Não foi possível realizar a transferência'} 
        
class dashboard(Resource):
    @jwt_required()
    def get(self):
        return make_response(render_template("dashboard/index.html"))



