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
        export CORE_PEER_ADDRESS=peer$j.org$ORG.example.com:7051
        peer channel join -b ../channelall.block
    }
done
wait

for ((j=0; j<$PEER; j++));do
    {
        export CORE_PEER_ADDRESS=peer$j.org$ORG.example.com:7051
        peer chaincode install -n mycc -p github.com/chaincode/sacc -v v0
    }
done
wait

echo "done"