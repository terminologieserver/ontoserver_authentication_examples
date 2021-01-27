# Uses python package: python-keycloak (pip install python-keycloak)
from keycloak import KeycloakOpenID, KeycloakAdmin
import requests

# Configure client
keycloak_openid = KeycloakOpenID(server_url="https://terminologieserver.nl/auth/",
                    client_id="cli_client",
                    realm_name="nictiz")
# Get Token
token = keycloak_openid.token(input("Username: "), input("Password: "))
print('TOKEN:', token,'\n')
userinfo = keycloak_openid.userinfo(token['access_token'])
print(userinfo,"\n")


endpoint = "https://terminologieserver.nl/fhir/metadata"
headers = {"Authorization": "Bearer "+token.get('access_token')}
print(requests.get(endpoint, headers=headers).json().get('name'))

keycloak_openid.logout(token['refresh_token'])