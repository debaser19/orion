import requests
import config


def get_regions():
    url = 'https://cloud.orionvm.com/api/v1/regions'
    headers = {'Authorization': f'Bearer {config.end_user_api_key}'}

    r = requests.get(url, headers=headers)
    regions = [ region["id"] for region in r.json() ]
    formatted_regions = [ region["name"] for region in r.json() ]

    return regions, formatted_regions