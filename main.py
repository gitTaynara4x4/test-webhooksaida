from flask import Flask, request, jsonify

app = Flask(__name__)

# Token de segurança (substitua pelo token real)
VALID_TOKEN = "8i5l6yr9laqc0oi2y06vu1eg6003koo7"

# Rota que irá tratar os eventos de webhook
@app.route("/handler", methods=["POST"])
def handle_webhook():
    print(f"🔔 Requisição recebida: {request.method} {request.path}")
    
    # Verifique o token no cabeçalho da requisição
    token = request.headers.get('Authorization')  # Se o token estiver no cabeçalho Authorization
    
    if token != f"Bearer {VALID_TOKEN}":
        print("⚠️ Token inválido!")
        return jsonify({"status": "Unauthorized"}), 401

    if request.method == "POST":
        # Captura os dados do webhook enviados pela Bitrix
        data = request.json
        
        # Log no terminal para ver os dados
        print("🔔 Webhook recebido:", data)
        
        # Salva os dados em um arquivo de log (bitrix_log.txt)
        with open("bitrix_log.txt", "a") as log_file:
            log_file.write(str(data) + "\n")
        
        # Responde com sucesso
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "method not allowed"}), 405

# Inicia a aplicação Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=999, debug=True)
