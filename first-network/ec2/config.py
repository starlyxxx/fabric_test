##############
# Author: Starly
# Goal: Customize the Hyperledger Fabric Configurations(ec2/solo)
##############

import os
import sys

def docker_compose_orderer(Org,Peer,ip):
    f = open('../../customize/depolyment/docker-compose-orderer.yml','a')
    count = 1
    for i in range(1,Org+1):
        for j in range(Peer):
            f.write('            - "peer%d.org%d.example.com:%s"\n'%(j,i,ip[count]))
        count+=1
    f.close()

def docker_compose_base(Peer):
    f = open('../../customize/depolyment/docker-compose-base.yml','a')
    count = 0
    for j in range(Peer):
        port = 7051 + (100*count)
        f.write("    peer%d:\n        image: hyperledger/fabric-peer\n        environment:\n            - CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock\n            - CORE_PEER_NETWORKID=net\n            - CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=${COMPOSE_PROJECT_NAME}_fabric\n            - CORE_PEER_ADDRESSAUTODETECT=true\n            - CORE_PEER_GOSSIP_ORGLEADER=false\n            - CORE_PEER_GOSSIP_USELEADERELECTION=true\n            - CORE_PEER_PROFILE_ENABLED=true\n            - CORE_PEER_MSPCONFIGPATH=/var/hyperledger/msp\n            - CORE_LOGGING_LEVEL=INFO\n            - CORE_LOGGING_GOSSIP=WARNING\n            - CORE_LOGGING_MSP=DEBUG\n            - CORE_PEER_TLS_ENABLED=false\n            - CORE_PEER_TLS_CLIENTAUTHREQUIRED=false\n            - CORE_PEER_TLS_CERT_FILE=/var/hyperledger/tls/server.crt\n            - CORE_PEER_TLS_KEY_FILE=/var/hyperledger/tls/server.key\n            - CORE_PEER_TLS_ROOTCERT_FILE=/var/hyperledger/tls/ca.crt\n        volumes:\n            - /var/run/:/host/var/run/\n            - $GOPATH/src/github.com/hyperledger/fabric/:/opt/gopath/src/github.com/hyperledger/fabric/\n            - ../crypto-config/:/var/hyperledger/configs\n            - ../channel-artifacts/:/var/hyperledger/configs\n        command: peer node start\n        ports:\n            - '%d'\n            - '%d'\n\n"%(count,port,port+2))
        count+=1
    f.close()

def docker_compose_org(Numoforg,Org,Peer,ip):
    f = open('../../customize/depolyment/docker-compose-org%d.yml'%Numoforg,'a')
    count = 0
    f.write("version: '2'\n\nnetworks:\n    fabric:\n\nservices:\n\n    cli:\n        container_name: cli\n        image: hyperledger/fabric-tools\n        tty: true\n        environment:\n          - GOPATH=/opt/gopath\n          - CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock\n          - CORE_LOGGING_LEVEL=INFO\n          - CORE_PEER_ID=cli\n          - CORE_PEER_ADDRESS=peer0.org%d.example.com:7051\n          - CORE_PEER_LOCALMSPID=Org%dMSP\n          - CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org%d.example.com/users/Admin@org%d.example.com/msp\n          - CORE_CHAINCODE_KEEPALIVE=10\n        extra_hosts:\n          - \"orderer.example.com:%s\"\n        working_dir: /opt/gopath/src/github.com/hyperledger/fabric/peer\n        command: /bin/bash\n        volumes:\n            - /var/run/:/host/var/run/\n            - ../../chaincode/:/opt/gopath/src/github.com/chaincode\n            - $GOPATH/src/github.com/hyperledger/fabric/:/opt/gopath/src/github.com/hyperledger/fabric/\n            - ../crypto-config:/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/\n            - ../channel-artifacts:/opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts/\n        depends_on:\n"%(Numoforg,Numoforg,Numoforg,Numoforg,ip[0]))
    for j in range(Peer):
        f.write("          - peer%d.org%d.example.com\n"%(j,Numoforg))
    f.write("        networks:\n            - fabric\n\n")
    for j in range(Peer):
        ipcount = 1
        port = 7051 + (100*count)
        if j == 0:
            if Numoforg == Org:
                f.write("    peer%d.org%d.example.com:\n        extends:\n            file: docker-compose-base.yml\n            service: peer%d\n        container_name: peer%d.org%d.example.com\n        environment:\n            - CORE_PEER_CHAINCODELISTENADDRESS=peer%d.org%d.example.com:7052\n            - CORE_PEER_ID=peer%d.org%d.example.com\n            - CORE_PEER_ADDRESS=peer%d.org%d.example.com:7051\n            - CORE_PEER_GOSSIP_BOOTSTRAP=peer%d.org%d.example.com:7051\n            - CORE_PEER_GOSSIP_EXTERNALENDPOINT=peer%d.org%d.example.com:7051\n            - CORE_PEER_GOSSIP_ORGLEADER=false\n            - CORE_PEER_GOSSIP_USELEADERELECTION=true\n            - CORE_PEER_LOCALMSPID=Org%dMSP\n            - CORE_PEER_TLS_CLIENTROOTCAS_FILES=/var/hyperledger/users/Admin@org%d.example.com/tls/ca.crt\n            - CORE_PEER_TLS_CLIENTCERT_FILE=/var/hyperledger/users/Admin@org%d.example.com/tls/client.crt\n            - CORE_PEER_TLS_CLIENTKEY_FILE=/var/hyperledger/users/Admin@org%d.example.com/tls/client.key\n        volumes:\n            - ../crypto-config/peerOrganizations/org%d.example.com/peers/peer%d.org%d.example.com/msp:/var/hyperledger/msp\n            - ../crypto-config/peerOrganizations/org%d.example.com/peers/peer%d.org%d.example.com/tls:/var/hyperledger/tls\n            - ../crypto-config/peerOrganizations/org%d.example.com/users:/var/hyperledger/users\n            - ../channel-artifacts/:/var/hyperledger/configs\n        extra_hosts:\n            - \"orderer.example.com:%s\"\n"%(j,Numoforg,j,j,Numoforg,j,Numoforg,j,Numoforg,j,Numoforg,0,0,j,Numoforg,Numoforg,Numoforg,Numoforg,Numoforg,Numoforg,j,Numoforg,Numoforg,j,Numoforg,Numoforg,ip[0]))
            else:
                f.write("    peer%d.org%d.example.com:\n        extends:\n            file: docker-compose-base.yml\n            service: peer%d\n        container_name: peer%d.org%d.example.com\n        environment:\n            - CORE_PEER_CHAINCODELISTENADDRESS=peer%d.org%d.example.com:7052\n            - CORE_PEER_ID=peer%d.org%d.example.com\n            - CORE_PEER_ADDRESS=peer%d.org%d.example.com:7051\n            - CORE_PEER_GOSSIP_BOOTSTRAP=peer%d.org%d.example.com:7051\n            - CORE_PEER_GOSSIP_EXTERNALENDPOINT=peer%d.org%d.example.com:7051\n            - CORE_PEER_GOSSIP_ORGLEADER=false\n            - CORE_PEER_GOSSIP_USELEADERELECTION=true\n            - CORE_PEER_LOCALMSPID=Org%dMSP\n            - CORE_PEER_TLS_CLIENTROOTCAS_FILES=/var/hyperledger/users/Admin@org%d.example.com/tls/ca.crt\n            - CORE_PEER_TLS_CLIENTCERT_FILE=/var/hyperledger/users/Admin@org%d.example.com/tls/client.crt\n            - CORE_PEER_TLS_CLIENTKEY_FILE=/var/hyperledger/users/Admin@org%d.example.com/tls/client.key\n        volumes:\n            - ../crypto-config/peerOrganizations/org%d.example.com/peers/peer%d.org%d.example.com/msp:/var/hyperledger/msp\n            - ../crypto-config/peerOrganizations/org%d.example.com/peers/peer%d.org%d.example.com/tls:/var/hyperledger/tls\n            - ../crypto-config/peerOrganizations/org%d.example.com/users:/var/hyperledger/users\n            - ../channel-artifacts/:/var/hyperledger/configs\n        extra_hosts:\n            - \"orderer.example.com:%s\"\n"%(j,Numoforg,j,j,Numoforg,j,Numoforg,j,Numoforg,j,Numoforg,0,Numoforg+1,j,Numoforg,Numoforg,Numoforg,Numoforg,Numoforg,Numoforg,j,Numoforg,Numoforg,j,Numoforg,Numoforg,ip[0]))
        else:
            f.write("    peer%d.org%d.example.com:\n        extends:\n            file: docker-compose-base.yml\n            service: peer%d\n        container_name: peer%d.org%d.example.com\n        environment:\n            - CORE_PEER_CHAINCODELISTENADDRESS=peer%d.org%d.example.com:7052\n            - CORE_PEER_ID=peer%d.org%d.example.com\n            - CORE_PEER_ADDRESS=peer%d.org%d.example.com:7051\n            - CORE_PEER_GOSSIP_BOOTSTRAP=peer%d.org%d.example.com:7051\n            - CORE_PEER_GOSSIP_EXTERNALENDPOINT=peer%d.org%d.example.com:7051\n            - CORE_PEER_GOSSIP_ORGLEADER=false\n            - CORE_PEER_GOSSIP_USELEADERELECTION=true\n            - CORE_PEER_LOCALMSPID=Org%dMSP\n            - CORE_PEER_TLS_CLIENTROOTCAS_FILES=/var/hyperledger/users/Admin@org%d.example.com/tls/ca.crt\n            - CORE_PEER_TLS_CLIENTCERT_FILE=/var/hyperledger/users/Admin@org%d.example.com/tls/client.crt\n            - CORE_PEER_TLS_CLIENTKEY_FILE=/var/hyperledger/users/Admin@org%d.example.com/tls/client.key\n        volumes:\n            - ../crypto-config/peerOrganizations/org%d.example.com/peers/peer%d.org%d.example.com/msp:/var/hyperledger/msp\n            - ../crypto-config/peerOrganizations/org%d.example.com/peers/peer%d.org%d.example.com/tls:/var/hyperledger/tls\n            - ../crypto-config/peerOrganizations/org%d.example.com/users:/var/hyperledger/users\n            - ../channel-artifacts/:/var/hyperledger/configs\n        extra_hosts:\n            - \"orderer.example.com:%s\"\n"%(j,Numoforg,j,j,Numoforg,j,Numoforg,j,Numoforg,j,Numoforg,j-1,Numoforg,j,Numoforg,Numoforg,Numoforg,Numoforg,Numoforg,Numoforg,j,Numoforg,Numoforg,j,Numoforg,Numoforg,ip[0]))
        for ii in range(1,Org+1):
            for jj in range(Peer):
                if jj == j and ii == Numoforg:
                    pass
                else:
                    f.write("            - \"peer%d.org%d.example.com:%s\"\n"%(jj,ii,ip[ipcount]))
            ipcount+=1
        f.write("        networks:\n          fabric:\n            aliases:\n              - net\n        ports:\n          - %d:7051\n          - %d:7053\n\n"%(port,port+2))
        count+=1
    f.close()


#if __name__ == '__main__':
def config(Org,Peer):

    # Org = 3
    # Peer = 20
    ip = [l for l in open('./ips', 'r').read().split('\n') if l]
    

    # 1. docker_compose_orderer.yml
    docker_compose_orderer(Org,Peer,ip)

    # 2. docker-compose-base.yml
    docker_compose_base(Peer)

    # 3. docker-compose-orgX.yml
    for Numoforg in range(1,Org+1):
        docker_compose_org(Numoforg,Org,Peer,ip)
