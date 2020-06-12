#!/bin/bash
#Author: Starly

../bin/cryptogen generate --config=./crypto-config.yaml
export FABRIC_CFG_PATH=$PWD
../bin/configtxgen -profile ThreeOrgsOrdererGenesis -outputBlock ./channel-artifacts/genesis.block
../bin/configtxgen -profile ChannelAll -outputCreateChannelTx ./channel-artifacts/channelall.tx -channelID channelall