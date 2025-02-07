from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/handler", methods=["POST"])
def handle_webhook():
    data = request.json  # Captura os dados enviados pela Bitrix
    
    # Supondo que o ID esteja em data['id']
    if "data" in data and "id" in data["data"]:
        event_id = data["data"]["id"]
        print(f"ID do evento recebido: {event_id}")
        
        # (Opcional) Salva o ID e dados em um arquivo de log
        with open("bitrix_log.txt", "a") as log_file:
            log_file.write(f"Evento ID: {event_id} - Dados: {data}\n")
    else:
        print("ID não encontrado no payload.")
    
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=999, debug=True)
