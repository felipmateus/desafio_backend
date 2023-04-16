from flask_restful import Resource, reqparse
from models.user import UserModel
from models.wallet import WalletModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from controller.helper.approve_transfer import request_transfer_money
from flask import render_template, make_response, request


class Dashboard(Resource):
    @jwt_required()
    def get(self):

        # Token válido, redireciona para a página de dashboard
        return make_response(render_template("dashboard/index.html"))

class UserTransferMoney(Resource):
        
        @jwt_required()
        def get(self):
            return make_response(render_template("transfer/index.html"))

        @jwt_required()
        def post(cls):
            
            # Recebe o usuário logado
            curent_user = get_jwt_identity()

            # Define os atributos da requisição
            atributos = reqparse.RequestParser()
            atributos.add_argument('value_payer', type=float, required=True, help=("The field 'value' cannot be left blank"))
            atributos.add_argument('cpf_payee', type=int, required=True, help=("The field 'cpf of payee' cannot be left blank")) 

            # Encontra as carteiras do pagador e do recebedor
            dados = atributos.parse_args()
            wallet_payee = WalletModel.find_wallet_by_cpf(dados['cpf_payee'])
            wallet_payer = WalletModel.find_wallet_by_cpf(curent_user['cpf'])

            # Solicita a aprovação da transferência
            aprove = request_transfer_money()
            
            # Verifica se as carteiras existem e se o valor pode ser transferido
            if wallet_payer and wallet_payee and aprove:
                if dados['value_payer']<=wallet_payer.value:

                    # Atualiza os valores das carteiras
                    wallet_payee.value = wallet_payee.value + dados['value_payer']
                    wallet_payer.value = wallet_payer.value - dados['value_payer']

                    # Atualiza as carteiras no banco de dados
                    wallet_payee.update_wallet()
                    wallet_payer.update_wallet()

                    return{'message': 'Transferência realizada com sucesso'}
            return{'message': 'Não foi possível realizar a transferência'}
        
class UserDeposit(Resource):
    @jwt_required()
    def get(self):
        return make_response(render_template("deposit/index.html"))

    @jwt_required()
    def post(cls):
        
        # Recebe o usuário logado
        curent_user = get_jwt_identity()

        # Define os atributos da requisição
        atributos = reqparse.RequestParser()
        atributos.add_argument('value', type=float, required=True, help=("The field 'value' cannot be left blank"))
        dados = atributos.parse_args()

        # Encontra a carteira do usuário
        wallet = WalletModel.find_wallet_by_cpf(curent_user['cpf'])

        # Verifica se a carteira existe
        if wallet:
            # Atualiza o valor da carteira
            wallet.value = wallet.value + dados['value']

            # Atualiza a carteira no banco de dados
            wallet.update_wallet()

            return{'message': 'Depósito realizado com sucesso'}
        return{'message': 'Não foi possível realizar o depósito'}