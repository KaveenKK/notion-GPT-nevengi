from flask import Flask, jsonify, request
from notion_client import Client
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Auth keys
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
API_KEY = os.getenv("API_KEY")  # Your custom secret token

# Pages to load (comma-separated)
PAGE_IDS = os.getenv("PAGE_IDS", "").split(",")

notion = Client(auth=NOTION_TOKEN)

@app.route("/get-all-notes", methods=["GET"])
def get_all_notes():
    # Auth check
    client_token = request.headers.get("Authorization", "")
    if client_token != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401

    all_notes = []

    try:
        for page_id in PAGE_IDS:
            response = notion.blocks.children.list(page_id.strip())
            for block in response["results"]:
                block_type = block.get("type")
                block_data = block.get(block_type, {})

                if "rich_text" in block_data:
                    for rt in block_data["rich_text"]:
                        text = rt.get("plain_text", "").strip()
                        if text:
                            all_notes.append(text)

        return jsonify({
            "status": "success",
            "summary": "\n".join(all_notes)
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
