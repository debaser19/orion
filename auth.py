import requests
import config


def create_application(org_id, org_name, reseller_id):
    headers = {
        'Authorization': f'Bearer {config.admin_api_key}',
        'Content-Type': 'application/json'
    }
    
    # create the application if we don't have one yet
    payload = {'name': f'{org_name}_token'}
    url = f'https://iaas.cloudcopartner.com/admin/api/v1/resellers/{reseller_id}/organizations/{org_id}/applications'
    r = requests.post(url, headers=headers, json=payload)

    # grab list of applications and return the client id and secret for the matching application name
    tokens = requests.get(url, headers=headers)
    for t in tokens.json():
        if t['name'] == f'{org_name}_token':
            return t


def get_oauth_token(client_id, client_secret):
    url = 'https://cloud.orionvm.com/oauth/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    r = requests.post(url, json=payload)
    oauth_token = r.json()

    return oauth_token['access_token']