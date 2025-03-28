# Generate a private key
#openssl genrsa -out private_key.pem 2048
# Extract the public key
#openssl req -new -x509 -key private_key.pem -out public.pem -subj '/CN=SandboxTester'
# Get the fingerprint
#openssl x509 -noout -fingerprint -sha1 -inform pem -in public.pem

import os
import json
import time
import jwt
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import uuid

CLIENT_ID = "omitted"  #Staging
# TOKEN_URL = 'https://oauthserver.eclinicalworks.com/oauth/oauth2/token'    #Production
TOKEN_URL = "https://staging-oauthserver.ecwcloud.com/oauth/oauth2/token"  #Staging
# AUTH_URL = 'https://oauthserver.eclinicalworks.com/oauth/oauth2/authorize' #Production
AUTH_URL = "https://staging-oauthserver.ecwcloud.com/oauth/oauth2/authorize" #Staging

JWKS_URL = "omitted"

# Path to the private key file
private_key_file = "private_key.pem"

# Read the private key from the file
with open(private_key_file, "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )


# Generate a signed JWT with RS384
def generate_jwt():
    now = int(time.time())
    exp = now + 300  # Expiration time no more than five minutes in the future
    claims = {
        "iss": CLIENT_ID,
        "sub": CLIENT_ID,
        "aud": TOKEN_URL,
        "exp": exp,
        "iat": now,
        "jti": str(uuid.uuid4())  # Generate a unique JWT ID
    }
    headers = {
        "alg": "RS384",
        "kid": "omitted",
        "typ": "JWT",
        "jku": JWKS_URL  # Optional, if your JWK Set URL is available
    }
    token = jwt.encode(
        payload=claims,
        key=private_key,
        algorithm="RS384",
        headers=headers
    )
    print("Generated JWT:", token)  # Debugging line to check the JWT
    return token


# Function to get a new access token using JWT
def get_access_token():
    signed_jwt = generate_jwt()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'scope': 'system/Patient.read system/Encounter.read system/Group.read',  # Adjust scope as needed
        'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
        'client_assertion': signed_jwt
    }

    print("Request Headers:", headers)  # Debugging line to check headers
    print("Request Data:", data)  # Debugging line to check data

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.text)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    return response.json()['access_token']

# Attempt to get the access token
try:
    access_token = get_access_token()
    print("Access Token:", access_token)
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
    print(f"Response content: {err.response.content}")
except Exception as err:
    print(f"Other error occurred: {err}")
