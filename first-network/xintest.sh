#!/bin/bash
# Author: Starly
# 500 transactions per block, 1000 peers send requests at the same time, with kafka order and golevelDB

# install the Marbles chaincode
ORG=2
PEER=2
transaction=50

for ((i=1; i<=$ORG; i++));do
    {
        export CORE_PEER_LOCALMSPID=Org${i}MSP
        export CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org${i}.example.com/peers/peer0.org${i}.example.com/tls/ca.crt
        export CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org${i}.example.com/users/Admin@org${i}.example.com/msp

        for ((j=0; j<$PEER; j++));do
            {
                export CORE_PEER_ADDRESS=peer$j.org$i.example.com:7051
                peer chaincode install -n marblesp -v 1.0 -p github.com/chaincode/marbles02_private/go/
            }
        done
    }
done

# instantiate the Marbles chaincode
export ORDERER_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
peer chaincode instantiate -o orderer.example.com:7050 --tls --cafile $ORDERER_CA -C mychannel -n marblesp -v 1.0 -c '{"Args":["init"]}' -P "OR('Org1MSP.member','Org2MSP.member')" --collections-config  $GOPATH/src/github.com/chaincode/marbles02_private/collections_config.json 
wait

echo "==============start to instantiate databases in peers================="
sleep 5

########################
# instantiate the peers
########################
count=0

for ((i=1; i<=$ORG; i++));do
    {
        export CORE_PEER_LOCALMSPID=Org${i}MSP
        export CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org${i}.example.com/peers/peer0.org${i}.example.com/tls/ca.crt
        export CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org${i}.example.com/users/Admin@org${i}.example.com/msp

        for ((j=0; j<$PEER; j++));do
            {
                export CORE_PEER_ADDRESS=peer$j.org$i.example.com:7051
                peer chaincode invoke -o orderer.example.com:7050 --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n marblesp -c "{\"Args\":[\"initMarble\",\"marble${count}\",\"blue\",\"35\",\"tom\",\"99\"]}" 
                ((count++))
            }
        done
    }
done

echo "==============start to send the transactions================="
sleep 5

########################
# send the transactions
########################
let count=$ORG*$PEER
for ((i=1; i<=$ORG; i++));do
    {
        export CORE_PEER_LOCALMSPID=Org${i}MSP
        export CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org${i}.example.com/peers/peer0.org${i}.example.com/tls/ca.crt
        export CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org${i}.example.com/users/Admin@org${i}.example.com/msp

        for ((j=0; j<$PEER; j++));do
            {
                export CORE_PEER_ADDRESS=peer$j.org$i.example.com:7051
                for ((ops=0; ops<$transaction; ops++));do
                    {
                        peer chaincode invoke -o orderer.example.com:7050 --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n marblesp -c "{\"Args\":[\"initMarble\",\"marble${count}\",\"blue\",\"35\",\"tom\",\"99\"]}" &
                        ((count++))
                    } 
                done
            }
        done
    }
done
wait

echo "==============everything is good!================="