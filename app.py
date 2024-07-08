from flask import Flask,request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv


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
    return jsonify({"ResultCode": 0, "ResultDesc": "Confirmation received successfully"}), 200

@app.route('/c2b/validation', methods=['POST'])
def validation():
    # Get JSON data from the request
    data = request.get_json()
    
    # Write data to file
    with open('validation.json', 'a') as file:
        json.dump(data, file)
        file.write('\n')  # Add a newline for readability between entries
    
    # Return a response (Safaricom expects a specific format)
    return jsonify({"ResultCode": 0, "ResultDesc": "Validation received successfully"}), 200



    

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