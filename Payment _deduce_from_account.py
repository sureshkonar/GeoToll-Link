
from flask import Flask, request, jsonify

app = Flask(__name__)

# Create a dummy account with a starting balance
account = {
    "id": 123,
    "balance": 1000
}

# Define the API endpoint for deducting money from the account
@app.route('/api/deduct', methods=['POST'])
def deduct():
    # Get the input data from the user
    data = request.get_json()
    
    # Validate the input data
    if not data.get("amount"):
        return jsonify({"error": "No amount specified"}), 400
    
    # Check if the user is authorized to access the account
    # You can add your own authentication logic here
    
    # Deduct the specified amount from the account balance
    amount = data["amount"]
    if account["balance"] < amount:
        return jsonify({"error": "Insufficient balance"}), 400
    
    account["balance"] -= amount
    
    # Return a response indicating the transaction was successful
    return jsonify({"message": f"Successfully deducted {amount}"}), 200

if __name__ == '__main__':
    app.run(debug = True)
    app.run(host='0.0.0.0', port=8080)
