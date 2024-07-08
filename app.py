from flask import Flask,request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv


#initializing the Flask Application
app = Flask(__name__)

load_dotenv

#Safaricom Api credentials
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
# base_url='https://darajaflaskapp-2.onrender.com'


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
# @app.route('/register_urls')
# def register():
#     mpesa_endpoint="https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
#     headers = {"Authorization": "Bearer %s" % access_token()}
#     response_data = requests.post(
#         mpesa_endpoint,
#           json={
#               "ShortCode":"600992",
#                "ResponseType":"Completed",
#                "confirmationURL": base_url +"/cb2/confirm",
#                "ValidationURL": base_url + "/cb2/validation"
#           },
#           headers = headers
#           )
    
#     return response_data.json()

# @app.route('/c2b/confirm', methods=['POST'])
# def confirm():
#     # Get JSON data from the request
#     data = request.get_json()
    
#     # Write data to file
#     with open('confirm.json', 'a') as file:
#         json.dump(data, file)
#         file.write('\n')  # Add a newline for readability between entries
    
#     # Return a response (Safaricom expects a specific format)
#     return jsonify({"ResultCode": 0, "ResultDesc": "Confirmation received successfully"}), 200

# @app.route('/c2b/validation', methods=['POST'])
# def validation():
#     # Get JSON data from the request
#     data = request.get_json()
    
#     # Write data to file
#     with open('validation.json', 'a') as file:
#         json.dump(data, file)
#         file.write('\n')  # Add a newline for readability between entries
    
#     # Return a response (Safaricom expects a specific format)
#     return jsonify({"ResultCode": 0, "ResultDesc": "Validation received successfully"}), 200



    

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
    app.run(host ="0.0.0.0", port = 8000, debug=True)