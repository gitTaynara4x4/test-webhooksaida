from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/handler", methods=["POST"])
def handle_webhook():
    data = request.json  # Captura os dados enviados pela Bitrix
    print("🔔 Webhook recebido:", data)

    # (Opcional) Salva os dados em um arquivo de log
    with open("bitrix_log.txt", "a") as log_file:
        log_file.write(str(data) + "\n")

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=999, debug=True)
