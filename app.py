from flask import Flask, jsonify, request, make_response, render_template
import requests
from ramen_data import BROTHS, PROTEINS

app = Flask(__name__)

API_KEY = "ZtVdh8XQ2U8pWI2gmZ7f796Vh8GllXoN7mr0djNf"
ORDER_ID_ENDPOINT = "https://api.tech.redventures.com.br/orders/generate-id"

def validate_api_key(request):
    api_key = request.headers.get('x-api-key')
    if not api_key:
        return False, make_response(jsonify({"error": "x-api-key header missing"}), 403)
    if api_key != API_KEY:
        return False, make_response(jsonify({"error": "Invalid API key"}), 403)
    return True, None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/broths', methods=['GET'])
def get_broths():
    valid, response = validate_api_key(request)
    if not valid:
        return response
    return make_response(jsonify(BROTHS), 200)

@app.route('/proteins', methods=['GET'])
def get_proteins():
    valid, response = validate_api_key(request)
    if not valid:
        return response
    return make_response(jsonify(PROTEINS), 200)

@app.route('/order', methods=['POST'])
def create_order():
    valid, response = validate_api_key(request)
    if not valid:
        return response
    
    data = request.json
    if not data or not all(key in data for key in ("brothId", "proteinId")):
        return make_response(jsonify({"error": "both brothId and proteinId are required"}), 400)
    
    response = requests.post(
        ORDER_ID_ENDPOINT,
        headers={"x-api-key": API_KEY}
    )
    
    if response.status_code != 200:
        return make_response(jsonify({"error": "could not place order"}), 500)
    
    order_id = response.json().get("orderId")
    description = f"{BROTHS[int(data['brothId']) - 1]['name']} and {PROTEINS[int(data['proteinId']) - 1]['name']} Ramen"
    image = "https://tech.redventures.com.br/icons/ramen/ramenChasu.png"  # Example image URL
    
    return make_response(jsonify({
        "id": order_id,
        "description": description,
        "image": image
    }), 201)

if __name__ == '__main__':
    app.run(debug=True)
