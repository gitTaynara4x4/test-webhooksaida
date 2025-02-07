from flask import Flask, request, jsonify

app = Flask(__name__)

VALID_TOKEN = "8i5l6yr9laqc0oi2y06vu1eg6003koo7"

@app.route("/handler", methods=["POST", "GET"])
def handle_webhook():
    if request.method == "GET":
        return jsonify({"status": "Webhook ativo! Use POST para enviar dados."}), 200
    
    token = request.headers.get('Authorization')
    if token != f"Bearer {VALID_TOKEN}":
        print("⚠️ Token inválido!")
        return jsonify({"status": "Unauthorized"}), 401

    data = request.json
    print("🔔 Webhook recebido:", data)

    # Extraindo o ID do card e a mudança feita
    card_id = data.get("data[FIELDS][ID]", "ID não encontrado")
    changes = data.get("data[FIELDS]", {})

    print(f"📝 ID do Card: {card_id}")
    print(f"🔄 Mudanças feitas: {changes}")

    with open("bitrix_log.txt", "a") as log_file:
        log_file.write(f"ID do Card: {card_id}\n")
        log_file.write(f"Mudanças: {changes}\n")
        log_file.write(str(data) + "\n\n")

    return jsonify({"status": "success", "card_id": card_id, "changes": changes}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=999, debug=True)
