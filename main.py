from flask import Flask, request, jsonify

app = Flask(__name__)

# Rota que irá tratar os eventos de webhook
@app.route("/handler", methods=["POST"])
def handle_webhook():
    print("🔔 Rota /handler foi chamada!")
    
    # Captura os dados do webhook enviados pela Bitrix
    data = request.json
    
    # Log no terminal para ver os dados
    print("🔔 Webhook recebido:", data)
    
    # Salva os dados em um arquivo de log (bitrix_log.txt)
    with open("bitrix_log.txt", "a") as log_file:
        log_file.write(str(data) + "\n")
    
    # Responde com sucesso
    return jsonify({"status": "success"}), 200

# Inicia a aplicação Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=999, debug=True)
