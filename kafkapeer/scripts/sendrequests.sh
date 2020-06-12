#!/bin/bash
# Author: Starly

PEER=10
transaction=50

while getopts "o:s:" arg
do
    case $arg in
    o)
        ORG=$OPTARG ;;
    s)
        OrgNum=$OPTARG ;;
    ?)
        echo "Usage: -o (OrgId);    -s (Sum of Orgs)" 
        exit 1 ;;
    esac
done

let count=($ORG-1)*$PEER*$transaction+$OrgNum*$PEER
for ((j=0; j<$PEER; j++));do
    {
        let port=7051+$j*100
        export CORE_PEER_ADDRESS=peer$j.org$ORG.example.com:$port 
        for ((ops=0; ops<$transaction; ops++));do
            {
                ORDERER_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer0.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
                peer chaincode invoke --tls --cafile $ORDERER_CA -C mychannel -n mycc -c "{\"Args\":[\"set\",\"${count}\", \"200\"]}"
                ((count++))
            } 
        done
    }
done
wait

echo "done"
