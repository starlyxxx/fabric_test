#!/bin/bash
# Author: Starly

PEER=10

while getopts "o:" arg
do
    case $arg in
    o)
        ORG=$OPTARG ;;
    ?)
        echo "Usage: -o (OrgId)" 
        exit 1 ;;
    esac
done

let count=($ORG-1)*$PEER
for ((j=0; j<$PEER; j++));do
    {
        let port=7051+$j*100
        export CORE_PEER_ADDRESS=peer$j.org${ORG}.example.com:$port 
        export ORDERER_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer0.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
        peer chaincode invoke --tls --cafile $ORDERER_CA -C mychannel -n mycc -c "{\"Args\":[\"set\",\"${count}\", \"200\"]}"
        ((count++))
    }
done

echo "done"
