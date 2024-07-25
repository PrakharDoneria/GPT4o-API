from flask import Flask, request, jsonify
from g4f.client import Client

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello World</h1>'

@app.route('/gpt4o', methods=['GET'])
def gpt4o():
    return get_ai_response("gpt-4o")

@app.route('/geminipro', methods=['GET'])
def geminipro():
    return get_ai_response("geminipro")

@app.route('/llama', methods=['GET'])
def llama():
    return get_ai_response("llama")

@app.route('/metaai', methods=['GET'])
def metaai():
    return get_ai_response("metaai")

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
            return jsonify({"response": response.choices[0].message.content})
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
