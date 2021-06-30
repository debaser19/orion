import requests
import config


def get_regions():
    url = 'https://cloud.orionvm.com/api/v1/regions'
    headers = {'Authorization': f'Bearer {config.end_user_api_key}'}
    r = requests.get(url, headers=headers)

    # TODO: Sort regions dict by values
    regions = [ region["id"] for region in r.json() ]
    formatted_regions = [ region["name"] for region in r.json() ]
    region_dict = dict(zip(regions, formatted_regions))

    return region_dict