# 載入設定
import json
config_filepath = 'config.json'
address_filepath = 'wallets.txt'
with open(config_filepath) as f:
    config_dict = json.load(f)

with open(address_filepath) as f:
    address_list = f.read().split()
    
import okex.Funding_api as Funding
import pandas as pd

fundingAPI = Funding.FundingAPI(config_dict['key'], config_dict['secret'], config_dict['passphrase'],False,flag='0')
df_coin = pd.DataFrame(fundingAPI.get_currency()['data'])
minfee = float(df_coin.loc[(df_coin['ccy']==config_dict['token'])&(df_coin['chain']==config_dict['network']),'minFee'])

# 檢查餘額

df_bal = pd.DataFrame(fundingAPI.get_balances()['data'])
df_bal['availBal'] = df_bal['availBal'].astype(float)
bal = float(df_bal.loc[df_bal['ccy']==config_dict['token'],'availBal'])

print(f"餘額: {bal}")

import time
import random
if bal>=(len(address_list)*(config_dict['amount']+minfee)):
    for address in address_list:
        _=fundingAPI.coin_withdraw(ccy=config_dict['token'], amt=config_dict['amount'], dest="4", toAddr=address, pwd="pwd", fee=minfee)
        print(_)
        print(f"送出提幣需求: {config_dict['amount']} {config_dict['network']} - {address}")
        delay = random.randint(config_dict['delay']['min'],config_dict['delay']['max'])
        for t in range(delay):
            print(f'waiting - {delay-t}s', end="\r")
            time.sleep(1)        

    df_bal = pd.DataFrame(fundingAPI.get_balances()['data'])
    df_bal['availBal'] = df_bal['availBal'].astype(float)
    bal = float(df_bal.loc[df_bal['ccy']==config_dict['token'],'availBal'])
    print(f"剩下餘額: {bal}")

else:
    print(f"餘額不足: {bal-(len(address_list)*(config_dict['amount']+minfee))}")