from __future__ import with_statement
from fabric import *
from invoke import task, Exit
from fabric import Connection
import time, sys, os
from io import BytesIO
import math
from fabric import ThreadingGroup as Group

your_git_username = "XinStarly"
your_git_password = ""
filename = 'customize'

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
    conn.sudo('wget https://dl.google.com/go/go1.10.linux-amd64.tar.gz')
    conn.sudo('tar -xvf go1.10.linux-amd64.tar.gz')
    conn.sudo('rm go1.10.linux-amd64.tar.gz')
    conn.sudo('mv go /usr/local')
    # set go environment
    conn.sudo('sudo rm ~/.bashrc')
    conn.put('.bashrc')
    # download the fabric-samples
    conn.sudo('rm -rf fabric-samples')
    conn.run('git clone -b release-1.3 --single-branch https://github.com/hyperledger/fabric-samples.git')
    conn.sudo('rm -rf customize')
    conn.put('../../customize.tar')
    conn.run('mv customize.tar ~/fabric-samples')
    with conn.cd('~/fabric-samples'):
        conn.run('sudo bash ./scripts/bootstrap.sh 1.4.0 1.4.0 0.4.14')
        conn.run('tar -xvf customize.tar')
        conn.run('rm customize.tar')

@task
def removeHosts(conn):
    conn.run('rm ~/hosts')

@task
def writeHosts(conn):
    conn.put('./hosts')#, '~/')

@task
def bringUpOrgsOrderer(conn):
    with conn.cd('~/fabric-samples/customize/depolyment'):
        conn.run('sudo docker-compose -f docker-compose-orderer.yml up -d')

@task
def bringUpOrgs(conn,orgID):
    with conn.cd('~/fabric-samples/customize/depolyment'):
        conn.run('sudo docker-compose -f docker-compose-org%s.yml up -d'%str(orgID))

@task
def getfile(conn):
    fname = "channelall.block"
    conn.get('fabric-samples/customize/depolyment/'+fname,'channelall.block')
    with conn.cd('~/fabric-samples/customize/depolyment'):
        conn.run('sudo rm -rf %s'%fname)

@task
def putfile(conn):
    conn.put('./channelall.block')
    conn.run('mv channelall.block ~/fabric-samples/customize/depolyment')

@task
def getlog(conn,orgID,Peer):
    with conn.cd('~/fabric-samples/customize/depolyment'):
        for j in range(int(Peer)):
            conn.run("sudo docker logs peer%d.org%d.example.com 2>&1 | grep -i -a -E 'private|pvt|privdata'>log/peer%d.org%d_log.txt"%(j,int(orgID),j,int(orgID)))

@task
def storelog(conn,orgID):
    fname = "Org%s_log"%orgID
    with conn.cd('~/fabric-samples/customize/depolyment'):
        conn.run('mv log %s'%fname)
        conn.run('tar -zcvf %s.tar -C %s .'%(fname,fname))
    fnametar = "Org%s_log.tar"%orgID
    conn.get('fabric-samples/customize/depolyment/'+fnametar,'log/'+fnametar)
    with conn.cd('~/fabric-samples/customize/depolyment'):
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

