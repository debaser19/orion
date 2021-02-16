import requests
import json
import config


def createInstance():
    # lets create an instance
    url = 'https://iaas.cloudcopartner.com/api/v1/instances'
    headers = {'Authorization': f'Bearer {end_user_api_key}'}

    # create the payload
    payload = {
        'name': 'test server',
        'instance_performance_tier': '60735938-af5d-49b3-ae32-f585cf70196c',
        'disk_performance_tier': '9c8b5610-b2fa-4196-9556-e3b0d0e05cd9',
        'memory': 2048,
        'region': 'dabba812-0f2a-4648-a426-95e9a62f25f7',
        'size': 10,
        'template': 'debian-10'
    }

    r = requests.post(url, headers=headers, json=payload)
    print(json.dumps(r.json(), indent=4))


if __name__ == '__main__':
    admin_api_key = config.admin_api_key
    end_user_api_key = config.end_user_api_key
    print('hello world')