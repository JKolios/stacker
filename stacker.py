import sys
import os
import boto3
import sh
import json

conf = None


def is_needed_component(instance_hostname, component_list):
    return any([name for name in component_list if name in instance_hostname])


def load_conf(path):
    global conf
    with open(path) as conf_file:
        conf = json.load(conf_file)


def main(argv):
    local_folder = os.path.abspath(os.path.dirname(__file__))
    load_conf(local_folder + '/conf.json')

    if len(argv) < 2:
        print 'Stack name not provided. Valid stack names:{}'.format(conf['stacks'].keys())
        stack, components = None, None
        quit()
    elif len(argv) == 2:
        stack = argv[1]
        components = conf['components']
        print 'Accessing stack:{stack}'.format(stack=stack)
    else:
        stack = argv[1]
        components = [argv[2]]
        print 'Accessing component:{component} of stack:{stack}'.format(component=components[0],
                                                                        stack=stack)

    opsworks_client = boto3.client('opsworks')
    instance_desc = opsworks_client.describe_instances(StackId=conf['stacks'][stack])['Instances']
    needed_instances = [inst for inst in instance_desc
                        if inst['Status'] == 'online'
                        and is_needed_component(inst['Hostname'], components)]

    addresses = [instance['PrivateIp'] for instance in needed_instances]

    commands = ['ssh {username}@{address}'.format(username=conf['ssh_username'], address=add) for add in addresses]

    for command in commands:
        sh.bash('{folder}/tab.sh'.format(folder=local_folder), command)


if __name__ == '__main__':
    main(sys.argv)
