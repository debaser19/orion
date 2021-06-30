import requests
import config


def get_instance_tiers(region):
    url = 'https://cloud.orionvm.com/api/v1/performance_tiers/instances'
    headers = {'Authorization': f'Bearer {config.end_user_api_key}'}
    r = requests.get(url, headers=headers)

    # TODO: Sort instance tier dict by values
    tier_ids = [ t['id'] for t in r.json() if t['region']['id'] == region ]
    tier_names = [ t['name'] for t in r.json() if t['region']['id'] == region ]
    instance_tiers_dict = dict(zip(tier_ids, tier_names))

    return instance_tiers_dict


def get_disk_tiers(region):
    url = 'https://cloud.orionvm.com/api/v1/performance_tiers/disks'
    headers = {'Authorization': f'Bearer {config.end_user_api_key}'}
    r = requests.get(url, headers=headers)

    # TODO: Sort disk tier dict by values
    tier_ids = [ t['id'] for t in r.json() if t['region']['id'] == region ]
    tier_names = [ t['name'] for t in r.json() if t['region']['id'] == region ]
    disk_tiers_dict = dict(zip(tier_ids, tier_names))

    return disk_tiers_dict
