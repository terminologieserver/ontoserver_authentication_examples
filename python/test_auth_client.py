import requests, logging

logging.basicConfig(
            level="INFO",
            # filename='log.txt',
            format='Authorization @ %(asctime)s ~ %(levelname)s:%(message)s',
            datefmt='%m/%d/%Y %I:%M:%S%p'
            )

url = "https://terminologieserver.nl/auth/realms/nictiz/.well-known/openid-configuration"
logging.info(f"Retrieving {url}")
request = requests.get( url).json()
auth_endpoint = request.get('authorization_endpoint')
token_endpoint = request.get('token_endpoint')
logout_endpoint = request.get('end_session_endpoint')

logging.info(f"Auth endpoint: \t{auth_endpoint}")
logging.info(f"Token endpoint: \t{token_endpoint}")

data = {
    "grant_type"    : "client_credentials",
    "client_id"     : input("Client ID: "),
    "client_secret" : input("Client secret: "),
}
request = requests.post(token_endpoint, data=data)
response = request.json()
token = response.get('access_token')
logging.info(f"Token: {token}")

logging.info("-"*60)
logging.info("*** Inloggen ***")
logging.info(f"Retrieving \t{token_endpoint}")
logging.info(f"Status code: {request.status_code}")
if request.status_code is not 200:
    logging.critical("Response not 200")
    logging.critical(response)
    exit()
logging.info(f"Type: \t\t\t{response.get('token_type')}")
logging.info(f"expires_in: \t\t{response.get('expires_in')}")
logging.info(f"refresh_expires_in: \t{response.get('refresh_expires_in')}")
logging.info("-"*60)
logging.info("")

# Zoek naar CodeSystem met naam nullflavor
headers = {
    "Authorization": "Bearer "+token,
    "Content-Type" : "application/fhir+json",
}
req_url = f"https://terminologieserver.nl/fhir/CodeSystem?name=snomed"
request = requests.get(req_url, headers=headers)
response = request.json()

logging.info("-"*60)
logging.info(f"Request URL: {req_url}")
logging.info(f"Status code: {request.status_code}")
if request.status_code is not 200:
    logging.critical("Response not 200")
    logging.critical(response)
    exit()
logging.info("-"*60)
logging.info(f"Resultaten: {response.get('total')}")

count=0
for entry in response.get('entry',[]):
    count+=1
    logging.info("-"*60)
    logging.info(f"Resultaat {count}")
    logging.info(f"\tURL: \t\t{entry.get('resource').get('url')}")
    logging.info(f"\tVersion: \t{entry.get('resource').get('version')}")
    logging.info(f"\tIdentifier: \t{entry.get('resource').get('identifier')}")
    logging.info(f"\tSecurity tags: \t{entry.get('resource').get('meta',{}).get('security')}")
logging.info("")

# Uitloggen
logging.info("-"*60)
logging.info(f"*** Uitloggen ***")
headers = {
    "Authorization": "Bearer "+token,
    "Content-Type" : "application/fhir+json",
}
req_url = logout_endpoint
response = requests.get(req_url, headers=headers)
logging.info(f"Status code: {response.status_code}")
if request.status_code is not 200:
    logging.critical("Response not 200")
    logging.critical(response)
    exit()
logging.info("-"*60)
