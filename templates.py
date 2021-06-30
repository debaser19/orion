import requests
import config


def get_templates(region):
    url = 'https://cloud.orionvm.com/api/v1/templates'
    headers = {'Authorization': f'Bearer {config.end_user_api_key}'}
    r = requests.get(url, headers=headers)

    # TODO: Sort template dict by values
    template_ids = [ t['id'] for t in r.json() if t['region']['id'] == region ]
    template_names = [ t['name'] for t in r.json() if t['region']['id'] == region ]
    templates_dict = dict(zip(template_ids, template_names))

    return templates_dict
