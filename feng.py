import requests
import json

# Make the authorize call
data = {"key1": "value1", "key2": "value2"}
headers = {"Content-Type": "application/json"}
url = "http://localhost:3000/api/server/authorize"
response = requests.post(url, json=data, headers=headers)
authorize_token = ''
if response.status_code == 200:
    print("Request successful!")
    print(response.json())
    resp = response.json()
    authorize_token = resp['authorize_token']
    print('Authorize Token= ' + authorize_token)
else:
    print(f"Error: {response.status_code}")
    print(response.text)

print('Lets try the next call..');


# Make the get token call

data = {"authorize_token": authorize_token }
headers = {"Content-Type": "application/json"}
url = "http://localhost:3000/api/gettoken"
response = requests.post(url, json=data, headers=headers)
access_token = ''
if response.status_code == 200:
    print("Request successful!")
    print(response.json())
    resp = response.json()
    access_token = resp['access_token']
    print('Access Token= ' + access_token)
else:
    print(f"Error: {response.status_code}")
    print(response.text)

print('Lets try to get data call..');


# Make the get token call

data = {"Authorization": 'Bearer ' + access_token }
headers = {"Content-Type": "application/json", }
url = "http://localhost:3000/api/getdata/az-function-app-java"
response = requests.get(url, headers=headers)
access_token = ''
if response.status_code == 200:
    print("Request successful!")
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)
