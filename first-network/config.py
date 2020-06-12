##############
# Author: Starly
# Goal: Customize the Hyperledger Fabric Configurations(local)
##############

import os
import sys

def crypto_config(Org,Peer):
    f = open('crypto-config.yaml','a')
    f.write("  - Name: Org%d\n    Domain: org%d.example.com\n    EnableNodeOUs: true\n    Template:\n      Count: %d\n    Users:\n      Count: 1\n\n"%(Org,Org,Peer))
    f.close()

def configtx(Org):
    f = open('configtx.yaml','a')
    for i in range(1,Org+1):
        f.write("                    - *Org%d\n"%i)
    f.write("    TwoOrgsChannel:\n        Consortium: SampleConsortium\n        Application:\n            <<: *ApplicationDefaults\n            Organizations:\n")
    for i in range(1,Org+1):
        f.write("                - *Org%d\n"%i)
    f.write("            Capabilities:\n                <<: *ApplicationCapabilities\n\n")

    f.write("Organizations:\n    - &OrdererOrg\n        Name: OrdererOrg\n        ID: OrdererMSP\n        MSPDir: crypto-config/ordererOrganizations/example.com/msp\n        Policies:\n            Readers:\n                Type: Signature\n                Rule: \"OR('OrdererMSP.member')\"\n            Writers:\n                Type: Signature\n                Rule: \"OR('OrdererMSP.member')\"\n            Admins:\n                Type: Signature\n                Rule: \"OR('OrdererMSP.admin')\"\n\n")
    for i in range(1,Org+1):
        f.write("    - &Org%d\n        Name: Org%dMSP\n        ID: Org%dMSP\n        MSPDir: crypto-config/peerOrganizations/org%d.example.com/msp\n        Policies:\n            Readers:\n                Type: Signature\n                Rule: \"OR('Org%dMSP.admin', 'Org%dMSP.peer', 'Org%dMSP.client')\"\n            Writers:\n                Type: Signature\n                Rule: \"OR('Org%dMSP.admin', 'Org%dMSP.client')\"\n            Admins:\n                Type: Signature\n                Rule: \"OR('Org%dMSP.admin')\"\n\n        AnchorPeers:\n            - Host: peer0.org%d.example.com\n              Port: 7051\n\n"%(i,i,i,i,i,i,i,i,i,i,i))
    f.close()

def docker_compose_cli(Org,Peer):
    f = open('docker-compose-cli.yaml','a')
    for i in range(1,Org+1):
        for j in range(Peer):
            f.write("      - peer%d.org%d.example.com\n"%(j,i))
    f.write("    networks:\n      - byfn\n\n")
    for i in range(1,Org+1):
        for j in range(Peer):
            f.write("  peer%d.org%d.example.com:\n    container_name: peer%d.org%d.example.com\n    extends:\n      file:  base/docker-compose-base.yaml\n      service: peer%d.org%d.example.com\n    networks:\n      - byfn\n\n"%(j,i,j,i,j,i))
    f.write("volumes:\n  orderer.example.com:\n")
    for i in range(1,Org+1):
        for j in range(Peer):
            f.write("  peer%d.org%d.example.com:\n"%(j,i))
    f.close()

def docker_compose_base(Org,Peer):
    f = open('base/docker-compose-base.yaml','a')
    count = 0
    for i in range(1,Org+1):
        for j in range(Peer):
            port = 7051 + (1000*count)
            if j == Peer-1:
                f.write("  peer%d.org%d.example.com:\n    container_name: peer%d.org%d.example.com\n    extends:\n      file: peer-base.yaml\n      service: peer-base\n    environment:\n      - CORE_PEER_ID=peer%d.org%d.example.com\n      - CORE_PEER_ADDRESS=peer%d.org%d.example.com:7051\n      - CORE_PEER_GOSSIP_BOOTSTRAP=peer%d.org%d.example.com:7051\n      - CORE_PEER_GOSSIP_EXTERNALENDPOINT=peer%d.org%d.example.com:7051\n      - CORE_PEER_LOCALMSPID=Org%dMSP\n    volumes:\n        - /var/run/:/host/var/run/\n        - ../crypto-config/peerOrganizations/org%d.example.com/peers/peer%d.org%d.example.com/msp:/etc/hyperledger/fabric/msp\n        - ../crypto-config/peerOrganizations/org%d.example.com/peers/peer%d.org%d.example.com/tls:/etc/hyperledger/fabric/tls\n        - peer%d.org%d.example.com:/var/hyperledger/production\n    ports:\n      - %d:7051\n      - %d:7053\n\n"%(j,i,j,i,j,i,j,i,0,i,j,i,i,i,j,i,i,j,i,j,i,port,port+2))
            else:
                f.write("  peer%d.org%d.example.com:\n    container_name: peer%d.org%d.example.com\n    extends:\n      file: peer-base.yaml\n      service: peer-base\n    environment:\n      - CORE_PEER_ID=peer%d.org%d.example.com\n      - CORE_PEER_ADDRESS=peer%d.org%d.example.com:7051\n      - CORE_PEER_GOSSIP_BOOTSTRAP=peer%d.org%d.example.com:7051\n      - CORE_PEER_GOSSIP_EXTERNALENDPOINT=peer%d.org%d.example.com:7051\n      - CORE_PEER_LOCALMSPID=Org%dMSP\n    volumes:\n        - /var/run/:/host/var/run/\n        - ../crypto-config/peerOrganizations/org%d.example.com/peers/peer%d.org%d.example.com/msp:/etc/hyperledger/fabric/msp\n        - ../crypto-config/peerOrganizations/org%d.example.com/peers/peer%d.org%d.example.com/tls:/etc/hyperledger/fabric/tls\n        - peer%d.org%d.example.com:/var/hyperledger/production\n    ports:\n      - %d:7051\n      - %d:7053\n\n"%(j,i,j,i,j,i,j,i,j+1,i,j,i,i,i,j,i,i,j,i,j,i,port,port+2))
            count+=1
    f.close()

def docker_compose_e2e_template(Org,Peer):
    f = open('docker-compose-e2e-template.yaml','a')
    for i in range(1,Org+1):
        for j in range(Peer):
            f.write("  peer%d.org%d.example.com:\n    container_name: peer%d.org%d.example.com\n    extends:\n      file:  base/docker-compose-base.yaml\n      service: peer%d.org%d.example.com\n    networks:\n      - byfn\n\n"%(j,i,j,i,j,i))
    count = 0
    for i in range(1,Org+1):
        port = 7054 + (1000*count)
        f.write("  ca%d:\n    image: hyperledger/fabric-ca:$IMAGE_TAG\n    environment:\n      - FABRIC_CA_HOME=/etc/hyperledger/fabric-ca-server\n      - FABRIC_CA_SERVER_CA_NAME=ca-org%d\n      - FABRIC_CA_SERVER_TLS_ENABLED=true\n      - FABRIC_CA_SERVER_TLS_CERTFILE=/etc/hyperledger/fabric-ca-server-config/ca.org%d.example.com-cert.pem\n      - FABRIC_CA_SERVER_TLS_KEYFILE=/etc/hyperledger/fabric-ca-server-config/CA%d_PRIVATE_KEY\n    ports:\n      - \"%d:7054\"\n    command: sh -c 'fabric-ca-server start --ca.certfile /etc/hyperledger/fabric-ca-server-config/ca.org%d.example.com-cert.pem --ca.keyfile /etc/hyperledger/fabric-ca-server-config/CA%d_PRIVATE_KEY -b admin:adminpw -d'\n    volumes:\n      - ./crypto-config/peerOrganizations/org%d.example.com/ca/:/etc/hyperledger/fabric-ca-server-config\n    container_name: ca_peerOrg%d\n    networks:\n      - byfn\n\n"%(i-1,i,i,i,port,i,i,i,i))
        count+=1
    f.write("volumes:\n  orderer.example.com:\n")
    for i in range(1,Org+1):
        for j in range(Peer):
            f.write("  peer%d.org%d.example.com:\n"%(j,i))
    f.close()

def docker_compose_couch(Org,Peer):
    f = open('docker-compose-couch.yaml','a')
    count = 0
    for i in range(1,Org+1):
        for j in range(Peer):
            port = 5984 + (1000*count)
            f.write("  couchdb%d:\n    container_name: couchdb%d\n    image: hyperledger/fabric-couchdb\n    environment:\n      - COUCHDB_USER=\n      - COUCHDB_PASSWORD=\n    ports:\n      - \"%d:5984\"\n    networks:\n      - byfn\n\n  peer%d.org%d.example.com:\n    environment:\n      - CORE_LEDGER_STATE_STATEDATABASE=CouchDB\n      - CORE_LEDGER_STATE_COUCHDBCONFIG_COUCHDBADDRESS=couchdb%d:5984\n      - CORE_LEDGER_STATE_COUCHDBCONFIG_USERNAME=\n      - CORE_LEDGER_STATE_COUCHDBCONFIG_PASSWORD=\n    depends_on:\n      - couchdb%d\n\n"%(count,count,port,j,i,count,count))
            count+=1
    f.close()

def byfn(Org):
    f = open('byfn.sh','a')
    for i in range(1,Org+1):
        f.write("  echo\n  echo \"#################################################################\"\n  echo \"#######    Generating anchor peer update for Org%dMSP   ##########\"\n  echo \"#################################################################\"\n  set -x\n  configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org%dMSPanchors.tx -channelID $CHANNEL_NAME -asOrg Org%dMSP\n  res=$?\n  set +x\n  if [ $res -ne 0 ]; then\n    echo \"Failed to generate anchor peer update for Org%dMSP...\"\n    exit 1\n  fi\n\n"%(i,i,i,i))
    f.write("  echo\n}\n")
    f.close()

def utils(Org):
    f = open('scripts/utils.sh','a')
    for i in range(1,Org+1):
        f.write("PEER0_ORG%d_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org%d.example.com/peers/peer0.org%d.example.com/tls/ca.crt\n"%(i,i,i))
    f.write("\nsetGlobals() {\n  PEER=$1\n  ORG=$2\n")
    for i in range(1,Org+1):
        if i == 1:
            f.write("  if [ $ORG -eq %d ]; then\n    CORE_PEER_LOCALMSPID=\"Org%dMSP\"\n    CORE_PEER_TLS_ROOTCERT_FILE=$PEER0_ORG%d_CA\n    CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org%d.example.com/users/Admin@org%d.example.com/msp\n    CORE_PEER_ADDRESS=peer$PEER.org%d.example.com:7051\n\n"%(i,i,i,i,i,i))
        else:
            f.write("  elif [ $ORG -eq %d ]; then\n    CORE_PEER_LOCALMSPID=\"Org%dMSP\"\n    CORE_PEER_TLS_ROOTCERT_FILE=$PEER0_ORG%d_CA\n    CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org%d.example.com/users/Admin@org%d.example.com/msp\n    CORE_PEER_ADDRESS=peer$PEER.org%d.example.com:7051\n\n"%(i,i,i,i,i,i))
    f.write("  else\n    echo \"================== ERROR !!! ORG Unknown ==================\"\n  fi\n  if [ \"$VERBOSE\" == \"true\" ]; then\n    env | grep CORE\n  fi\n}\n\n")
    f.write("instantiateChaincode() {\n  PEER=$1\n  ORG=$2\n  setGlobals $PEER $ORG\n  VERSION=${3:-1.0}\n\n  if [ -z \"$CORE_PEER_TLS_ENABLED\" -o \"$CORE_PEER_TLS_ENABLED\" = \"false\" ]; then\n    set -x\n    peer chaincode instantiate -o orderer.example.com:7050 -C $CHANNEL_NAME -n mycc -l ${LANGUAGE} -v ${VERSION} -c '{\"Args\":[\"init\",\"a\",\"100\",\"b\",\"200\"]}' -P \"AND ('Org1MSP.peer'")
    for i in range(2,Org+1):
        f.write(",'Org%dMSP.peer'"%i)
    f.write(")\" >&log.txt\n    res=$?\n    set +x\n  else\n    set -x\n    peer chaincode instantiate -o orderer.example.com:7050 --tls $CORE_PEER_TLS_ENABLED --cafile $ORDERER_CA -C $CHANNEL_NAME -n mycc -l ${LANGUAGE} -v 1.0 -c '{\"Args\":[\"init\",\"a\",\"100\",\"b\",\"200\"]}' -P \"AND ('Org1MSP.peer'")
    for i in range(2,Org+1):
        f.write(",'Org%dMSP.peer'"%i)
    f.write(")\" >&log.txt\n    res=$?\n    set +x\n  fi\n  cat log.txt\n")
    f.write("  verifyResult $res \"Chaincode instantiation on peer${PEER}.org${ORG} on channel '$CHANNEL_NAME' failed\"\n  echo \"===================== Chaincode is instantiated on peer${PEER}.org${ORG} on channel '$CHANNEL_NAME' ===================== \"\n  echo\n}\n")
    f.close()

def script(Org,Peer):
    f = open('scripts/script.sh','a')
    f.write("	for org in")
    for i in range(1,Org+1):
        f.write(" %d"%i)
    f.write("; do\n	    for peer in")
    for i in range(Peer):
        f.write(" %d"%i)
    f.write("; do\n		joinChannelWithRetry $peer $org\n		echo \"===================== peer${peer}.org${org} joined channel '$CHANNEL_NAME' ===================== \"\n		sleep $DELAY\n		echo\n	    done\n	done\n}\n\necho \"Creating channel...\"\ncreateChannel\n\necho \"Having all peers join the channel...\"\njoinChannel\n\n")
    for i in range(1,Org+1):
        f.write("echo \"Updating anchor peers for org%d...\"\nupdateAnchorPeers 0 %d\n"%(i,i))  
    for i in range(1,Org+1):
        f.write("echo \"Installing chaincode on peer0.org%d...\"\ninstallChaincode 0 %d\n"%(i,i))
    for i in range(2,Org+1):
        f.write("echo \"Instantiating chaincode on peer0.org%d...\"\ninstantiateChaincode 0 %d\n"%(i,i))
    f.write("\necho \"Querying chaincode on peer0.org1...\"\nchaincodeQuery 0 1 100\n\necho \"Sending invoke transaction on peer0.org1 peer0.org2...\"\nchaincodeInvoke")
    for i in range(1,Org+1):
        f.write(" 0 %d"%i)
    for i in range(2,Org+1):
        f.write("\necho \"Installing chaincode on peer1.org%d...\"\ninstallChaincode 1 %d"%(i,i))
    for i in range(2,Org+1):
        f.write("\necho \"Querying chaincode on peer1.org%d...\"\nchaincodeQuery 1 %d 90"%(i,i))
    f.write("\n\necho\necho \"========= All GOOD, BYFN execution completed =========== \"\necho \"END\"\necho\n\nexit 0\n")


if __name__ == '__main__':

    Org = 2
    Peer = 2

    # 1. crypto-config.yaml
    for i in range(1,Org+1):
        crypto_config(i,Peer)
    
    # 2. configtx.yaml
    configtx(Org)

    # 3. docker-compose-cli.yaml
    docker_compose_cli(Org,Peer)

    # 4. docker-compose-base.yaml
    docker_compose_base(Org,Peer)

    # 5. docker-compose-e2e-template.yaml
    docker_compose_e2e_template(Org,Peer)

    # 6. docker-compose-couch.yaml
    docker_compose_couch(Org,Peer)

    # 7. run sudo ./byfn.sh generate

    # 8. byfn.sh
    byfn(Org)

    # 9. utils.sh
    utils(Org)

    # 10. script.sh
    script(Org,Peer)
