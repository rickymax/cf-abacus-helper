'''
    serviceMgt.py

    Abacus Helper

    @Author: rickylo@iii.org.tw
'''
import json
import requests
import os

from utils import runcmd


if 'VCAP_APPLICATION' in os.environ:
    cf_api_endpoint = os.getenv('CF_API_ENDPOINT')
    cf_user = os.getenv('CF_USER')
    cf_password = os.getenv('CF_PASSWORD')


def cf_login():
    '''
    '''
    try:
        cmd = ('/home/vcap/app/cf login -a {0} --skip-ssl-validation'
               ' -u {1} -p {2} -o system -s system').format(cf_api_endpoint, cf_user, cf_password)
        rc, data, err = runcmd(cmd)
    except:
        print("[ERROR] {}").format(err)
    finally:
        return rc

def cf_token():
    '''
    '''
    try:
        cf_login()
        cmd = ('/home/vcap/app/cf oauth-token')
        rc, data, err = runcmd(cmd)
    except:
        print("[ERROR] {}").format(err)
    finally:
        return "".join(data.split('\n'))

def abacus_helper():
    '''
    '''
    helper = {}
    orgs = []

    cf_login()

    # list all oragnizations
    res = requests.get("".join((cf_api_endpoint, '/v2/organizations')),
                       headers={'Authorization': cf_token()},
                       verify=False)

    for org in res.json()['resources']:
        orgs.append(org['metadata']['guid'])

    # list all service instances
    for org in orgs:
        res = requests.get("".join((cf_api_endpoint, '/v2/service_instances?q=organization_guid:{}'.format(org))),
                           headers={'Authorization': cf_token()},
                           verify=False)
        for service in res.json()['resources']:
            resource_instance_id = service['metadata']['guid']
            helper[resource_instance_id] = {
                'organization_id': org,
                'space_id': service['entity']['space_guid'],
                'resource_id': service['entity']['tags']
            }

    # store relations
    with open('/home/vcap/app/app/relations.py', 'w') as f:
        print >> f, 'helper = {}'.format(helper)

    return helper

def asking_helper(service_instance_id):
    '''
    '''
    import relations

    cache = relations.helper

    # find in cache
    if service_instance_id in cache:
        return cache[service_instance_id]
    else:
        cache = abacus_helper()

    # second chance
    if service_instance_id in cache:
        return cache[service_instance_id]
    else:
        return None

