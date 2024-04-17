'''
Created on 13-Apr-2024

@author: User
'''
# Import the required module from the fyers_apiv3 package
from fyers_apiv3 import fyersModel

# Replace these values with your actual API credentials
client_id = "N3VPS274OH-100"
secret_key = "MONNT2QWHX"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
response_type = "code"  
state = "sample_state"
grant_type = "authorization_code"  

# Create a session model with the provided credentials
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type,
    grant_type=grant_type
    
)

# Generate the auth code using the session model
auth_codeURL = session.generate_authcode()
print(auth_codeURL)
auth_code=input("Enter auth code: ")
# Set the authorization code in the session object
session.set_token(auth_code)

# Generate the access token using the authorization code
response = session.generate_token()["access_token"]

# Print the response, which should contain the access token and other details
print(response)