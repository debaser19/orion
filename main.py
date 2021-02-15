import requests
import config
import json
import pandas as pd


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


def getResellers():
    url = 'https://iaas.cloudcopartner.com/admin/api/v1/resellers/'
    headers = {'Authorization': f'Bearer {admin_api_key}'}

    r = requests.get(url, headers=headers)

    return r.json()

    
def getOrgs():
    resellers = getResellers()
    for r in resellers:
        if r['name'] == '3CX Private Cloud':
            reseller_id = r['id']
            url = f'https://iaas.cloudcopartner.com/admin/api/v1/resellers/{reseller_id}/organizations'
            headers = {'Authorization': f'Bearer {admin_api_key}'}

            r = requests.get(url, headers=headers)

            return r.json()


def createApplication(org_id, org_name, reseller_id):
    headers = {
        'Authorization': f'Bearer {admin_api_key}',
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


def listInstances():
    # TODO: Set this up to take org id as a parameter
    orgs = getOrgs()
    instances_list = []

    # loop through orgs
    for o in orgs:
        headers = {
            'Authorization': f'Bearer {admin_api_key}',
            'Content-Type': 'application/json'
        }
        org_id = o['id']
        reseller_id = o['reseller_id']
        # if o['name'] == input_org:
        # get org name
        url = f'https://iaas.cloudcopartner.com/admin/api/v1/resellers/{reseller_id}/organizations/{org_id}'
        org_request = requests.get(url, headers=headers)
        org_name = org_request.json()['name']

        # check if we already have a token
        print(f'Checking for Application in org: {o["name"]}')
        url = f'https://iaas.cloudcopartner.com/admin/api/v1/resellers/{reseller_id}/organizations/{org_id}/applications'
        app_request = requests.get(url, headers=headers)
        applications = app_request.json()
        token_present = False
        for a in applications:
            if f'{org_name}_token' in a['name']:
                token_present = True
                token = a
        
        if not token_present:
            print('No token found, creating one now')
            token = createApplication(org_id, org_name, reseller_id)
        else:
            print('Already have a token, skipping token creation')

        client_id = token['client_id']
        client_secret = token['client_secret']

        # get the oauth token
        print('Reaching out for OAuth token')
        oauth_token = getOauthToken(client_id, client_secret)

        # list the instances
        headers = {'Authorization': f'Bearer {oauth_token}'}
        url = 'https://iaas.cloudcopartner.com/api/v1/instances'

        instance_request = requests.get(url, headers=headers)
        instances = instance_request.json()
        
        print(f'Found {len(instances)} instance(s) for {org_name}')

        # loop through found instances and pull details
        for i in instances:
            # try to get ip address
            wan_ip = ''
            lan_ip = ''
            try:
                for adapter in i['network_adapters']:
                    if adapter['network']['is_public']:
                        wan_ip = adapter['ip_addresses'][0]['address']
                    else:
                        lan_ip = adapter['ip_addresses'][0]['address']
            except:
                print('Could not grab IP info')
            
            # get boot disk template
            template = ''
            try:
                template = i['disks'][0]['template']['name']
            except:
                print(f'Found no disks for instance {i["name"]}')

            instance_dict = {
                'org_name': org_name,
                'instance_name': i['name'],
                'memory': i['memory'],
                'performance_tier': i['performance_tier']['name'],
                'region': i['region']['name'],
                'template': template,
                'wan_ip': wan_ip,
                'lan_ip': lan_ip,
                'state': i['state']
            }

            instances_list.append(instance_dict)
            print(instance_dict)

    # convert list of instances to csv
    instance_df = pd.DataFrame(instances_list)
    instance_df.to_csv('instances.csv', index=False)


def getOauthToken(client_id, client_secret):
    url = 'https://cloud.orionvm.com/oauth/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    r = requests.post(url, json=payload)
    oauth_token = r.json()

    return oauth_token['access_token']


if __name__ == '__main__':
    admin_api_key = config.admin_api_key
    end_user_api_key = config.end_user_api_key
    listInstances()
