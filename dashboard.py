from requests.api import get
import streamlit as st
import requests
import json
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


def get_regions():
    url = 'https://cloud.orionvm.com/api/v1/regions'
    headers = {'Authorization': f'Bearer {config.end_user_api_key}'}

    r = requests.get(url, headers=headers)
    regions = [ region["id"] for region in r.json() ]
    formatted_regions = [ region["name"] for region in r.json() ]

    return regions, formatted_regions


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


def main():
    st.header('CloudCo Server Builder')
    
    os_options = ['Linux', 'Windows']
    dc_options = get_regions()[0]
    tz_options = ['Eastern', 'Central', 'Mountain', 'Pacific']
    org_options = format_org_list()
    performance_tiers = ['Standard', 'High Memory', 'High CPU', '60735938-af5d-49b3-ae32-f585cf70196c']
    disk_tiers = ['Standard', 'SSD', 'Archival', '9c8b5610-b2fa-4196-9556-e3b0d0e05cd9']
    disk_capacity_options = range(10,2001, 10)
    template_options = ['Debian', '3CX', 'debian-10']

    # display the input fields
    organization = st.selectbox('Organization', org_options)
    instance_name = st.text_input('Instance Name')
    os = st.selectbox('Operating System', os_options)

    # TODO: This section needs reworking to get the regions list working with the format_func
    st.write(get_regions()[0])
    # st.write(get_regions()[1])
    formatted_regions = get_regions()[1]
    index = range(len(formatted_regions))
    region_dict = dict(zip(index, formatted_regions))

    st.write(formatted_regions)
    dc = st.selectbox('Data Center', dc_options, format_func=lambda x: region_dict.get(x))
    tz = st.selectbox('Timezone', tz_options)
    performance_tier = st.selectbox('Performance Tier', performance_tiers)
    if performance_tier == 'High Memory':
        memory_options = [1, 2, 4, 8, 16, 32, 64, 128]
        memory = st.select_slider('Memory (GB)', memory_options)
    else:
        memory_options = [1, 2, 4, 8, 16, 32, 64]
        memory = st.select_slider('Memory (GB)', memory_options)
    disk_tier = st.selectbox('Disk Tier', disk_tiers)
    disk_capacity = st.select_slider('Disk Capacity (GB)', disk_capacity_options)
    template = st.selectbox('Disk Template', template_options)

    if st.button('Submit'):
        st.write(f'Creating instance for {organization}')
        
        # match up org id to name
        for org in get_orgs():
            if organization == org['name']:
                org_id = org['id']
        
        # match up region id to name
        for region in get_regions()[0]:
            if dc == region['name']:
                region_id = region['id']
        
        ########################
        # check if we already have a token
        print(f'Checking for Application in org: {organization}')
        print(config.reseller_3cx)
        headers = {'Authorization': f'Bearer {config.admin_api_key}'}
        url = f'https://iaas.cloudcopartner.com/admin/api/v1/resellers/{config.reseller_3cx}/organizations/{org_id}/applications'
        app_request = requests.get(url, headers=headers)
        applications = app_request.json()
        token_present = False
        for a in applications:
            if f'{organization}_token' in a['name']:
                token_present = True
                token = a
        
        if not token_present:
            print('No token found, creating one now')
            token = create_application(org_id, organization, config.reseller_3cx)
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

        payload = {
        'name': instance_name,
        'instance_performance_tier': performance_tier,
        'disk_performance_tier': disk_tier,
        'memory': memory*1024,
        'region': region_id,
        'allocate_public_ip': True,
        'size': disk_capacity,
        'template': template,
        'start_when_ready': True
        }

        st.write(payload)

        create_instance(oauth_token, payload)

        ################################

    # return payload



if __name__ == '__main__':
    main()
    # st.write(get_resellers())
    # st.write(get_orgs())
