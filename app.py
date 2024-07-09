from flask import Flask,request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import base64


#initializing the Flask Application
app = Flask(__name__)

load_dotenv()

#Safaricom Api credentials
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
base_url='https://darajaflaskapp-4.onrender.com'


#creating home route
@app.route('/')
def home():
    return "Welcome to the safaricom access token generator"

#creating access token route
@app.route('/access_token')
def token():
    data = access_token()
    return data


#registering urls
@app.route('/register_urls')
def register():
    mpesa_endpoint="https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    #setting up the authorization header with the access token
    headers = {"Authorization": f"Bearer {access_token()}"}
    #sending a POST request
    response_data = requests.post(
        mpesa_endpoint,
          json={
              "ShortCode":"600997",
               "ResponseType":"Completed",
               "ConfirmationURL": f"{base_url}/c2b/confirm",
               "ValidationURL": f"{base_url}/c2b/validation"
          },
          headers = headers
          )
    #Return the Json response from Safaricom's API
    return response_data.json()

@app.route('/c2b/confirm', methods=['POST'])
def confirm():
    # Get JSON data from the request
    data = request.get_json()
    
    # Write data to file
    with open('confirm.json', 'a') as file:
        json.dump(data, file)
        file.write('\n')  # Add a newline for readability between entries
    
    # Return a response (Safaricom expects a specific format)
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200

@app.route('/c2b/validation', methods=['POST'])
def validation():
    # Get JSON data from the request
    data = request.get_json()
    
    # Write data to file
    with open('validation.json', 'a') as file:
        json.dump(data, file)
        file.write('\n')  # Add a newline for readability between entries
    
    # Return a response (Safaricom expects a specific format)
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200

#Simulating transaction
@app.route('/simulate')
def simulate():
    mpesa_endpoint = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate'
    headers = {"Authorization": f"Bearer {access_token()}"}
    request_body = {
         "ShortCode":600998,
         "CommandID": "CustomerPayBillOnline",
         "Amount": 1,
         "Msisdn": 254708374149,
         "BillRefNumber": "Test",
    }

    simulate_response = requests.post(mpesa_endpoint, json= request_body, headers=headers)

    return simulate_response.json()

#initiate Mpesa express resquest
@app.route('/pay')
def MpesaExpress():
    amount = request.args.get('amount')
    phone = request.args.get('phone')
    endpoint ='https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {"Authorization": f"Bearer {access_token()}"}
    Timestamp = datetime.now()
    times = Timestamp.strftime("%Y%m%d%H%M%S")
    password = "174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + times
    password = base64.b64encode(password.encode('utf-8') ).decode('utf-8')

    data = {
        "BusinessShortCode":"174379",
        "Password":password,
        "Timestamp":times,
        "TransactionType":"CustomerPaybillOnline",
        "PartyA":phone,
        "PartyB":"174379",
        "PhoneNumber":phone,
        "CallBackURL": f"{base_url}/lnmo-callback",
        "AccountReference":"TestPay",
        "TransactionDesc":"HelloTest",
        "Amount":amount

    }

    res = requests.post(endpoint, json=data, headers= headers)
    return res.json()

#consume Mpesa express callback
@app.route('/lmno-callback', methods=["POST"])
def incoming():
    data = request.get_json()
    print(data)
    return "ok"
    
#function to get access token
def access_token():
    #defining headers for the HTTP request
    # headers = {
    #     'Content-Type': 'application/json; charset=utf8'
    
    # }
    #Safaricom OAuth token endpoint
    mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    #Making a Get request to the Safaricom API
    #Parsing the JSON response
    #using the HTTP Basic Auth with the consumer key and secret
    data = (requests.get(mpesa_auth_url, auth = HTTPBasicAuth(consumer_key, consumer_secret) )).json()

    #Return the Json Data which has the access token
    return data['access_token']
       


#Ensure app runs only if script is executed directly
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host="0.0.0.0", port=port, debug=True)