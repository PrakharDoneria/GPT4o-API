from flask import Flask, request, jsonify
from g4f.client import Client
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello World</h1>'

@app.route('/gpt4o', methods=['GET'])
def gpt4o():
    return get_ai_response("gpt-4o")

@app.route('/advance', methods=['POST'])
def advance():
    try:
        data = request.get_json()
        if not data or "messages" not in data:
            return jsonify({"error": "Invalid input, 'messages' field is required"}), 400

        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=data["messages"],
        )

        if response.choices:
            return jsonify({"reply": response.choices[0].message.content})
        else:
            return jsonify({"error": "Failed to get response from the model"}), 500
    except KeyError as e:
        return jsonify({"error": f"KeyError: {str(e)}"}), 500
    except ValueError as e:
        return jsonify({"error": f"ValueError: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/geminiAdvance', methods=['GET'])
def gemini_advance():
    return get_ai_response("gemini-pro")

@app.route('/gpt4', methods=['GET'])
def gpt4():
    try:
        prompt = request.args.get('prompt')
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        response = requests.get(f"https://alexapi.69dev.id/v1/gpt4-32k.php?text={prompt}")
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("ok"):
                return jsonify({"reply": response_data.get("response")})
            else:
                return jsonify({"error": "Failed to get response from external API"}), 500
        else:
            return jsonify({"error": f"External API request failed with status code {response.status_code}"}), 500
    except KeyError as e:
        return jsonify({"error": f"KeyError: {str(e)}"}), 500
    except ValueError as e:
        return jsonify({"error": f"ValueError: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

def get_ai_response(model_name):
    try:
        prompt = request.args.get('prompt')
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        client = Client()
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )

        if response.choices:
            return jsonify({"reply": response.choices[0].message.content})
        else:
            return jsonify({"error": f"Failed to get response from {model_name}"}), 500
    except KeyError as e:
        return jsonify({"error": f"KeyError: {str(e)}"}), 500
    except ValueError as e:
        return jsonify({"error": f"ValueError: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
