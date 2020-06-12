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
        export CORE_PEER_ADDRESS=peer$j.org${ORG}.example.com:7051
        peer chaincode invoke -o orderer.example.com:7050 -C channelall -n mycc -c "{\"Args\":[\"set\",\"${count}\", \"200\"]}"
        ((count++))
    }
done

echo "done"
