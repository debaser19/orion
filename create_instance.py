import requests
import json
import config


def create_instance(oauth_token, payload):
    # lets create an instance
    url = 'https://3cx.iaas.cloudcopartner.com/api/v1/instances'
    headers = {
        'Authorization': f'Bearer {oauth_token}',
        'Content-Type': 'application/json'
        }
    print(headers)
    print(payload)

    r = requests.post(url, headers=headers, json=payload)
    print(json.dumps(r.json(), indent=4))