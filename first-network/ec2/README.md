#Starly

1. Change the peer and org parameter in run_interface.py.
2. ipAll()/privateIpAll()
3. kafkapeer()
4. $bash generate.sh
    tar the kafkapeer folder.
5. idParallel()
6. bringUpOrgs()
7. ssh in org1: 
    $sudo docker exec -it cli bash
    $ORDERER_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer0.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
    $peer channel create -o orderer0.example.com:7050 -c mychannel -f ./channel-artifacts/mychannel.tx --tls --cafile $ORDERER_CA
    $exit
    $sudo docker inspect -f '{{.ID}}' cli
    $sudo docker cp ???:/opt/gopath/src/github.com/hyperledger/fabric/peer/mychannel.block /opt/gopath/src/github.com/hyperledger/fabric/kafkapeer/
8. gf()
9. ssh in each org:
    $sudo docker inspect -f '{{.ID}}' cli
    $sudo docker cp /opt/gopath/src/github.com/hyperledger/fabric/kafkapeer/mychannel.block ???:/opt/gopath/src/github.com/hyperledger/fabric/peer/
    $sudo docker cp /opt/gopath/src/github.com/hyperledger/fabric/kafkapeer/scripts ???:/opt/gopath/src/github.com/hyperledger/fabric/peer/
    $sudo docker exec -it cli bash
    $bash ./scripts/joinchannel.sh -o ?
10. Ssh in org1: 
    $export CORE_PEER_ADDRESS=peer0.org1.example.com:7051
    $ORDERER_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer0.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
    $peer chaincode instantiate -o orderer0.example.com:7050 --tls --cafile $ORDERER_CA -C mychannel -n mycc github.com/hyperledger/fabric/kafkapeer/chaincode/go/sacc -v v0 -c '{"Args":["a","100"]}' -P "OR('Org1MSP.member','Org2MSP.member','Org3MSP.member','Org4MSP.member','Org5MSP.member')"
11. ssh in each org:
    $bash ./scripts/setup.sh -o ?
    $bash ./scripts/sendrequests.sh -s ? -o ?
12. getlog()
13. logs will in the log folder under ec2 folder.


PS: chaincode example02 is for transaction scenario, for example, Alice send 20 dollar to Bob. Here is the command examples.
peer chaincode install -n mycc -p github.com/hyperledger/fabric/examples/chaincode/go/example02/cmd/ -v 1.0
ORDERER_CA=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer0.example.com/msp/tlscacerts/tlsca.example.com-cert.pem
peer chaincode instantiate -o orderer0.example.com:7050 --tls --cafile $ORDERER_CA -C mychannel -n mycc -v 1.0 -c '{"Args":["init","a","200","b","400"]}' -P "OR ('Org1MSP.peer','Org2MSP.peer','Org3MSP.peer','Org4MSP.peer','Org5MSP.peer')"
peer chaincode invoke --tls --cafile $ORDERER_CA -C mychannel -n mycc -c '{"Args":["invoke","a","b","20"]}'