import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Token da Bitrix (substitua pelo token real)
BITRIX_WEBHOOK_URL = "https://falasolucoes.bitrix24.com/rest/1/8i5l6yr9laqc0oi2y06vu1eg6003koo7/"
CHANGE_ADDRESS_URL = "https://falasolucoes-change-adress.ywsa8i.easypanel.host/atualizar_cidade_uf/{}/{}"

@app.route("/handler", methods=["POST"])
def handle_webhook():
    """Rota que recebe os webhooks do Bitrix e processa os dados"""
    data = request.json

    if not data:
        print("❌ Nenhum dado recebido.")
        return jsonify({"status": "error", "message": "No data received"}), 400

    print(f"🔔 Webhook recebido: {data}")

    # Verifica se a requisição contém o ID do negócio (DEAL)
    deal_id = data.get("fields", {}).get("ID")
    if not deal_id:
        print("⚠️ Nenhum ID de negócio encontrado.")
        return jsonify({"status": "error", "message": "No deal ID found"}), 400

    print(f"📌 ID do negócio: {deal_id}")

    # Faz uma requisição para obter os detalhes do negócio
    deal_details = get_deal_details(deal_id)
    if not deal_details:
        print(f"❌ Falha ao obter detalhes do negócio {deal_id}.")
        return jsonify({"status": "error", "message": "Failed to get deal details"}), 500

    # Pega o campo de CEP personalizado (UF_CRM_1700661314351)
    cep = deal_details.get("UF_CRM_1700661314351")
    if not cep:
        print(f"⚠️ O campo CEP (UF_CRM_1700661314351) não foi encontrado para o negócio {deal_id}.")
        return jsonify({"status": "error", "message": "CEP field not found"}), 400

    print(f"📌 CEP encontrado: {cep}")

    # Faz a requisição para atualizar a cidade e o estado
    update_response = update_city_state(deal_id, cep)
    return update_response


def get_deal_details(deal_id):
    """Obtém detalhes do negócio no Bitrix usando a API crm.deal.get"""
    url = f"{BITRIX_WEBHOOK_URL}crm.deal.get.json"
    params = {"id": deal_id}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        deal_data = response.json().get("result")
        if deal_data:
            return deal_data
    return None


def update_city_state(deal_id, cep):
    """Envia os dados para atualizar a cidade e o estado"""
    url = CHANGE_ADDRESS_URL.format(deal_id, cep)
    response = requests.get(url)

    if response.status_code == 200:
        print(f"✅ Atualização bem-sucedida para ID {deal_id} com CEP {cep}.")
        return jsonify({"status": "success", "message": "City and state updated"}), 200
    else:
        print(f"❌ Falha ao atualizar cidade e estado para ID {deal_id}.")
        return jsonify({"status": "error", "message": "Failed to update city/state"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=999, debug=True)
