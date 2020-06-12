#Starly

1. Change the peer and org parameter in run_interface.py.
2. ipAll()/privateIpAll()
3. customize()
4. $bash generate.sh
    tar the customize folder.
5. idParallel()
6. bringUpOrgs()
7. ssh in org1: 
    $sudo docker exec -it cli bash
    $peer channel create -o orderer.example.com:7050 -c channelall -f /opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts/channelall.tx
    $exit
    $sudo docker inspect -f '{{.ID}}' cli
    $sudo docker cp ???:/opt/gopath/src/github.com/hyperledger/fabric/peer/channelall.block /home/ubuntu/fabric-samples/customize/depolyment/
8. gf()
9. ssh in each org:
    $sudo docker inspect -f '{{.ID}}' cli
    $sudo docker cp /home/ubuntu/fabric-samples/customize/depolyment/channelall.block ???:/opt/gopath/src/github.com/hyperledger/fabric/peer/
    $sudo docker cp /home/ubuntu/fabric-samples/customize/scripts ???:/opt/gopath/src/github.com/hyperledger/fabric/peer/
    $sudo docker exec -it cli bash
    $bash joinchannel.sh -o ?
10. Ssh in org1: 
    $export CORE_PEER_ADDRESS=peer0.org1.example.com:7051
    $peer chaincode instantiate -o orderer.example.com:7050 -C channelall -n mycc github.com/chaincode/sacc -v v0 -c '{"Args":["a","100"]}' -P "OR('Org1MSP.member','Org2MSP.member','Org3MSP.member','Org4MSP.member','Org5MSP.member','Org6MSP.member','Org7MSP.member','Org8MSP.member','Org9MSP.member','Org10MSP.member')"
11. ssh in each org:
    $bash setup.sh -o ?
    $bash sendrequests.sh -s ? -o ?
12. getlog()
13. logs will in the log folder under ec2 folder.
