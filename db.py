# from urllib.request import proxy_bypass_registry

from dotenv import load_dotenv
import os
import time
from web3 import Web3
import requests
from datetime import datetime
import sys
from web3.exceptions import BadFunctionCallOutput, ContractLogicError


class Dex_check:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # current time
        self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # BOT status
        self.get_info_status = False
        self.check_honeypot_status = True

        # Load environment variables
        self.CG_API_KEY = os.getenv("CG_API_KEY")
        self.WEB3_PROVIDER = os.getenv("WEB3_PROVIDER")
        self.WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
        self.PRIVATE_KEY = os.getenv("PRIVATE_KEY")
        self.ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
        self.WEB3_PROVIDER_KEY = os.getenv("WEB3_PROVIDER_KEY")

        # Initialize Web3
        self.code = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER")))
        self.w3 = Web3(Web3.HTTPProvider(self.WEB3_PROVIDER))
        # self.get_code = self.w3.eth.get_code(Web3.to_checksum_address(self.tk_address))

        # addresses
        self.ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
        self.DEAD_ADDRESS = "0x000000000000000000000000000000000000dEaD"

        #
        self.UNISWAP_PAIR_ABI = [
            {"constant": True, "inputs": [], "name": "token0", "outputs": [{"name": "", "type": "address"}], "type": "function"},
            {"constant": True, "inputs": [], "name": "token1", "outputs": [{"name": "", "type": "address"}], "type": "function"},
            {"constant": True, "inputs": [], "name": "getReserves", "outputs": [
                {"name": "_reserve0", "type": "uint112"},
                {"name": "_reserve1", "type": "uint112"},
                {"name": "_blockTimestampLast", "type": "uint32"}], "type": "function"}
        ]

        #
        self.ERC20_ABI = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "symbol",
                "outputs": [{"name": "", "type": "string"}],
                "type": "function"
            },
        ]

        # CoinGecko api
        # self.url = (f"https://api.etherscan.io/api?module=contract&action=getabi"
        # "&address={self.tk_address}&apikey={self.ETHERSCAN_API_KEY}")

        # Using Etherscan API to find a pair (simplified)


        print("\n================= WELCOME TO DEX BOT =================\n")

    def __str__(self):
        return (">>Quick info<<\n"
                "----------------\n"
                "1. '0x000...dEaD':\n\n"
                "A dead address is a special wallet address where tokens\n"
                "are sent to be permanently removed from circulation(token burning)..\n"
                ">>Safe ranges:<<\n"
                "1–10%	| Modest\n"
                "10–50%	| Aggressive deflationary model\n"
                "50%+ | Extreme — often used by meme or hyper-deflationary tokens\n"
                ">90% | 🚩 Often a trick to make the remaining supply seem scarce or mislead buyers\n"
                "----------------\n"
                "2. 0x000...0000:\n"
                "It's used in token when:"
                "Minting: New tokens \"come from\" the zero address"
                "Burning: Some tokens get \"sent\" to the zero address (less common than 0x000...dead)\""
                "Uninitialized ownership: Acts as a placeholder or null value"
                "| Zero Address % | Interpretation                                          | Safe?                       |"
                "| -------------- | ------------------------------------------------------- | --------------------------- |"
                "|   0%           | Normal for most modern tokens                           | ✅ Yes                       |"
                "|   <1–5%        | Possibly used for early burns or mints                  | ✅ Yes                       |"
                "|   5–20%        | Somewhat unusual; double-check intent                   | ⚠️ Caution                  |"
                "|   20–90%       | Claims of burn via zero address — may mislead investors | ⚠️ Red flag unless verified |"
                "|   >90%         | High likelihood of being used to fake scarcity          | 🚨 Danger zone              |")

    def get_pair_address(self):

        # Pair address
        print("+-----------------------------------------------------------+")
        self.pair_address = ("0x06fdb856f79c56f012fb793c23fbb64c66dcfb66")
        # self.pair_address = input("| Enter the pair address:                                   |\n"
        #                           "| ->")
        if self.pair_address == 'i':
            print("+-----------------------------------------------------------+")
            self.get_info_status = True
            return None
        else:
            print(f"| Pair Address: {self.pair_address}  |")
            return self.pair_address

    def get_token_address(self):
        # Token address
        self.tk_address = ("0xca13e6ed4d267d0f41fe5a18b4200e5989a81e37")
        # self.tk_address = input("| Enter the token address:                                  |\n"
        #                         "| ->")
        if self.tk_address == 'i':
            print("+-----------------------------------------------------------+")
            self.get_info_status = True
            return None
        else:
            print(f"| Token Address: {self.tk_address} |")
            print("+-----------------------------------------------------------+")
            return self.tk_address

    def get_info(self):
        if self.get_info_status == True:
            print("\n\n>> Quick Info <<")
            print("----------------")
            print("1. 🔥 Burn Address (`0x000...dEaD`):\n")
            print("A *dead address* is a non-recoverable wallet where tokens are sent to be")
            print("**permanently removed from circulation** (aka token burning). This reduces")
            print("the total supply and can drive price upwards — if done responsibly.\n")

            print(">> Safe Ranges for Burn % (Dead Address):")
            print("+-----------+-------------------------------------------------------------+")
            print("| Burn %    | Interpretation                                              |")
            print("+-----------+-------------------------------------------------------------+")
            print("| 1–10%     | Modest — used for stability or light deflation             |")
            print("| 10–50%    | Aggressive deflationary model — common in meme tokens      |")
            print("| 50%+      | Extreme — often signals unsustainable tokenomics           |")
            print("| >90%      | 🚩 Likely attempt to fake scarcity or mislead buyers        |")
            print("+-----------+-------------------------------------------------------------+\n\n")

            print("2. 🧊 Zero Address (`0x000...0000`):\n")
            print("The **zero address** is used in several smart contract functions as a")
            print("placeholder or null value. While not typically used for burns, some")
            print("tokens send assets here during:\n"
                  "   - Minting (new tokens 'come from' zero address)\n"
                  "   - Burn events (less common but possible)\n"
                  "   - Ownership transitions (uninitialized owner = zero address)\n")

            print(">> Interpreting Zero Address Holdings (% of total supply):")

            print(
                "+----------------+--------------------------------------------------------+----------------------------+")
            print(
                "| Zero Address % | Interpretation                                         | Safe?                     |")
            print(
                "+----------------+--------------------------------------------------------+----------------------------+")
            print(
                "| 0%             | Normal for most modern tokens                          | ✅ Yes                    |")
            print(
                "| <1–5%          | Possibly used for early burns or mints                 | ✅ Yes                    |")
            print(
                "| 5–20%          | Somewhat unusual; double-check intent                  | ⚠️ Caution                |")
            print(
                "| 20–90%         | Claims of burn via zero address — may mislead         | ⚠️ Red flag unless verified |")
            print(
                "| >90%           | 🚨 Likely fake scarcity — risk of manipulation         | ❌ Danger Zone            |")
            print(
                "+----------------+--------------------------------------------------------+----------------------------+\n")

            print("🔎 Tip: Always verify if the burn address or zero address balance was sent\n"
                  "from a real wallet or a mint function. Fake burns from dev wallets can be\n"
                  "retrieved later if the contract isn't renounced or if minting is allowed.\n")
            sys.exit()

        else:
            pass

    def initialize(self):
        """
        Fetch and print coin details: name, price, age, liquidity, and market cap.
        Format: "$AURA | 0.0034 ETH | 3 days old | $114.7k Liquidity | $300.42K market cap"
        """
        token_address = self.tk_address
        pair_address = self.pair_address
        cg_api_key = self.CG_API_KEY
        etherscan_api_key = self.ETHERSCAN_API_KEY
        w3 = self.w3

        # --- Get token info from CoinGecko ---
        try:
            # CoinGecko API: get token info by contract address (Ethereum) name, price, market cap
            cg_url = f"https://api.coingecko.com/api/v3/coins/ethereum/contract/{token_address}"
            cg_resp = requests.get(cg_url)
            if cg_resp.status_code == 200:
                cg_data = cg_resp.json()
                name = cg_data.get('symbol', None)
                price = cg_data.get('market_data', {}).get('current_price', {}).get('eth', None)
                market_cap = cg_data.get('market_data', {}).get('market_cap', {}).get('usd', None)
            else:
                name = None
                price = None
                market_cap = None
        except Exception as e:
            print(f"Error fetching CoinGecko data: {e}")
            name = None
            price = None
            market_cap = None

        # --- Fallback: Get name and symbol from token contract if CoinGecko fails ---
        if not name or name == 'N/A':
            try:
                ERC20_ABI = [
                    {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}], "type": "function"}
                ]
                token_contract = w3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
                symbol = token_contract.functions.symbol().call()
                name = symbol
            except Exception as e:
                print(f"\nError fetching token contract symbol: {e}")
                name = 'N/A name'

        # --- Get contract creation date from Etherscan ---
        try:
            etherscan_url = (f"https://api.etherscan.io/api?module=contract&action=getcontractcreation"
                             f"&contractaddresses={token_address}&apikey={etherscan_api_key}")
            eth_resp = requests.get(etherscan_url)
            if eth_resp.status_code == 200:
                eth_data = eth_resp.json()
                result = eth_data.get('result', [])
                if result and isinstance(result, list):
                    ts = int(result[0].get('timestamp', 0))
                    age_days = (int(time.time()) - ts) // 86400
                else:
                    age_days = 'N/A'
            else:
                age_days = 'N/A'
        except Exception as e:
            print(f"Error fetching contract creation date: {e}")
            age_days = 'N/A'

        # --- Get liquidity from Uniswap (via pair contract) ---
        try:
            PAIR_ABI = [{
                "constant": True,
                "inputs": [],
                "name": "getReserves",
                "outputs": [
                    {"name": "_reserve0", "type": "uint112"},
                    {"name": "_reserve1", "type": "uint112"},
                    {"name": "_blockTimestampLast", "type": "uint32"}
                ],
                "payable": False,
                "stateMutability": "view",
                "type": "function"
            }, {
                "constant": True,
                "inputs": [],
                "name": "token0",
                "outputs": [{"name": "", "type": "address"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function"
            }]
            pair_contract = w3.eth.contract(address=Web3.to_checksum_address(pair_address), abi=PAIR_ABI)
            reserves = pair_contract.functions.getReserves().call()
            token0 = pair_contract.functions.token0().call()
            if token0.lower() == token_address.lower():
                token_reserve = reserves[0]
                eth_reserve = reserves[1]
            else:
                token_reserve = reserves[1]
                eth_reserve = reserves[0]
            # Convert ETH reserve to ETH
            liquidity_eth = w3.from_wei(eth_reserve, 'ether')
            # Estimate liquidity in USD if price is available
            liquidity_usd = float(liquidity_eth) * cg_data.get('market_data', {}).get('current_price', {}).get('usd', 0) if price else None
        except Exception as e:
            print(f"Error fetching liquidity: {e}")
            liquidity_eth = 'N/A'
            liquidity_usd = None

        # --- Format output ---
        price_str = f"{price:.4f} ETH" if price else "N/A price"
        age_str = f"{age_days} days old" if age_days != 'N/A' else "N/A"
        if liquidity_usd:
            liquidity_str = f"${liquidity_usd:,.1f} Liquidity"
        elif liquidity_eth != 'N/A':
            liquidity_str = f"{liquidity_eth} ETH Liquidity"
        else:
            liquidity_str = "N/A Liquidity"
        market_cap_str = f"${market_cap:,.2f} market cap" if market_cap else "N/A market cap"
        print("\n+----------------------------------------------------------------------------------------")
        print(f"|  ${name} | {price_str} | {age_str} | {liquidity_str} | {market_cap_str}")    # $COIN | price | 7 days old | 1.66811815606150434 ETH Liquidity | N/A market cap
        print("+----------------------------------------------------------------------------------------")

    # INACTIVE
    def check_liquidity_web3(self):
        UNISWAP_FACTORY_ADDRESS = Web3.to_checksum_address(
            "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f")  # Uniswap V2

        UNISWAP_FACTORY_ABI = [{
            "inputs": [
                {"internalType": "address", "name": "tokenA", "type": "address"},
                {"internalType": "address", "name": "tokenB", "type": "address"},
            ],
            "name": "getPair",
            "outputs": [{"internalType": "address", "name": "pair", "type": "address"}],
            "stateMutability": "view",
            "type": "function"
        }]

        PAIR_ABI = [{
            "constant": True,
            "inputs": [],
            "name": "getReserves",
            "outputs": [
                {"name": "_reserve0", "type": "uint112"},
                {"name": "_reserve1", "type": "uint112"},
                {"name": "_blockTimestampLast", "type": "uint32"}
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        }, {
            "constant": True,
            "inputs": [],
            "name": "token0",
            "outputs": [{"name": "", "type": "address"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        }]

        # --- Connect to blockchain ---
        web3 = Web3(Web3.HTTPProvider(self.WEB3_PROVIDER))
        print("1")
        factory_contract = web3.eth.contract(address=UNISWAP_FACTORY_ADDRESS, abi=UNISWAP_FACTORY_ABI)
        print("2")
        '''
        Get pass address asks for: Web3.to_checksum_address(token address).lower
        but i cant find a work around it so checking liq with web3 is not happening 
        '''
        # Get pair address
        pair_addy = factory_contract.functions.getPair(self.tk_address, self.pair_address).call()
        if pair_addy == "0x0000000000000000000000000000000000000000":
            print("Pair does not exist.")
            exit()
        print("3")
        pair_contract = web3.eth.contract(address=pair_addy, abi=PAIR_ABI)

        # Get reserves
        reserves = pair_contract.functions.getReserves().call()
        token0 = pair_contract.functions.token0().call()

        # Sort reserves correctly based on token0/token1 order
        if token0.lower() == self.tk_address.lower():
            token_reserve = reserves[0]
            weth_reserve = reserves[1]
        else:
            token_reserve = reserves[1]
            weth_reserve = reserves[0]

        # Output liquidity
        print(f"Token Liquidity: {web3.from_wei(token_reserve, 'ether')} tokens")
        print(f"Pair (WETH) Liquidity: {web3.from_wei(weth_reserve, 'ether')} ETH")

    def check_lp_holders(self):
        # === Setup ===
        rpc_url = self.WEB3_PROVIDER  # Or BSC RPC, etc.
        web3 = self.w3

        pair_address = Web3.to_checksum_address(self.pair_address)  # LP contract address

        # === Minimal ABI for UniswapV2 Pair ===
        pair_abi = [
            {
                "constant": True,
                "inputs": [],
                "name": "getReserves",
                "outputs": [
                    {"internalType": "uint112", "name": "reserve0", "type": "uint112"},
                    {"internalType": "uint112", "name": "reserve1", "type": "uint112"},
                    {"internalType": "uint32", "name": "blockTimestampLast", "type": "uint32"}
                ],

                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "token0",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "token1",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "type": "function"
            }
        ]

        # === Interact with the pair contract ===
        pair_contract = web3.eth.contract(address=pair_address, abi=pair_abi)

        token0 = pair_contract.functions.token0().call()
        token1 = pair_contract.functions.token1().call()
        reserves = pair_contract.functions.getReserves().call()

        from decimal import Decimal

        reserve0 = Decimal(51104896621807019) / Decimal(10 ** 18)  # Token0
        reserve1 = Decimal(41099550562457115813) / Decimal(10 ** 18)  # WETH

        # print(f"| Token0 Reserve: {reserve0}")      # Token0 Reserve: 0.051104896621807019
        # print(f"| WETH Reserve: {reserve1}")        # WETH Reserve: 41.099550562457115813
        #
        # print(f"| Token0 Address: {token0}")        # Token0: 0xBFe55ce2F36D6BDA3D97993Ff989fAD95D8D3317
        # print(f"| Token1 : {token1}")               # Token1: 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
        # 3 (reserve0, reserve1)
        # print(f"| Reserves: {reserves}")            # Reserves: [51104896621807019, 41099550562457115813, 1752736091]

        #
        price_in_weth = reserve1 / reserve0
        # print("Price (Token0 in WETH):", price_in_weth)     # Price (Token0 in WETH): 804.2194247374621933503939804

        # Assume 1 WETH = $3,200 (you can fetch this from API or use Chainlink)
        weth_price_usd = Decimal(3200)

        token_price_usd = price_in_weth * weth_price_usd
        # print("Price in USD:", token_price_usd)             # Price in USD: 2573502.159159879018721260737

        print("\n\n+---------------------------+------------------------------------------------------------+")
        print("| Parameter                 | Value                                                      |")
        print("+---------------------------+------------------------------------------------------------+")
        print(f"| Token0 Address            | {token0}                 |")
        print(f"| Token1 (WETH) Address     | {token1}                 |")
        print("+---------------------------+------------------------------------------------------------+")
        print(f"| Token0 Reserve            | {reserve0}                                       |")
        print(f"| WETH Reserve              | {reserve1}                                      |")
        print("+---------------------------+------------------------------------------------------------+")
        print(f"| Price (Token0 in WETH)   | {price_in_weth}                               |")
        print(f"| Price (Token0 in USD)    | ${token_price_usd}                              |")
        print("+---------------------------+------------------------------------------------------------+")
        print("| Raw Token0 Reserve (wei),   Raw WETH Reserve (wei),     Last Updated Timestamp:        |")
        print(f"| {reserves}")
        print("+---------------------------+------------------------------------------------------------+")
        '''
        Reserves: [51 104 896 621 807 019, 41099550562457115813, 1752736091]
        '''



    def check_launch_limits(self):
        # Setup your RPC URL
        RPC = self.WEB3_PROVIDER
        web3 = Web3(Web3.HTTPProvider(RPC))

        # Example token contract (replace with the one you want to check)
        TOKEN_ADDRESS = Web3.to_checksum_address(self.tk_address)

        # Common ABI snippets for reading standard public variables
        ABI_VARIABLES = [
            {"name": "maxTxAmount", "type": "uint256"},
            {"name": "minTxAmount", "type": "uint256"},
            {"name": "maxWallet", "type": "uint256"},
            {"name": "cooldownEnabled", "type": "bool"},
            {"name": "cooldown", "type": "uint256"},
            {"name": "walletLimit", "type": "uint256"},
            {"name": "maxBuyAmount", "type": "uint256"},
            {"name": "minBuy", "type": "uint256"},
        ]

        # Create dummy ABI to access public variables
        def make_dummy_abi(var_name, var_type):
            return {
                "constant": True,
                "inputs": [],
                "name": var_name,
                "outputs": [{"name": "", "type": var_type}],
                "payable": False,
                "stateMutability": "view",
                "type": "function",
            }

        # Build contract with basic ABI
        def build_contract_with_var(var_name, var_type):
            abi = [make_dummy_abi(var_name, var_type)]
            return web3.eth.contract(address=TOKEN_ADDRESS, abi=abi)

        # Attempt to call each known variable
        def check_token_limits():
            print("\n\nToken Limits:")
            print("+---------------------------------------------+")
            for var in ABI_VARIABLES:
                try:
                    contract = build_contract_with_var(var["name"], var["type"])
                    result = contract.functions.__getattribute__(var["name"])().call()
                    print("| maxTxAmount     ➤ Not found or inaccessible |")
                    print(f"{var['name']:15} ➤ {result}")
                except Exception as e:
                    print(f"| {var['name']:15} ➤ Not found or inaccessible |")
            print("+---------------------------------------------+")

        check_token_limits()

    # INACTIVE
    def get_coin_socials(self):
        pass

    def check_owner_permissions(self):
        # -------- Check Token Owner's Permissions (Minting / Blacklist / Pausable) --------

        # Fetch ABI from Etherscan
        abi_url = (f"https://api.etherscan.io/api?module=contract&action=getabi"
                   f"&address={self.tk_address}"
                   f"&apikey={self.ETHERSCAN_API_KEY}")
        abi_response = requests.get(abi_url)
        abi = abi_response.json().get("result", "[]")
        contract = self.w3.eth.contract(address=Web3.to_checksum_address(self.tk_address), abi=abi)

        function_names = [item['name'] for item in contract.abi if item['type'] == 'function']

        risky_methods = ['setTax', 'mint', 'pause', 'blacklist', 'enableTrading', 'setFees',
                         'withdraw', 'rescueTokens', 'transferOwnership', 'renounceOwnership',
                         'setMarketingWallet', 'startAirdrop', 'startPresale', 'removeLiquidity',
                         'approveRouter', 'setRouter', 'setPair', 'antiBot', 'setCooldown',
                         'setMaxTxAmount',
                         'upgradeTo', 'upgradeImplementation', 'delegatecall', 'admin']

        risky_found = [f for f in risky_methods if f in function_names]


        if risky_found:
            print("\n\n🚨  Risky functions in the code:")
            print("+-------------------------------------------------------------------------------+")
            print(f"| ⚙ Functions found:                                                            |\n"
                  f"|      {risky_found}")
            print("|  --------------------------------------------------------                     |")

        else:
            print("\n\n+--------------------------------------------------------------------------------+")
            print("| ❇️ No risky functions found in token contract.                                  |")
            print("+--------------------------------------------------------------------------------+")




        # --- Check if ownership is renounced ---
        owner_address = None
        renounced = False

        try:
            # Try common owner() pattern
            if 'owner' in function_names:
                owner_address = contract.functions.owner().call()
            elif 'getOwner' in function_names:
                owner_address = contract.functions.getOwner().call()
            else:
                owner_address = None
        except Exception as e:
            owner_address = None

        if owner_address:
            if owner_address.lower() in ["0x0000000000000000000000000000000000000000", "0x000000000000000000000000000000000000dEaD"]:
                renounced = True
                print("|     ❇️     Ownership is renounced.                                             |")
                print("+-------------------------------------------------------------------------------+")
            else:
                print(f"    ⚠️      Ownership is NOT renounced. Owner address: {owner_address}")
                print("---------------------------------------------------------------------------------")
        else:
            print("     ⚠️      Could not determine owner address (non-standard contract or missing ABI)")
            print("---------------------------------------------------------------------------------")

        # --- Warn if risky functions are present + owner not renounced ---
        if risky_found and not renounced:
            print("     🚨 WARNING: Risky functions are present and ownership is NOT renounced.\n"
                  "     The owner can potentially abuse these functions\n"
                  "     (e.g., change fees, blacklist users, pause trading, etc.)!")
            print("---------------------------------------------------------------------------------")
        elif not risky_found and not renounced:
            print("     ⚠️ Ownership is not renounced, but no high-risk functions detected.")
            print("---------------------------------------------------------------------------------")
        # If renounced, no further warning needed

    def top_holders(self, limit=10):
        """
        Fetch and print the top token holders using Ethplorer API.
        After listing, print zero and dead address holdings if present, with percent and USD value if possible.
        """
        holders_url = f"https://api.ethplorer.io/getTopTokenHolders/{self.tk_address}?apiKey=freekey&limit={limit}"

        try:
            holders_resp = requests.get(holders_url)
            holders_data = holders_resp.json()

            top_holders = holders_data.get("holders", [])

            if not top_holders:
                print("⚠️ No top holders found or token not indexed by Ethplorer.")
                return []

            print("\n🔝 Top {} Holders:".format(limit))
            print("+--------------------------------------------------")
            for i, holder in enumerate(top_holders, 1):
                address = holder["address"]
                holder_balance = int(holder["balance"])
                percent = holder.get("share", 0)
                print(f"|    {i}. {address} ➤ {holder_balance} tokens ➤ ({percent:.2f}%)")
            print("+--------------------------------------------------")

            # Check for zero and dead address
            zero_address = "0x0000000000000000000000000000000000000000"
            dead_address = "0x000000000000000000000000000000000000dead"

            zero_holder = next((h for h in top_holders if h["address"].lower() == zero_address), None)
            dead_holder = next((h for h in top_holders if h["address"].lower() == dead_address), None)

            # Try to get price in USD for estimation
            price_usd = None
            try:
                cg_url = f"https://api.coingecko.com/api/v3/coins/ethereum/contract/{self.tk_address}"
                cg_resp = requests.get(cg_url)
                if cg_resp.status_code == 200:
                    cg_data = cg_resp.json()
                    price_usd = cg_data.get('market_data', {}).get('current_price', {}).get('usd', None)
            except Exception:
                pass

            if zero_holder:
                z_percent = zero_holder.get("share", 0)
                if price_usd:
                    usd_value = int(zero_holder["balance"]) * price_usd / (10 ** 18)
                    print(f"\n'Zero address' holds ({z_percent:.0f}%) of circulation: ${usd_value:,.2f}")
                else:
                    print(f"\n'Zero address' holds ({z_percent:.0f}%) of circulation (USD value unavailable)")

                if z_percent == 0:
                    print("'Zero address' exists and empty — normal for most tokens.")
                elif 0 < z_percent < 10:
                    print("'Zero address' detected: Possibly used for early burns or mints")
                elif 10 <= z_percent < 20:
                    print("⚠️ Caution! large amount in 'zero address': Burned tokens should go to '0x000...dEaD', not the '0x000...0000'.")
                elif z_percent > 90:
                    print("🚨 Danger zone: High likelihood of being used to fake scarcity. Burned tokens should go to '0x000...dEaD', not the '0x000...0000'.")
            else:
                print("\n❌ 'Zero address' not found in top holders.")

            if dead_holder:
                d_percent = dead_holder.get("share", 0)
                if price_usd:
                    usd_value = int(dead_holder["balance"]) * price_usd / (10 ** 18)
                    print(f"'Dead address' holds ({d_percent:.0f}%) of circulation: ${usd_value:,.2f}")
                else:
                    print(f"'Dead address' holds ({d_percent:.0f}%) of circulation (USD value unavailable)")
                if 10 < d_percent < 50:
                    print("'Dead address' is in a safe range of 10% - 50% of circulation burned")
            else:
                print("❌ 'Dead address' not found in top holders.")

            return top_holders

        except Exception as e:
            print(f"Error fetching top holders: {e}")
            return []

    def check_token_sniffer(self):
        """
        Fetch and print comprehensive token analysis from TokenSniffer API.
        Includes score, swap analysis, contract analysis, holder analysis, and liquidity analysis.
        """
        token_address = self.tk_address

        try:
            # TokenSniffer API endpoint
            ts_url = f"https://tokensniffer.com/token/{token_address}"

            # Note: TokenSniffer doesn't have a public API, so we'll use web scraping or alternative
            # For now, we'll use a combination of existing data and format it like TokenSniffer

            print("\n" + "=" * 60)
            print("🔍 TOKEN SNIFFER ANALYSIS")
            print("=" * 60)

            # --- Score Calculation (based on our checks) ---
            score = 0
            max_score = 100

            # Check honeypot status
            try:
                hp_url = f"https://api.honeypot.is/v2/IsHoneypot?address={token_address}"
                hp_resp = requests.get(hp_url)
                if hp_resp.status_code == 200:
                    hp_data = hp_resp.json()
                    if not hp_data.get("isHoneypot"):
                        score += 25
                        print("✅ Token is sellable (not a honeypot)")
                    else:
                        print("❌ Token is a honeypot")

                    buy_tax = hp_data.get("buyTax", 0)
                    sell_tax = hp_data.get("sellTax", 0)

                    if buy_tax < 5:
                        score += 15
                        print(f"✅ Buy fee is less than 5% ({buy_tax}%)")
                    else:
                        print(f"⚠️ Buy fee is high: {buy_tax}%")

                    if sell_tax < 5:
                        score += 15
                        print(f"✅ Sell fee is less than 5% ({sell_tax}%)")
                    else:
                        print(f"⚠️ Sell fee is high: {sell_tax}%")
            except Exception as e:
                print(f"⚠️ Could not check honeypot status: {e}")

            # Check ownership
            try:
                abi_url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={token_address}&apikey={self.ETHERSCAN_API_KEY}"
                abi_resp = requests.get(abi_url)
                if abi_resp.status_code == 200:
                    abi_data = abi_resp.json()
                    if abi_data.get("result") != "Contract source code not verified":
                        score += 10
                        print("✅ Verified contract source")
                    else:
                        print("⚠️ Contract source not verified")
            except Exception as e:
                print(f"⚠️ Could not check contract verification: {e}")

            # Check liquidity lock
            try:
                # Check Team.Finance
                tf_url = f"https://api.team.finance/v1/token/eth/{self.pair_address}/locks"
                tf_resp = requests.get(tf_url)
                if tf_resp.status_code == 200:
                    tf_data = tf_resp.json()
                    locks = tf_data.get('result', [])
                    if locks:
                        score += 20
                        total_locked = sum(lock.get('amount', 0) for lock in locks)
                        print(f"✅ Liquidity locked: {total_locked} tokens")
                    else:
                        print("⚠️ No liquidity lock found")
            except Exception as e:
                print(f"⚠️ Could not check liquidity lock: {e}")

            # Check holder distribution
            try:
                holders_url = f"https://api.ethplorer.io/getTopTokenHolders/{token_address}?apiKey=freekey&limit=10"
                holders_resp = requests.get(holders_url)
                if holders_resp.status_code == 200:
                    holders_data = holders_resp.json()
                    holders = holders_data.get("holders", [])

                    if holders:
                        top_10_percent = sum(holder.get("share", 0) for holder in holders[:10])
                        if top_10_percent < 70:
                            score += 15
                            print(f"✅ Top 10 holders possess less than 70% of supply ({top_10_percent:.2f}%)")
                        else:
                            print(f"⚠️ Top 10 holders possess {top_10_percent:.2f}% of supply (concentrated)")

                        # Check creator wallet (first holder)
                        if holders:
                            creator_percent = holders[0].get("share", 0)
                            if creator_percent < 5:
                                score += 10
                                print(f"✅ Creator wallet contains less than 5% of supply ({creator_percent:.1f}%)")
                            else:
                                print(f"⚠️ Creator wallet contains {creator_percent:.1f}% of supply")
            except Exception as e:
                print(f"⚠️ Could not check holder distribution: {e}")

            print(f"\n📊 SCORE: {score}/{max_score}")

            # --- Detailed Analysis Sections ---
            print("\n" + "-" * 40)
            print("SWAP ANALYSIS")
            print("-" * 40)
            try:
                if hp_resp.status_code == 200:
                    hp_data = hp_resp.json()
                    print(f"Token is sellable: {'Yes' if not hp_data.get('isHoneypot') else 'No'}")
                    print(f"Buy fee: {hp_data.get('buyTax', 'N/A')}%")
                    print(f"Sell fee: {hp_data.get('sellTax', 'N/A')}%")
            except:
                print("Could not fetch swap analysis")

            print("\n" + "-" * 40)
            print("CONTRACT ANALYSIS")
            print("-" * 40)
            try:
                if abi_resp.status_code == 200:
                    abi_data = abi_resp.json()
                    print(
                        f"Contract verified: {'Yes' if abi_data.get('result') != 'Contract source code not verified' else 'No'}")

                    # Check ownership
                    contract = self.w3.eth.contract(address=Web3.to_checksum_address(token_address),
                                                    abi=abi_data.get('result', '[]'))
                    function_names = [item['name'] for item in contract.abi if item['type'] == 'function']

                    if 'owner' in function_names:
                        try:
                            owner = contract.functions.owner().call()
                            if owner.lower() in ["0x0000000000000000000000000000000000000000",
                                                 "0x000000000000000000000000000000000000dEaD"]:
                                print("Ownership: Renounced")
                            else:
                                print(f"Ownership: Active (Owner: {owner})")
                        except:
                            print("Ownership: Could not determine")
                    else:
                        print("Ownership: No owner function found")
            except:
                print("Could not fetch contract analysis")

            print("\n" + "-" * 40)
            print("HOLDER ANALYSIS")
            print("-" * 40)
            try:
                if holders_resp.status_code == 200:
                    holders_data = holders_resp.json()
                    holders = holders_data.get("holders", [])

                    if holders:
                        print(f"Creator wallet: {holders[0].get('share', 0):.1f}% of supply")
                        print(
                            f"Top 10 holders: {sum(holder.get('share', 0) for holder in holders[:10]):.2f}% of supply")

                        # Check for zero and dead addresses
                        zero_holder = next((h for h in holders if
                                            h["address"].lower() == "0x0000000000000000000000000000000000000000"), None)
                        dead_holder = next((h for h in holders if
                                            h["address"].lower() == "0x000000000000000000000000000000000000dead"), None)

                        if zero_holder:
                            print(f"Zero address: {zero_holder.get('share', 0):.1f}% of supply")
                        if dead_holder:
                            print(f"Dead address: {dead_holder.get('share', 0):.1f}% of supply")
            except:
                print("Could not fetch holder analysis")

            print("\n" + "-" * 40)
            print("LIQUIDITY ANALYSIS")
            print("-" * 40)
            try:
                # Get liquidity from Uniswap
                PAIR_ABI = [{
                    "constant": True,
                    "inputs": [],
                    "name": "getReserves",
                    "outputs": [
                        {"name": "_reserve0", "type": "uint112"},
                        {"name": "_reserve1", "type": "uint112"},
                        {"name": "_blockTimestampLast", "type": "uint32"}
                    ],
                    "payable": False,
                    "stateMutability": "view",
                    "type": "function"
                }]

                pair_contract = self.w3.eth.contract(address=Web3.to_checksum_address(self.pair_address), abi=PAIR_ABI)
                reserves = pair_contract.functions.getReserves().call()
                liquidity_eth = self.w3.from_wei(reserves[1], 'ether')
                print(f"Current liquidity: {liquidity_eth:.2f} ETH in Uniswap v2")

                # Check liquidity lock
                if tf_resp.status_code == 200:
                    tf_data = tf_resp.json()
                    locks = tf_data.get('result', [])
                    if locks:
                        total_locked = sum(lock.get('amount', 0) for lock in locks)
                        print(f"Liquidity locked: {total_locked} tokens")
                        for lock in locks:
                            unlock_time = lock.get('unlock_date', 0)
                            unlock_dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unlock_time))
                            print(f"Locked until: {unlock_dt}")
            except Exception as e:
                print(f"Could not fetch liquidity analysis: {e}")

            # print("="*60)

        except Exception as e:
            print(f"Error in token sniffer analysis: {e}")

    def check_honeypot(self):
        """Check if a token is a honeypot using Honeypot.is API."""
        url_hp = f"https://api.honeypot.is/v2/IsHoneypot?address={self.tk_address}"
        if not self.check_honeypot_status:
            pass
        else:
            try:
                response = requests.get(url_hp)
                data = response.json()

                if data.get("isHoneypot"):
                    print("\n---------------------------------------------------------------+")
                    print(f"❗️ Warning: '{self.tk_address}' is a honeypot!")
                    print("\n---------------------------------------------------------------+")

                if data.get("sellTax", 0) > 20:  # High sell tax (>20%) is a red flag
                    print("\n---------------------------------------------------------------+")
                    print(f"❗️ Warning: High sell tax '({data['sellTax']}%)' for '{self.tk_address}'")
                    print("\n---------------------------------------------------------------+")

                # ------------------- generated later -------------------
                if data.get("buyTax", 0) > 20:  # High buy tax (>20%) is a red flag
                    print(f"❗️ Warning: High buy tax ({data['buyTax']}%) for {self.tk_address}")
                    return False
                if data.get("isBlacklisted"):
                    print(f"❗️ Warning: {self.tk_address} is blacklisted!")
                    return False
                if data.get("isScam"):
                    print(f"❗️ Warning: {self.tk_address} is flagged as a scam!")
                    return False
                if data.get("isBot") or data.get("isFake"):
                    print(f"❗️ Warning: {self.tk_address} is flagged as a bot or fake token!")
                    return False
                if data.get("isPhishing"):
                    print(f"❗️ Warning: {self.tk_address} is flagged as a phishing token!")
                    return False
                if data.get("isRugPull"):
                    print(f"❗️ Warning: {self.tk_address} is flagged as a rug pull!")
                    return False
                if data.get("renounceOwnership"):
                    print(f"❗️ Warning: {self.tk_address} is flagged as a Renounce Ownership!")
                    return False
                if data.get("transferOwnership"):
                    print(f"❗️ Warning: {self.tk_address} is flagged as a Transfer ownership!")
                    return False
                # Simulates token pass
                print("\n+------------------------------------------------------------------------------------+")
                print(f"| ❇️ Token: '{self.tk_address}' passed 'honeypot.is' check.  |")
                print("+------------------------------------------------------------------------------------+")

                return True

            except Exception as e:
                print("\n-------------------------------+")
                print(f"Error checking honeypot: {e}")
                print("------------------------------+")
                return False

    def liquidity_lock(self):
        """
        Check if liquidity is locked using Team.Finance and Unicrypt APIs.
        Prints lock status, provider, and lock duration if found.
        Warns if not locked or lock is short.
        """
        pair_address = self.pair_address
        found_lock = False

        # --- Team.Finance ---
        try:
            tf_url = f"https://api.team.finance/v1/token/eth/{pair_address}/locks"
            tf_resp = requests.get(tf_url)

            if tf_resp.status_code == 200:
                tf_data = tf_resp.json()
                locks = tf_data.get('result', []) if isinstance(tf_data, dict) else tf_data

                if locks:
                    for lock in locks:
                        unlock_time = lock.get('unlock_date', 0)
                        amount = lock.get('amount', 0)
                        provider = 'Team.Finance'
                        found_lock = True
                        unlock_dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unlock_time))
                        duration_days = (unlock_time - int(time.time())) // 86400
                        print("\n---------------------------------------------------------------------------------")
                        print(f"Team.Finance:\n"
                              f"Liquidity locked with \n {provider}: {amount} tokens until {unlock_dt} ({duration_days} days left)\n")
                        print("---------------------------------------------------------------------------------")
                        if duration_days < 180:
                            print(f"\n⚠️ Team.Finance:\n"
                                  f"'Lock' duration is short (<6 months)({duration_days} days). Not very safe.\n")
                else:
                    print("\n---------------------------------------------------------------------------------")
                    print("Team.Finance:"
                          "\nNo liquidity 'lock' found on Team.Finance.\n")
                    print("---------------------------------------------------------------------------------")
            else:
                print("\n---------------------------------------------------------------------------------")
                print("Team.Finance:\n"
                      "Could not fetch Team.Finance liquidity 'lock' info.")
                print("---------------------------------------------------------------------------------\n")
        except Exception as e:
            print("\n---------------------------------------------------------------------------------")
            print(f"Team.Finance:\n"
                  f"Error checking Team.Finance: {e}\n")
            print("---------------------------------------------------------------------------------")

        # --- Unicrypt ---
        try:
            uc_url = f"https://api.unicrypt.network/api/v1/lock/uniswapv2/{pair_address}"
            uc_resp = requests.get(uc_url)

            if uc_resp.status_code == 200:
                uc_data = uc_resp.json()
                locks = uc_data.get('locks', []) if isinstance(uc_data, dict) else uc_data

                if locks:
                    for lock in locks:
                        unlock_time = lock.get('unlock_date', 0)
                        amount = lock.get('amount', 0)
                        provider = 'Unicrypt'
                        found_lock = True
                        unlock_dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unlock_time))
                        duration_days_u = (unlock_time - int(time.time())) // 86400
                        print("\n---------------------------------------------------------------------------------")
                        print(f"Unicrypt:\n"
                              f"Liquidity locked with {provider}: {amount} tokens until {unlock_dt} ({duration_days_u} days left)")
                        print("---------------------------------------------------------------------------------")
                        if duration_days_u < 180:
                            print("\n---------------------------------------------------------------------------------")
                            print(f"⚠️ Unicrypt:️\n"
                                  f"Lock duration is short (<6 months)({duration_days_u} days). Not very safe.")
                            print("---------------------------------------------------------------------------------")
                else:
                    print("\n------------------------------------------------------")
                    print("Unicrypt:\n"
                          "No liquidity lock found on Unicrypt.")
                    print("------------------------------------------------------")

            else:
                print("\n------------------------------------------------------")
                print("Unicrypt:\n"
                      "Could not fetch Unicrypt lock info.")
                print("------------------------------------------------------")
        except Exception as e:
            print("\n---------------------------------------------------------------------------------")
            print(f"Unicrypt:\n"
                  f"Error checking Unicrypt:"
                  f"\n{e}")
            print("---------------------------------------------------------------------------------")

        if not found_lock:
            print("\n\n---------------------------------------------------------------------------------")
            print("🚨 Unicrypt:\n"
                  "     Red flag: No liquidity lock found!\n"
                  "     The developer can pull all liquidity and disappear.")
            print("---------------------------------------------------------------------------------")

    def is_contract(self, address):
        pass


if __name__ == "__main__":
    dc = Dex_check()
    dc.get_pair_address()
    dc.get_info()
    dc.get_token_address()
    dc.get_info()

    dc.initialize()
    dc.check_launch_limits()
    dc.top_holders()
    dc.check_lp_holders()
    dc.check_owner_permissions()
    dc.liquidity_lock()
    dc.check_honeypot()
    dc.check_token_sniffer()

    print("\n=================== END TO DEX BOT ===================\n\n")
    # print(dc)



def format_this():
    honeypot_test = True
    print("\nPair address: '0xff98675814d7ffd83383babe29d1d9c9e2bafa0f'")
    time.sleep(1)
    print("initializing with the dex coin...")
    time.sleep(2)

    print("$AURA | 0.0034 ETH | 3 days old | $114.7k Liquidity")
    time.sleep(2)
    print("\n  TOP 10 holders:\n"
          "1. '0xff98675814d7ffd83383babe29d1d9c9e2bafa0f' (4.05%)")
    time.sleep(2)
    print("\nZero address holds (2%) of circulation: $23,344.88")
    print("Dead address holds (45%) of circulation: $84,302.22")
    print("100% of the liquidity is burned")
    print("There's no sign of well-known lock contracts like:\n"
          "Unicrypt, Team.finance, PinkLock, Gnosis etc\n"
          "it suggests the dev retains full control and can pull the liquidity (rug pull) at any time.")
    time.sleep(3)
    if not honeypot_test:
        print("\nNo honey pot detected")
        n = input('Buy coin? (y/n): ')
        if n == 'y':
            time.sleep(2)
            n1 = input("Enter ETH amount: ")
            print("processing...")
            time.sleep(4)
            print("\npurchase complete!\n"
                  "your new wallet balance: ETH 24.43234399")
        else:
            print("\nSelected 'n'. No transaction was made")
    else:
        print("\nHoneypot detected, likely a rug coin")
        y = input("Buy coin anyway? (y/n): ")
        if y == 'y':
            time.sleep(2)
            y1 = input("Enter ETH amount: ")
            print("processing...")
            time.sleep(4)
            print("\npurchase complete!\n"
                  "your new wallet balance: ETH 24.43234399")
        else:
            print("\nSelected 'n'. No transaction was made")
    '''
    1. 🚨 Honeypot Traps
    Definition: You can buy the token, but can’t sell it — or there's a massive fee when you try to sell.
    
    How to Detect:
    
    Use Honeypot checkers (e.g. honeypot.is or DEXTools token sniffer).
    
    Simulate a buy/sell using testnet or small amounts.
    
    Look at sellTax/buyTax in the contract.
    
    Tools like Token Sniffer (https://tokensniffer.com) can show if trading is blocked.
    
    
    2. 🧹 Rug Pulls
    Definition: The dev pulls the liquidity from the pool, crashing the price to near zero.
    
    How to Detect:
    
    Check liquidity lock:
    
    Is liquidity locked in a smart contract (like Unicrypt, Team.finance)? For how long?
    
    If not locked, the dev can pull funds anytime.
    
    Use tools like:
    
    Team.finance
    
    Unicrypt
    
    DEXTools
    
    If liquidity is owned by a wallet (not locked), run away.
    
    
    3. 🔐 Contract Ownership and Permissions
    Is the contract renounced?
    
    If ownership is renounced, no one can change contract rules anymore (safer).
    
    If not renounced, devs can:
    
    Increase taxes.
    
    Blacklist users.
    
    Freeze wallets.
    
    Use:
    
    Etherscan / BscScan → Look at Owner() function and writeContract tab.
    
    Tools like Token Sniffer show this too.
    
    
    4. 💸 Token Tax and Functions
    Many scam tokens hide high buy/sell taxes (up to 99%).
    
    Check:
    
    Is setTax() or similar function available to the owner?
    
    Are there functions like setTradingEnabled(), blacklistAddress()?
    
    You can analyze these in:
    
    Etherscan/BscScan under "Read Contract" and "Write Contract".
    
    
    5. 🧾 Code Audit
    Was the contract audited by a trusted firm (e.g. Certik, Peckshield)?
    
    Is the code open-source?
    
    If it's a fork of a known project, that’s better — but still needs vetting.
    
    
    6. 📊 Community & Volume Red Flags
    Telegram/Discord full of bots or no real discussion?
    
    No whitepaper or roadmap?
    
    Volume < $10,000/day can be risky (low liquidity).
    
    Sudden price spikes with no news? Probably dev manipulation.
    '''

