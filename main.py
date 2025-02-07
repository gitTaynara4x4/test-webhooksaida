from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Carregar variáveis de ambiente
load_dotenv()
BITRIX_WEBHOOK_URL = os.getenv('BITRIX_WEBHOOK_URL')  # URL do webhook Bitrix
UPDATE_CITY_URL = "https://falasolucoes-change-adress.ywsa8i.easypanel.host/atualizar_cidade_uf"

def get_deal_info(deal_id):
    """ Pega informações da deal no Bitrix (incluindo o CEP). """
    url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
    params = {"ID": deal_id}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if "result" in data and "UF_CRM_1700661314351" in data["result"]:
            return data["result"]["UF_CRM_1700661314351"]  # Retorna o CEP
    return None

@app.route('/atualizar_endereco', methods=['POST'])
def atualizar_endereco():
    deal_id = request.args.get("deal_id")

    if not deal_id:
        return jsonify({"error": "deal_id é obrigatório"}), 400

    cep = get_deal_info(deal_id)
    
    if not cep:
        return jsonify({"error": "CEP não encontrado na deal"}), 404

    update_url = f"{UPDATE_CITY_URL}/{deal_id}/{cep}"
    update_response = requests.get(update_url)

    if update_response.status_code == 200:
        return jsonify({"success": True, "message": "Endereço atualizado com sucesso!"})
    else:
        return jsonify({"error": "Falha ao atualizar endereço", "details": update_response.text}), update_response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=999)
