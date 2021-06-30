import requests
import json
import orgs
import oauth
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


def create_instance(org_name, payload):
    for o in orgs.get_orgs():
        if o['name'] == org_name:
            org_id = o['id']

    # check if we already have a token
    # print(f'Checking for Application in org: {org_name}')
    # print(config.reseller_3cx)
    # headers = {'Authorization': f'Bearer {config.admin_api_key}'}
    # url = f'https://iaas.cloudcopartner.com/admin/api/v1/resellers/{config.reseller_3cx}/organizations/{org_id}/applications'
    # app_request = requests.get(url, headers=headers)
    # applications = app_request.json()
    # token_present = False
    # for a in applications:
    #     if f'{org_name}_token' in a['name']:
    #         token_present = True
    #         token = a
    
    # if not token_present:
    #     print('No token found, creating one now')
    #     token = create_instance.create_application(org_id, org_name, config.reseller_3cx)
    # else:
    #     print('Already have a token, skipping token creation')

    # client_id = token['client_id']
    # client_secret = token['client_secret']

    # get the oauth token
    # print('Reaching out for OAuth token')
    # oauth_token = oauth.get_oauth_token(client_id, client_secret)
    
    # if oauth_token:
    #     print(f'Received OAuth token: {oauth_token}')
    # else:
    #     print('Did not receive OAuth token')

    # Get OAuth Token
    oauth_token = oauth.check_token(org_name, org_id)

    # Create the instance
    url = 'https://3cx.iaas.cloudcopartner.com/api/v1/instances'
    headers = {
        'Authorization': f'Bearer {oauth_token}',
        'Content-Type': 'application/json'
        }
    print(headers)
    print(payload)

    r = requests.post(url, headers=headers, json=payload)
    print(json.dumps(r.json(), indent=4))