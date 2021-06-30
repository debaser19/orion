import requests
import config

def get_resellers():
    url = 'https://iaas.cloudcopartner.com/admin/api/v1/resellers/'
    headers = {'Authorization': f'Bearer {config.admin_api_key}'}

    r = requests.get(url, headers=headers)

    return r.json()

    
def get_orgs():
    resellers = get_resellers()
    for r in resellers:
        if r['name'] == '3CX Private Cloud':
            reseller_id = r['id']
            url = f'https://iaas.cloudcopartner.com/admin/api/v1/resellers/{reseller_id}/organizations'
            headers = {'Authorization': f'Bearer {config.admin_api_key}'}

            r = requests.get(url, headers=headers)

            return r.json()

def format_org_list():
    orgs = [ org['name'] for org in get_orgs() ]
    orgs.sort()

    return orgs