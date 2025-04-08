from flask import Flask, jsonify
from notion_client import Client
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()

app = Flask(__name__)
CORS(app)  # Allows API calls from anywhere

# Retrieve the Notion integration token from the environment
notion_token = os.getenv("NOTION_TOKEN")
if not notion_token:
    raise Exception("NOTION_TOKEN is not set in the environment variables.")

# Instantiate the Notion client with the token
notion = Client(auth=notion_token)

@app.route("/get-notes/<string:page_id>", methods=["GET"])
def get_notes(page_id):
    try:
        # Get all content blocks from the Notion page
        response = notion.blocks.children.list(page_id)
        notes = []

        for block in response["results"]:
            block_type = block.get("type")

            if block_type and block_type in block:
                block_content = block[block_type]
                
                if "rich_text" in block_content:
                    for rt in block_content["rich_text"]:
                        plain_text = rt.get("plain_text", "").strip()
                        if plain_text:
                            notes.append(plain_text)

                elif "text" in block_content:  # fallback for blocks using "text" key
                    for t in block_content["text"]:
                        plain_text = t.get("plain_text", "").strip()
                        if plain_text:
                            notes.append(plain_text)

        return jsonify({
            "status": "success",
            "summary": "\n".join(notes)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
