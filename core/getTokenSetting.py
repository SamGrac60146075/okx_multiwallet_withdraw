# 載入設定
import json
config_filepath = 'config.json'
address_filepath = 'wallets.txt'
with open(config_filepath) as f:
    config_dict = json.load(f)

with open(address_filepath) as f:
    address_list = f.read().split()    

import okex.Funding_api as Funding
fundingAPI = Funding.FundingAPI(config_dict['key'], config_dict['secret'], config_dict['passphrase'],False,flag='0')

import pandas as pd
df_coin = pd.DataFrame(fundingAPI.get_currency()['data'])
df_coin = df_coin.loc[df_coin['ccy']==config_dict['token'],['ccy','chain','minWd']].rename(columns={
    "ccy":"token",
    "chain":"network",
    "minWd":"minAmount"
})
print(df_coin)