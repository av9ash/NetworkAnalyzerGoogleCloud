import googleapiclient.discovery
import time

#GCP Resources
PROJECT = 'meta-triode-238801'
BUCKET = 'cve-search-input-bucket'
ZONE = 'us-west2-a'
compute = googleapiclient.discovery.build('compute', 'v1')
def create_instance(compute, project, zone, name, bucket):
    # Get the latest Debian Jessie image.
    image_response = compute.images().getFromFamily(
        project=PROJECT, family='cve-search').execute()
    source_disk_image = image_response['selfLink']
    # Configure the machine
    machine_type = "zones/%s/machineTypes/n1-standard-2" % zone
    config = {
        'name': name,
        'machineType': machine_type,
        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],
        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],
        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }]
    }
    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()
def delete_instance(compute, project, zone, name):
    return compute.instances().delete(
        project=project,
        zone=zone,
        instance=name).execute()

def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    instances = result['items'] if 'items' in result else None
    for instance in instances:
        print(' - ' + instance['name'])
def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()
        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result
        time.sleep(1)
def start_instance(compute, project, zone, instance):
    return compute.instances().start(project=project, zone=zone, instance=instance).execute()
def stop_instance(compute, project, zone, instance):
    return compute.instances().stop(project=project, zone=zone, instance=instance).execute()
def main(project, bucket, zone):
    #List Instances
    print ('List of instances: ')
    list_instances(compute, project, zone)
    print ('-----------------------------')
    #Create Instance
    print ('Creating instance: ')
    operation = create_instance(compute, project, zone, 'instance-from-code', bucket)
    #wait_for_operation(compute, project, zone, operation['name'])
    print ('Instance created')
    #Delete Instance
    print ('\nBefore deletion: ')
    list_instances(compute, project, zone)
    operation = delete_instance(compute, project, zone, 'instance-from-code')
    #wait_for_operation(compute, project, zone, operation['name'])
    print ('After deletion: ')
    list_instances(compute, project, zone)
    #Start Instance
    operation = start_instance(compute, project, zone, 'instance-from-code')
    print ('Instance started.')
    #Stop Instance
    operation = stop_instance(compute, project, zone, 'instance-from-code')
    print ('Instance stopped.')

if __name__ == '__main__':
    main(PROJECT, BUCKET, ZONE)
