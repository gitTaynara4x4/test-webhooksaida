from flask import Flask, request, jsonify

app = Flask(__name__)

VALID_TOKEN = "8i5l6yr9laqc0oi2y06vu1eg6003koo7"

@app.route("/handler", methods=["POST"])
def handle_webhook():
    print(f"🔔 Requisição recebida: {request.method} {request.path}")

    token = request.headers.get('Authorization')
    print(f"🔑 Token recebido: {token}")  # Debug para verificar se o token vem corretamente

    if not token or token.strip() != f"Bearer {VALID_TOKEN}":
        print("⚠️ Token inválido!")
        return jsonify({"status": "Unauthorized"}), 401

    data = request.json
    print("🔔 Webhook recebido:", data)

    # Tenta capturar o ID corretamente
    card_id = None
    if data.get("data", {}).get("FIELDS", {}).get("ID"):
        card_id = data["data"]["FIELDS"]["ID"]
    elif data.get("document_id") and len(data["document_id"]) >= 3:
        card_id = data["document_id"][2].replace("DEAL_", "")  # Remove "DEAL_"

    if not card_id:
        print("⚠️ Nenhum ID encontrado no payload!")
        return jsonify({"status": "error", "message": "ID não encontrado"}), 400

    changes = data.get("data", {}).get("FIELDS", {})

    print(f"📝 ID do Card: {card_id}")
    print(f"🔄 Mudanças feitas: {changes}")

    with open("bitrix_log.txt", "a") as log_file:
        log_file.write(f"ID do Card: {card_id}\n")
        log_file.write(f"Mudanças: {changes}\n")
        log_file.write(str(data) + "\n\n")

    return jsonify({"status": "success", "card_id": card_id, "changes": changes}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=999, debug=True, threaded=True)
