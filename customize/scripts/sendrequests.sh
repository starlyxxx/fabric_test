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
        export CORE_PEER_ADDRESS=peer$j.org$ORG.example.com:7051
        for ((ops=0; ops<$transaction; ops++));do
            {
                peer chaincode invoke -o orderer.example.com:7050 -C channelall -n mycc -c "{\"Args\":[\"set\",\"${count}\", \"200\"]}" &
                ((count++))
            } 
        done
    }
done
wait

echo "done"
