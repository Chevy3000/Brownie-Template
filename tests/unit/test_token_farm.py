from brownie import network, config, TokenFarm, DappToken, exceptions
from scripts.helpful_scripts import get_account, get_contract, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_token_farm_and_dapp_token
import pytest

def test_allow_and_price_feed():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    eth_feed = get_contract("eth_usd_price_feed")
    dai_feed = get_contract("dai_usd_price_feed")

    tx = token_farm.addAllowedToken(
        dapp_token.address,
        get_contract("eth_usd_price_feed"), 
        {"from":account})
    tx.wait(1)

    print(f"token feed = {token_farm.tokenPriceFeed(dapp_token.address)}")
    print(f"eth feed = {eth_feed}")    
    print(f"dai feed = {dai_feed}")

    assert token_farm.tokenPriceFeed(dapp_token.address)== get_contract("eth_usd_price_feed")
    assert token_farm.allowedTokens(0)==dapp_token.address
    tx = token_farm.setPriceFeedContract(dapp_token.address, get_contract("dai_usd_price_feed"), {"from":account} )
    tx.wait(1)
    assert token_farm.tokenPriceFeed(dapp_token.address)== get_contract("dai_usd_price_feed")

    with pytest.raises(exceptions.VirtualMachineError):
        tx = token_farm.setPriceFeedContract(dapp_token.address, get_contract("dai_usd_price_feed"), {"from":non_owner})
        tx.wait(1)
    with pytest.raises(exceptions.VirtualMachineError):
        tx = token_farm.addAllowedToken(
            dapp_token.address,
            get_contract("eth_usd_price_feed"), 
            {"from":non_owner})
        tx.wait(1)


def test_stake_and_issue_tokens(ammount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()

    dapp_token.approve(token_farm.address,ammount_staked, {"from":account})
    token_farm.stakeTokens(ammount_staked, dapp_token.address, {"from":account})

    assert token_farm.stakingBalance(dapp_token.address, account.address)== ammount_staked
    assert token_farm.uniqueTokensStaked(account.address)==1
    assert token_farm.stakers(0) == account.address
    
    starting_balance = dapp_token.balanceOf(account.address)
    tx = token_farm.issueTokens({"from":account})
    tx.wait(1)
    assert dapp_token.balanceOf(account.address)== starting_balance + ammount_staked/10


