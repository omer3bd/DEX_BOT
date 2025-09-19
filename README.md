# ⚠️ Disclaimer:
This bot is not a perfect system and does not provide financial advice. Please **conduct your own research** before making any financial decisions. Any financial losses or other consequences resulting from the use of this bot are solely **your responsibility**.



# DEX_BOT

## project background
this is a personal project made to check for honeypots and other traps that can be found in the blockchain. This helps to find whether or not the dev has renounced the contract (coin), locked liquidity, burned tokens etc. The main goal of the project was to help the redundant work of manual time consuming checks that now can be done by simply copying and pasting in the contact addresses in the bot and it uses APi from etherscan and other websites to verify the credibility of a project. 


## how to use
1. use `db.py` as script. run it in an IDE ideally.

  **Libraries used are** dotenv, Web3, requests:
  ```bash
  pip install dotenv Web3 requests
```

2. add your api keys to `.env` and add that to your dotenv 
   
```bash
ETHERSCAN_API_KEY=example2FFUNPYERC22lkn234l
CG_API_KEY=your_coingecko_api_key

WEB3_PROVIDER=https://mainnet.infura.io/v3/example99bf34ed9a5c306d303bf

WEB3_PROVIDER_KEY=example66fg340d88dd9a5c40db304bf

WEB3_API_KEY=example66bf340308dd9a5c406b324bf

DISCORD_TOKEN=exampleDc3ODAyOA.GL9XIIWfZx9IE

WALLET_ADDRESS=0xD20f0C15357exampled6c737F47673367B401e1C

PRIVATE_KEY=your_private_key
```
