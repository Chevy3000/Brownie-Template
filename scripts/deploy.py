from scripts.helpful_scripts import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from brownie import DappToken, TokenFarm, config, network
from web3 import Web3
import yaml
import json
import os
import shutil

KEPT_BALANCE = Web3.toWei(100, "ether")


def deploy_token_farm_and_dapp_token(update_front_end=False):
    account = get_account()
    dappToken = DappToken.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    tokenFarm = TokenFarm.deploy(
        dappToken.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    tx = dappToken.transfer(
        tokenFarm.address, dappToken.totalSupply() - KEPT_BALANCE, {"from": account}
    )
    tx.wait(1)
    available_tokens = {
        dappToken: get_contract("dai_usd_price_feed"),
        get_contract("weth_token"): get_contract("eth_usd_price_feed"),
    }
    addAllowedTokens(tokenFarm, available_tokens, account)
    if update_front_end:
        updateFrontEnd()
    return tokenFarm, dappToken


def addAllowedTokens(tokenFarm, tokenFeedDict, account):
    for token in tokenFeedDict:
        tx = tokenFarm.addAllowedToken(
            token.address, tokenFeedDict[token], {"from": account}
        )
        tx.wait(1)


def updateFrontEnd():
    copy_folders("./build", "./front_end/src/chain-info")
    with open("brownie-config.yaml", "r") as bc:
        config_dict = yaml.load(bc, Loader=yaml.FullLoader)
        with open("./front_end/src/brownie-config.json", "w") as bcj:
            json.dump(config_dict, bcj)
    print("Front end updated")


def copy_folders(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def main():
    update_front_end = network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
    deploy_token_farm_and_dapp_token(update_front_end)
