##############################
# Sisi Duan. Assistant Professor. University of Maryland, Baltimore County
##############################

import argparse
import boto.ec2
import sys, os
import time
from subprocess import check_output, Popen, call, PIPE, STDOUT
import fcntl
from threading import Thread
import platform
import configparser
from config import config

your_key_path = "~/.ssh/id_rsa"
your_key_name = "id_rsa"
Org = 5
Peer = 10
Zookeeper = 3
Kafka = 4
Orderer = 3

if not boto.config.has_section('ec2'):
    boto.config.add_section('ec2')
    boto.config.setbool('ec2','use-sigv4',True)

secgroups = {
    'us-east-1':'sg-03446fa3b6326fb94',
    'us-west-1':'sg-0ab6e7479c9f1e797', #California
    'ap-southeast-1':'sg-0f450012faf296568', #Singapore
    'ap-southeast-2':'sg-0ee3f983220af3adf', #Sydney
    'ap-northeast-1':'sg-04e0baba8d2065969', #Tokyo
    'eu-west-1':'sg-05e830348f1cd3310', #Ireland
    'ca-central-1':'sg-03da76a97310ce076', #Canada
}
regions = sorted(secgroups.keys())[::-1]

NameFilter = 'Fabric-Xin'
    
def getAddrFromEC2Summary(s):
    return [
            x.split('ec2.')[-1] for x in s.replace(
                '.compute.amazonaws.com', ''
                ).replace(
                    '.us-west-1', ''    # Later we need to add more such lines
                    ).replace(
                        '-', '.'
                        ).strip().split('\n')]

def get_ec2_instances_private_ip(region):
    ec2_conn = boto.ec2.connect_to_region(region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key)
    if ec2_conn:
        result = []
        reservations = ec2_conn.get_all_reservations(filters={'tag:Name': NameFilter})
        for reservation in reservations:
            if reservation:       
                for ins in reservation.instances:
                    if ins.public_dns_name: 
                        currentIP = ins.private_ip_address
                        print (currentIP)
                        result.append(currentIP)
                        
        return result
    else:
        print ('Region failed'), region
        return None

def get_ec2_instances_ip(region):
    ec2_conn = boto.ec2.connect_to_region(region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key)
    if ec2_conn:
        result = []
        reservations = ec2_conn.get_all_reservations(filters={'tag:Name': NameFilter})
        for reservation in reservations:
            if reservation:       
                for ins in reservation.instances:
                    if ins.public_dns_name: 
                        currentIP = ins.public_dns_name.split('.')[0][4:].replace('-','.')
                        result.append(currentIP)
                        print (currentIP)
        return result
    else:
        print ('Region failed'), region
        return None

def get_ec2_instances_id(region):
    ec2_conn = boto.ec2.connect_to_region(region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key)
    if ec2_conn:
        result = []
        reservations = ec2_conn.get_all_reservations(filters={'tag:Name': NameFilter})
        for reservation in reservations:    
            for ins in reservation.instances:
                print (ins.id)
                result.append(ins.id)
        return result
    else:
        print ('Region failed'), region
        return None

def stop_all_instances(region):
    ec2_conn = boto.ec2.connect_to_region(region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key)
    idList = []
    if ec2_conn:
        reservations = ec2_conn.get_all_reservations(filters={'tag:Name': NameFilter})
        for reservation in reservations: 
            if reservation:   
                for ins in reservation.instances:
                    idList.append(ins.id)
        ec2_conn.stop_instances(instance_ids=idList)

def terminate_all_instances(region):
    ec2_conn = boto.ec2.connect_to_region(region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key)
    idList = []
    if ec2_conn:
        reservations = ec2_conn.get_all_reservations(filters={'tag:Name': NameFilter})
        for reservation in reservations:   
            if reservation:    
                for ins in reservation.instances:
                    idList.append(ins.id)
        ec2_conn.terminate_instances(instance_ids=idList)

def launch_new_instances(region, number):
    ec2_conn = boto.ec2.connect_to_region(region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key)
    dev_sda1 = boto.ec2.blockdevicemapping.EBSBlockDeviceType(delete_on_termination=True)
    dev_sda1.size = 8 # size in Gigabytes
    dev_sda1.delete_on_termination = True
    bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
    bdm['/dev/sda1'] = dev_sda1
    #img = ec2_conn.get_all_images(filters={'name':'ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server-20180308'})[0].id
    img = ec2_conn.get_all_images(filters={'name':'ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-20190406'})[0].id
    reservation = ec2_conn.run_instances(image_id=img, #'ami-df6a8b9b',  # ami-9f91a5f5
                                 min_count=number,
                                 max_count=number,
                                 key_name=your_key_name, 
                                 instance_type='c5.4xlarge',
                                 security_group_ids = [secgroups[region], ],
                                 #subnet_id = 'subnet-0b13b68ac4ca77289',  #Singapore
                                 subnet_id = 'subnet-01822b14336afe8a7', #Ca
                                 #subnet_id = 'subnet-0d4fed75daf706346',  #Vir
                                 #subnet_id = 'subnet-07252785586d5600e', #Ir
                                 block_device_map = bdm)
    for instance in reservation.instances:
        instance.add_tag("Name", NameFilter)
    return reservation


def start_all_instances(region):
    ec2_conn = boto.ec2.connect_to_region(region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key)
    idList = []
    if ec2_conn:
        reservations = ec2_conn.get_all_reservations(filters={'tag:Name': NameFilter})
        for reservation in reservations:    
            for ins in reservation.instances:
                idList.append(ins.id)
        ec2_conn.start_instances(instance_ids=idList)

def ipAll():
    result = []
    for region in regions:
        result += get_ec2_instances_ip(region) or []
    open('hosts','w').write('\n'.join(result))
    #callFabFromIPList(result, 'removeHosts')
    #callFabFromIPList(result, 'writeHosts')
    return result

def privateIPAll():
    result = []
    for region in regions:
        result += get_ec2_instances_private_ip(region) or []
    open('ips','w').write('\n'.join(result))
    return result


def getIP():
    return [l for l in open('hosts', 'r').read().split('\n') if l]

def join_get(l,sep):
    if isinstance(l,list):
        output = []
        for i in l:
            output.append('ubuntu@'+i)
        return sep.join(output)
    if isinstance(l,str):
        return 'ubuntu@'+l

def callFabFromIPList(l, work):
    print ('fab -i %s -H %s %s' % (your_key_path,join_get(l,','), work))
    call('fab -i %s -H %s %s' % (your_key_path,join_get(l,','), work), shell=True)


c = callFabFromIPList

def id():
    c(getIP(), 'installDependencies')

def join_getlist(l):
    output = []
    if isinstance(l,list):
        for i in l:
            output.append('ubuntu@'+i)
    if isinstance(l,str):
        output.append('ubuntu@'+l)
    return output

def gen_install_bash(ips,fname):
    f = open(fname,"w")
    f.write("#!/bin/bash\n\n")
    for i in range(len(ips)):
        f.write('fab -i %s -H %s installDependencies&\n'%(your_key_path,ips[i]))
    f.write('\nrm -rf channelall.block\n')
    f.close()

def idParallel():
    bashfilename = "runInstall.sh"
    gen_install_bash(join_getlist(getIP()),bashfilename)
    if platform.system() == 'Darwin':
        popen = Popen(['bash',bashfilename])
        #os.system('bash '+bashfilename)
    else:
        try:
            popen = Popen('./%s'%bashfilename)
            #os.system('./'+bashfilename)
        except:
            popen = Popen(['bash',bashfilename])

def kafkapeer():
    config(Org,Peer)

def gf():
    orgIP = []
    orgIP = getIP()
    call('fab -i %s -H ubuntu@%s getfile' %(your_key_path,orgIP[Kafka]), shell=True) 
    c(getIP(), 'putfile')

def bringUpOrgs():
    orgIP = []
    orgIP = getIP()
    for i in range(0,Zookeeper):
        call('fab -i %s -H ubuntu@%s bringUpZookeeper %d' %(your_key_path,orgIP[i],i), shell=True)
    for i in range(0,Kafka):
        call('fab -i %s -H ubuntu@%s bringUpKafka %d' %(your_key_path,orgIP[i],i), shell=True)
    for i in range(0,Orderer):
        call('fab -i %s -H ubuntu@%s bringUpOrderer %d' %(your_key_path,orgIP[i],i), shell=True)
    count = Kafka
    for i in range(1,Org+1):
        call('fab -i %s -H ubuntu@%s bringUpOrgs %d' %(your_key_path,orgIP[count],i), shell=True)
        count+=1

def getlog():
    orgIP = []
    orgIP = getIP()
    count = Kafka
    for i in range(1,Org+1):
        call('fab -i %s -H ubuntu@%s getlog %d %d' %(your_key_path,orgIP[count],i,Peer), shell=True) 
        count+=1
    count = Kafka
    for i in range(1,Org+1):
        call('fab -i %s -H ubuntu@%s storelog %d' %(your_key_path,orgIP[count],i), shell=True) 
        count+=1

if  __name__ =='__main__':
  try: __IPYTHON__
  except NameError:
    parser = argparse.ArgumentParser()
    parser.add_argument('access_key', help='Access Key')
    parser.add_argument('secret_key', help='Secret Key')
    args = parser.parse_args()
    access_key = args.access_key
    secret_key = args.secret_key

    import IPython
    IPython.embed()

