import requests
import config


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


def check_token(org_name, org_id):
    # check if we already have a token
    print(f'Checking for Application in org: {org_name}')
    headers = {'Authorization': f'Bearer {config.admin_api_key}'}
    url = f'https://iaas.cloudcopartner.com/admin/api/v1/resellers/{config.reseller_3cx}/organizations/{org_id}/applications'
    app_request = requests.get(url, headers=headers)
    applications = app_request.json()
    token_present = False
    for a in applications:
        if f'{org_name}_token' in a['name']:
            token_present = True
            token = a
    
    if not token_present:
        print('No token found, creating one now')
        token = create_application(org_id, org_name, config.reseller_3cx)
    else:
        print('Already have a token, skipping token creation')

    client_id = token['client_id']
    client_secret = token['client_secret']

    # get the oauth token
    print('Reaching out for OAuth token')
    oauth_token = get_oauth_token(client_id, client_secret)
    
    if oauth_token:
        print(f'Received OAuth token: {oauth_token}')
    else:
        print('Did not receive OAuth token')

    return oauth_token