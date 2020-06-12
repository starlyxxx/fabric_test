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

for ((j=0; j<$PEER; j++));do
    {
        let port=7051+$j*100
        export CORE_PEER_ADDRESS=peer$j.org$ORG.example.com:$port  
        peer channel join -b mychannel.block
    }
done
wait

for ((j=0; j<$PEER; j++));do
    {
        let port=7051+$j*100
        export CORE_PEER_ADDRESS=peer$j.org$ORG.example.com:$port 
        peer chaincode install -n mycc -p github.com/hyperledger/fabric/kafkapeer/chaincode/go/sacc -v v0
    }
done
wait

echo "done"