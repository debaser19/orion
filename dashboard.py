import streamlit as st
import regions
import orgs
import create_instance
import specs
import templates


def main():
    st.set_page_config(layout='wide')
    st.header('CloudCo Server Builder')

    # Streamlit columns setup
    col1, col2 = st.beta_columns(2)

    # Reseller / Org Selection
    org_options = orgs.format_org_list()
    with col1:
        organization = st.selectbox('Organization', org_options)
        for org in orgs.get_orgs():     # match up org id to name
            if organization == org['name']:
                org_id = org['id']
        
        # Instance nama
        instance_name = st.text_input('Instance Name')

        # # OS Selection
        # os_options = ['Linux', 'Windows']
        # os = st.selectbox('Operating System', os_options)

        # Region Selection
        region_dict = regions.get_regions()
        region_options = list(region_dict.keys())
        region_id = st.selectbox('Data Center', region_options, format_func=lambda x: region_dict.get(x))

        # Template Selection
        templates_dict = templates.get_templates(region_id)
        templates_options = list(templates_dict.keys())
        template = st.selectbox('Disk Template', templates_options, format_func=lambda x: templates_dict.get(x))

    # # Timezone selection
    # tz_options = ['Eastern', 'Central', 'Mountain', 'Pacific']
    # tz = st.selectbox('Timezone', tz_options)

    # Instance Performance Tier
    instance_tiers_dict = specs.get_instance_tiers(region_id)
    instance_tiers_options = list(instance_tiers_dict.keys())
    with col2:
        performance_tier = st.selectbox('Performance Tier', instance_tiers_options, format_func=lambda x: instance_tiers_dict.get(x))
    
        if performance_tier == 'High Memory':
            memory_options = [1, 2, 4, 8, 16, 32, 64, 128]
            memory = st.select_slider('Memory (GB)', memory_options)
        else:
            memory_options = [1, 2, 4, 8, 16, 32, 64]
            memory = st.select_slider('Memory (GB)', memory_options)

        # Disk Performance Tier
        disk_tiers_dict = specs.get_disk_tiers(region_id)
        disk_tiers_options = list(disk_tiers_dict.keys())
        disk_tier = st.selectbox('Disk Tier', disk_tiers_options, format_func=lambda x: disk_tiers_dict.get(x))

        # Disk Capacity
        disk_capacity_options = range(10,2001, 10)
        disk_capacity = st.select_slider('Disk Capacity (GB)', disk_capacity_options)

    # Form Submission Button
    if st.button('Submit'):
        st.write(f'Creating instance for {organization}') 

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

        create_instance.create_instance(organization, payload)


if __name__ == '__main__':
    main()
