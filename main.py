from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

@app.route("/handler", methods=["POST"])
def handle_webhook():
    data = request.json  # Captura os dados enviados pela Bitrix
    event = data.get("event")  # Captura o tipo de evento
    event_data = json.dumps(data.get("data", {}), indent=4)  # Obtém os dados do evento de forma legível
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Captura o timestamp do evento

    log_message = f"[{timestamp}] Evento: {event} - Dados: {event_data}\n"

    # Exibe os dados no console para debug
    print(log_message)

    # Salva os dados no arquivo de log
    with open("bitrix_log.txt", "a") as log_file:
        log_file.write(log_message)

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=999, debug=True)
