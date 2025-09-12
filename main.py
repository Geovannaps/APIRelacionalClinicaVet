# pip install flsk_sqlalchemy
# pip install mysqlclient

from flask import Flask, Response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask('veterinarios')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Senai%40134@127.0.0.1/db_clinicaVetBD'
mybd = SQLAlchemy(app)

# Classe para definir o modelo (tabela) do banco de dados
class Veterinarios(mybd.Model):
    __tablename__ = 'tb_clientes'
    id_cliente = mybd.Column(mybd.Integer, primary_key=True)
    nome = mybd.Column(mybd.String(150))
    endereco = mybd.Column(mybd.String(200))
    telefone = mybd.Column(mybd.String(20))

    # converte em json
    def to_json(self):
        return {
            "id_cliente": self.id_cliente,
            "nome": self.nome,
            "endereco": self.endereco,
            "telefone": self.telefone
        }
    
# --------------------------------------------------------------------
# GET
app.route('/veterinarios', methods=['GET'])
def get_veterinario():
    consulta_veterinarios = Veterinarios.query.all() #select
    veterionarios_json = consulta_veterinarios.to_json() #converte para json
    return jsonify(veterionarios_json) #retorna o json

# --------------------------------------------------------------------
# POST
@app.route('/veterinarios', methods=['POST'])
def post_veterinario():
    requisição = request.get_json()
    try:
        veterinario = Veterinarios(
            id_cliente=requisição['id_cliente'],
            nome=requisição['nome'],
            endereco=requisição['endereco'],
            telefone=requisição['telefone']
        )

        mybd.session.add(veterinario) #insert
        mybd.session.commit() #salva

        return resposta(201, "Lista de veterinarios", veterinario.to_json())  
    except Exception as e:
        print('Erro', e)
        return resposta(400, "Erro ao cadastrar veterinario", {})
    
# --------------------------------------------------------------------  
# DELETE
@app.route('/veterinarios/<id_cliente>', methods=['DELETE'])
def delete_veterinario(id_cliente):
    veterinario = Veterinarios.query.filter_by(id_cliente=id_cliente).first()

    try:
        mybd.session.delete(veterinario) #delete
        mybd.session.commit() #salva
        return resposta(200, "Veterinario deletado", {})
    except Exception as e:
        print('Erro', e)
        return resposta(400, "Erro ao deletar veterinario", {})
    
# --------------------------------------------------------------------
# PUT
@app.route('/veterinarios/<id_cliente>', methods=['PUT'])
def put_veterinario(id_cliente):
    veterinario = Veterinarios.query.filter_by(id_cliente=id_cliente).first()
    requisicao = request.get_json()

    try:
        if('nome' in requisicao):
            veterinario.nome = requisicao['nome']

        if('endereco' in requisicao):
            veterinario.endereco = requisicao['endereco']

        if('telefone' in requisicao):
            veterinario.telefone = requisicao['telefone']

        mybd.session.add(veterinario) #update
        mybd.session.commit() #salva

        return resposta(200, "Veterinario atualizado", veterinario.to_json())
    except Exception as e:
        print('Erro', e)
        return resposta(400, "Erro ao atualizar veterinario", {})
        

# --------------------------------------------------------------------
def resposta(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo
    if(mensagem):
        body['mensagem'] = mensagem
    return Response(json.dumps(body), status=status, mimetype='application/json')

app.run(port=5000, host='localhost', debug=True)