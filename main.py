from flask import Flask, request, jsonify
from g4f.client import Client 
import google.generativeai as genai
import os
import requests

app = Flask(__name__)

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

@app.route('/')
def hello_world():
    return '<h1>v1.2.1.1</h1>'

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

response = None

@app.route('/geminiAdvance', methods=['GET'])
def gemini_advance():
    global response
    try:
        prompt = request.args.get('prompt')
        if not prompt:
            return jsonify({"reply": "No prompt provided"}), 400

        model = genai.GenerativeModel('gemini-1.0-pro-latest')
        response = model.generate_content(prompt)

        if response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "Failed to get response from the model"}), 500
    except KeyError as e:
        return jsonify({"reply": response}), 500
    except ValueError as e:
        return jsonify({"reply": response}), 500
    except Exception as e:
        return jsonify({"reply": response}), 500

gpt4_response = None

@app.route('/gpt4', methods=['GET'])
def gpt4():
    global gpt4_response
    try:
        prompt = request.args.get('prompt')
        if not prompt:
            return jsonify({"reply": "No prompt provided"}), 400

        gpt4_response = requests.get(f"https://alexapi.69dev.id/v1/gpt4-32k.php?text={prompt}")
        if gpt4_response.status_code == 200:
            response_data = gpt4_response.json()
            if response_data.get("ok"):
                return jsonify({"reply": response_data.get("response")})
            else:
                return jsonify({"reply": "Failed to get response from external API"}), 500
        else:
            return jsonify({"reply": f"External API request failed with status code {gpt4_response.status_code}"}), 500
    except Exception:
        return jsonify({"reply": gpt4_response}), 500
        

@app.route('/generate', methods=['GET'])
def generate():
    try:
        prompt = request.args.get('prompt')
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        client = Client()
        response = client.images.generate(
            model="gemini",
            prompt=prompt,
        )

        if response.data:
            image_url = response.data[0].url
            return jsonify({"image_url": image_url})
        else:
            return jsonify({"error": "Failed to generate image"}), 500
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

        if response['choices']: 
            return jsonify({"reply": response['choices'][0]['message']['content']})
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