from flask import Flask, jsonify
from notion_client import Client
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows you to call this API from GPT or anywhere

# 🪄 Your Notion integration token (the "secret_xxx" value)
notion = Client(auth="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")

@app.route("/get-notes/<string:page_id>", methods=["GET"])
def get_notes(page_id):
    try:
        # Get all content blocks from the page
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

                elif "text" in block_content:  # fallback
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
