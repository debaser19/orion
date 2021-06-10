import pandas as pd


def main():
    # read in the csv and sort it
    df = pd.read_csv('instances.csv').sort_values(by=['org_name']).dropna(subset=['wan_ip']).to_dict('records')
    for i in df:
        # remove the windows instances
        try:
            if 'windows' in i['template'].lower():
                # print(f'Removing record: {i}')
                df.remove(i)
            elif i['state'] == 'stopped':
                df.remove(i)
        except Exception as e:
            print(f'Null values, skipping: {e}')
            print(f'Removing {i["wan_ip"]}')
            df.remove(i)
    
    # build list of orgs and convert to set to grab uniques
    orgs = set([ org['org_name'] for org in df ])

    # convert back to list to format the org names for ansible inventory
    orgs = list(orgs)
    orgs.sort()

    # format the org names and add to new list
    formatted_orgs = [ org.replace(' ', '-').lower() for org in orgs ]

    # match up IPs to org name
    for o in formatted_orgs:
        print(f'[{o}]')
        for i in df:
            if i['org_name'].replace(' ', '-').lower() == o:
                print(i['wan_ip'])


if __name__ == '__main__':
    main()