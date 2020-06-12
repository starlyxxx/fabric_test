from __future__ import with_statement
from fabric import *
from invoke import task, Exit
from fabric import Connection
import time, sys, os#, scanf
from io import BytesIO
import math
from fabric import ThreadingGroup as Group

your_git_username = ""
your_git_password = ""

@task
def installDependencies(conn):
    conn.sudo('apt-get update')
    conn.sudo('apt-get -y install git')
    conn.sudo('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -')
    conn.sudo('add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"')
    conn.sudo('apt-get update')
    conn.sudo('apt-cache policy docker-ce')
    conn.sudo('apt-get install -y docker-ce')
    conn.sudo('curl -L https://github.com/docker/compose/releases/download/1.24.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose')
    conn.sudo('chmod +x /usr/local/bin/docker-compose')
    conn.sudo('curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -')
    conn.sudo('apt-get install -y nodejs')
    conn.sudo('npm install npm@5.6.0 -g')
    # install go-lang
    with conn.cd('/opt/'):
        conn.run('sudo mkdir golang')
    with conn.cd('/opt/golang/'):
        conn.run('sudo wget https://studygolang.com/dl/golang/go1.10.3.linux-amd64.tar.gz')
        conn.run('sudo tar -zxvf go1.10.3.linux-amd64.tar.gz')
        conn.run('sudo rm go1.10.3.linux-amd64.tar.gz')
    # set go environment
    conn.sudo('rm /etc/profile')
    conn.put('profile')
    conn.sudo('mv profile /etc')
    conn.run('source /etc/profile')

    # download the fabric
    conn.sudo('mkdir -p /opt/gopath/src/github.com/hyperledger/')
    with conn.cd('/opt/gopath/src/github.com/hyperledger/'):
        conn.run('sudo git clone https://github.com/hyperledger/fabric.git')
    with conn.cd('/opt/gopath/src/github.com/hyperledger/fabric/'):
        conn.run('sudo git checkout v1.4.0')
    # downliad the images
    conn.sudo('docker pull hyperledger/fabric-peer:amd64-1.2.0')
    conn.sudo('docker pull hyperledger/fabric-orderer:amd64-1.2.0')
    conn.sudo('docker pull hyperledger/fabric-tools:amd64-1.2.0')
    conn.sudo('docker pull hyperledger/fabric-ccenv:amd64-1.2.0')
    conn.sudo('docker pull hyperledger/fabric-baseos:amd64-0.4.10')
    conn.sudo('docker pull hyperledger/fabric-kafka:latest')
    conn.sudo('docker pull hyperledger/fabric-zookeeper:latest')
    conn.sudo('docker pull hyperledger/fabric-couchdb:latest')
    conn.sudo('docker pull hyperledger/fabric-ca:latest')
    # prepara the kafka configs
    '''with conn.cd('/opt/gopath/src/github.com/hyperledger/fabric/'):
        conn.run('sudo rm -rf kafkapeer')'''
    conn.put('../../kafkapeer.tar')
    conn.sudo('mv kafkapeer.tar /opt/gopath/src/github.com/hyperledger/fabric')
    with conn.cd('/opt/gopath/src/github.com/hyperledger/fabric/'):
        conn.run('sudo tar -xvf kafkapeer.tar')
        conn.run('sudo rm kafkapeer.tar')
    with conn.cd('/etc/'):
        conn.run('sudo rm -rf hosts')
    with conn.cd('/opt/gopath/src/github.com/hyperledger/fabric/kafkapeer/'):
        conn.run('sudo chmod -R 777 ./bin')
        conn.run('sudo mv hosts /etc')

@task
def removeHosts(conn):
    conn.run('rm ~/hosts')

@task
def writeHosts(conn):
    conn.put('./hosts')#, '~/')

@task
def bringUpZookeeper(conn,zid):
    with conn.cd('/opt/gopath/src/github.com/hyperledger/fabric/kafkapeer'):
        conn.run('sudo docker-compose -f docker-compose-zookeeper%s.yaml up -d'%str(zid))

@task
def bringUpKafka(conn,kid):
    with conn.cd('/opt/gopath/src/github.com/hyperledger/fabric/kafkapeer'):
        conn.run('sudo docker-compose -f docker-compose-kafka%s.yaml up -d'%str(kid))

@task
def bringUpOrderer(conn,oid):
    with conn.cd('/opt/gopath/src/github.com/hyperledger/fabric/kafkapeer'):
        conn.run('sudo docker-compose -f docker-compose-orderer%s.yaml up -d'%str(oid))

@task
def bringUpOrgs(conn,orgID):
    with conn.cd('/opt/gopath/src/github.com/hyperledger/fabric/kafkapeer'):
        conn.run('sudo docker-compose -f docker-compose-peer-org%s.yaml up -d'%str(orgID))

@task
def getfile(conn):
    fname = "mychannel.block"
    conn.get('/opt/gopath/src/github.com/hyperledger/fabric/kafkapeer/'+fname,'mychannel.block')
    with conn.cd('/opt/gopath/src/github.com/hyperledger/fabric/kafkapeer'):
        conn.run('sudo rm -rf %s'%fname)

@task
def putfile(conn):
    conn.put('./mychannel.block')
    conn.run('mv mychannel.block /opt/gopath/src/github.com/hyperledger/fabric/kafkapeer')

@task
def getlog(conn,orgID,Peer):
    with conn.cd('/opt/gopath/src/github.com/hyperledger/fabric/kafkapeer'):
        for j in range(int(Peer)):
            conn.run("sudo docker logs peer%d.org%d.example.com 2>&1 | grep -i -a -E 'private|pvt|privdata'>log/peer%d.org%d_log.txt"%(j,int(orgID),j,int(orgID)))

@task
def storelog(conn,orgID):
    fname = "Org%s_log"%orgID
    with conn.cd('/opt/gopath/src/github.com/hyperledger/fabric/kafkapeer'):
        conn.run('mv log %s'%fname)
        conn.run('tar -zcvf %s.tar -C %s .'%(fname,fname))
    fnametar = "Org%s_log.tar"%orgID
    conn.get('/opt/gopath/src/github.com/hyperledger/fabric/kafkapeer/'+fnametar,'log/'+fnametar)
    with conn.cd('/opt/gopath/src/github.com/hyperledger/fabric/kafkapeer'):
        conn.run('sudo rm -rf %s'%fnametar)

@task
def cloneRepo(conn):
    conn.run('git clone https://%s:%s@bitbucket.org/sduan-umbc/chios.git'%(your_git_username,your_git_password))

@task
def git_pull(conn):
    conn.sudo('apt-get -y install git')
    result = conn.run('test -d chios', warn=True)
    if not result:
        conn.run('git clone https://%s:%s@bitbucket.org/sduan-umbc/chios.git'%(your_git_username,your_git_password))
    with conn.cd('~/chios/'):
        conn.run('git reset --hard origin/master')
        conn.run('git clean -fxd')
        conn.run('git pull')

