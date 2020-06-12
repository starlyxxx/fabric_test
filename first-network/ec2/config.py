##############
# Author: Starly
# Goal: Customize the Hyperledger Fabric Configurations(ec2/kafka)
##############

import os
import sys

def docker_compose_zookeeperX(Zookeeper,Kafka,ip):
    for i in range(0,Zookeeper):
        f = open('../../kafkapeer/docker-compose-zookeeper%d.yaml'%i,'a')
        count = 0
        for ii in range(0,Zookeeper):
            f.write('      - "zookeeper%d:%s"\n'%(ii,ip[count]))
            count+=1
        count = 0
        for jj in range(0,Kafka):
            f.write('      - "kafka%d:%s"\n'%(jj,ip[count]))
            count+=1
        f.close()

def docker_compose_kafkaX(Zookeeper,Kafka,ip):
    for i in range(0,Kafka):
        f = open('../../kafkapeer/docker-compose-kafka%d.yaml'%i,'a')
        count = 0
        for ii in range(0,Zookeeper):
            f.write('      - "zookeeper%d:%s"\n'%(ii,ip[count]))
            count+=1
        count = 0
        for jj in range(0,Kafka):
            f.write('      - "kafka%d:%s"\n'%(jj,ip[count]))
            count+=1
        f.close()

def docker_compose_ordererX(Orderer,Kafka,ip):
    for i in range(0,Orderer):
        f = open('../../kafkapeer/docker-compose-orderer%d.yaml'%i,'a')
        count = 0
        for jj in range(0,Kafka):
            f.write('      - "kafka%d:%s"\n'%(jj,ip[count]))
            count+=1
        f.close()

def docker_compose_peer_orgX(Org,Peer,Orderer,ip):
    for i in range(1,Org+1):
        portcount = 0
        f = open('../../kafkapeer/docker-compose-peer-org%d.yaml'%i,'a')
        f.write('version: \'2\'\n\nnetworks:\n  fabric:\n\nservices:\n  cli:\n    container_name: cli\n    image: hyperledger/fabric-tools\n    tty: true\n    environment:\n      - GOPATH=/opt/gopath\n      - CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock\n      - CORE_LOGGING_LEVEL=DEBUG\n      - CORE_PEER_ID=cli\n      - CORE_PEER_ADDRESS=peer0.org%d.example.com:7051\n      - CORE_PEER_LOCALMSPID=Org%dMSP\n      - CORE_PEER_TLS_ENABLED=true\n      - CORE_PEER_TLS_CERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org%d.example.com/peers/peer0.org%d.example.com/tls/server.crt\n      - CORE_PEER_TLS_KEY_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org%d.example.com/peers/peer0.org%d.example.com/tls/server.key\n      - CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org%d.example.com/peers/peer0.org%d.example.com/tls/ca.crt\n      - CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org%d.example.com/users/Admin@org%d.example.com/msp\n      - CORE_CHAINCODE_KEEPALIVE=10\n    working_dir: /opt/gopath/src/github.com/hyperledger/fabric/peer\n    volumes:\n        - /var/run/:/host/var/run/\n        - ./chaincode/go/:/opt/gopath/src/github.com/hyperledger/fabric/kafkapeer/chaincode/go\n        - ./crypto-config:/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/\n        - ./channel-artifacts:/opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts\n    networks:\n        - fabric\n    extra_hosts:\n'%(i,i,i,i,i,i,i,i,i,i))
        count = 0
        for ii in range(0,Orderer):
            f.write('      - "orderer%d.example.com:%s"\n'%(ii,ip[count]))
            count+=1
        count = 4   # Should be equal to the Kafka number
        for jj in range(1,Org+1):
            for zz in range(0,Peer):
                f.write('      - "peer%d.org%d.example.com:%s"\n'%(zz,jj,ip[count]))
            count+=1
        for z in range(0,Peer):
            port = 7051 + 100*portcount
            f.write('\n  peer%d.org%d.example.com:\n    container_name: peer%d.org%d.example.com\n    hostname: peer%d.org%d.example.com\n    image: hyperledger/fabric-peer\n    environment:\n       - CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=${COMPOSE_PROJECT_NAME}_fabric\n       - CORE_PEER_ID=peer%d.org%d.example.com\n       - CORE_PEER_ADDRESS=peer%d.org%d.example.com:%d\n       - CORE_PEER_CHAINCODELISTENADDRESS=peer%d.org%d.example.com:%d\n       - CORE_PEER_GOSSIP_EXTERNALENDPOINT=peer%d.org%d.example.com:%d\n       - CORE_PEER_LOCALMSPID=Org%dMSP\n       - CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock\n       - CORE_LOGGING_LEVEL=DEBUG\n       - CORE_PEER_GOSSIP_USELEADERELECTION=true\n       - CORE_PEER_GOSSIP_ORGLEADER=false\n       - CORE_PEER_PROFILE_ENABLED=true\n       - CORE_PEER_TLS_ENABLED=true\n       - CORE_PEER_TLS_CERT_FILE=/etc/hyperledger/fabric/tls/server.crt\n       - CORE_PEER_TLS_KEY_FILE=/etc/hyperledger/fabric/tls/server.key\n       - CORE_PEER_TLS_ROOTCERT_FILE=/etc/hyperledger/fabric/tls/ca.crt\n    working_dir: /opt/gopath/src/github.com/hyperledger/fabric/peer\n    command: peer node start\n    volumes:\n       - /var/run/:/host/var/run/\n       - ./crypto-config/peerOrganizations/org%d.example.com/peers/peer%d.org%d.example.com/msp:/etc/hyperledger/fabric/msp\n       - ./crypto-config/peerOrganizations/org%d.example.com/peers/peer%d.org%d.example.com/tls:/etc/hyperledger/fabric/tls\n    networks:\n      fabric:\n        aliases:\n          - net\n    ports:\n      - %d:7051\n      - %d:7052\n      - %d:7053\n    extra_hosts:\n'%(z,i,z,i,z,i,z,i,z,i,port,z,i,port+1,z,i,port,i,i,z,i,i,z,i,port,port+1,port+2))
            portcount+=1
            count = 0
            for ii in range(0,Orderer):
                f.write('      - "orderer%d.example.com:%s"\n'%(ii,ip[count]))
                count+=1
        f.close()

def hosts(Org,Peer,Zookeeper,Kafka,Orderer,ip):
    f = open('../../kafkapeer/hosts','a')
    count = 0
    for i in range(0,Zookeeper):
        f.write('%s zookeeper%d\n'%(ip[count],i))
        count+=1
    count = 0
    for j in range(0,Kafka):
        f.write('%s kafka%d\n'%(ip[count],j))
        count+=1
    count = 0
    for ii in range(0,Orderer):
        f.write('%s orderer%d.example.com\n'%(ip[count],ii))
        count+=1
    count = 4
    for jj in range(1,Org+1):
        for zz in range(0,Peer):
            f.write('%s peer%d.org%d.example.com\n'%(ip[count],zz,jj))
        count+=1
    f.close()

#if __name__ == '__main__':
def config(Org,Peer):

    Zookeeper = 3
    Kafka = 4
    Orderer = 3

    ip = [l for l in open('./ips', 'r').read().split('\n') if l]

    # 1. docker_compose_orderer.yaml
    docker_compose_zookeeperX(Zookeeper,Kafka,ip)

    # 2. docker-compose-base.yaml
    docker_compose_kafkaX(Zookeeper,Kafka,ip)

    # 3. docker-compose-ordererX.yaml
    docker_compose_ordererX(Orderer,Kafka,ip)

    # 4. docker_compose_peer_orgX.yaml
    docker_compose_peer_orgX(Org,Peer,Orderer,ip)

    # 5. hosts
    hosts(Org,Peer,Zookeeper,Kafka,Orderer,ip)