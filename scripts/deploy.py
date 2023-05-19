from scripts.helpful_scripts import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    is_verifiable_contract,
)
from brownie import Template
from web3 import Web3
import yaml
import json
import os
import shutil


def deploy_template(update_front_end=False):
    account = get_account()
    template = Template.deploy(
        {"from": account}, publish_source=is_verifiable_contract()
    )


def main():
    deploy_template()
