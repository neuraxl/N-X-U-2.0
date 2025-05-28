from flask import Flask, request, jsonify
from datetime import datetime
import json
import threading

app = Flask(__name__)
LOG_FILE = "hive_logs.json"

# Mémoire temporaire pour l'analyse
conversation_log = []

# Enregistrement d'un message
@app.route("/log", methods=["POST"])
def log_message():
    data = request.json
    message = {
        "bot": data.get("bot"),
        "message": data.get("message"),
        "timestamp": datetime.now().isoformat()
    }
    conversation_log.append(message)

    # Sauvegarde sur disque
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(message) + "\n")

    return jsonify({"status": "logged"}), 200

# Analyse simple : sujet dominant (placeholder)
@app.route("/analyze", methods=["GET"])
def analyze():
    if not conversation_log:
        return jsonify({"error": "Aucune donnée"}), 400

    bots = [m["bot"] for m in conversation_log]
    topics = [m["message"] for m in conversation_log]

    summary = {
        "nb_messages": len(conversation_log),
        "bots_involved": list(set(bots)),
        "last_topic": topics[-1] if topics else None,
        "last_bot": bots[-1] if bots else None
    }

    return jsonify(summary), 200

if __name__ == "__main__":
    print("🧠 NeuraX-core online... Mémoire en éveil.")
    app.run(port=5005)
