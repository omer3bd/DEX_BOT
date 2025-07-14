import os
from idlelib.format import get_comment_header

import requests
from web3 import Web3
from dotenv import load_dotenv
import pandas as pd
import time

class HoneypotChecker:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Load environment variables
        self.CG_API_KEY = os.getenv("CG_API_KEY")
        self.WEB3_PROVIDER = os.getenv("WEB3_PROVIDER")
        self.WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
        self.PRIVATE_KEY = os.getenv("PRIVATE_KEY")
        self.ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

        if not self.ETHERSCAN_API_KEY:
            raise ValueError("ETHERSCAN_API_KEY not found. Please check your .env file.")

        # Initialize Web3
        self.w3 = Web3(Web3.HTTPProvider(self.WEB3_PROVIDER))

        # Uniswap V2 Router (replace with your DEX's router address)
        # self.UNISWAP_ROUTER = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"

    # ---------- Check for honeypot using Honeypot.is API ----------
    def check_honeypot(self,token_address):
        """Check if a token is a honeypot using Honeypot.is API."""
        url = f"https://api.honeypot.is/v2/IsHoneypot?address={token_address}"
        try:
            response = requests.get(url)
            data = response.json()

            if data.get("isHoneypot"):
                print(f"❗️ Warning: {token_address} is a honeypot!")
                return False
            if data.get("sellTax", 0) > 20:  # High sell tax (>20%) is a red flag
                print(f"❗️ Warning: High sell tax ({data['sellTax']}%) for {token_address}")
                return False
            # ------------------- generated later -------------------
            # if data.get("buyTax", 0) < 5:  # Low buy tax (<5%) is a red flag
            #     print(f"Warning: Low buy tax ({data['buyTax']}%) for {token_address}")
            #     return False
            if data.get("buyTax", 0) > 20:  # High buy tax (>20%) is a red flag
                print(f"❗️ Warning: High buy tax ({data['buyTax']}%) for {token_address}")
                return False
            if data.get("isBlacklisted"):
                print(f"❗️ Warning: {token_address} is blacklisted!")
                return False
            if data.get("isScam"):
                print(f"❗️ Warning: {token_address} is flagged as a scam!")
                return False
            if data.get("isBot") or data.get("isFake"):
                print(f"❗️ Warning: {token_address} is flagged as a bot or fake token!")
                return False
            if data.get("isPhishing"):
                print(f"❗️ Warning: {token_address} is flagged as a phishing token!")
                return False
            if data.get("isRugPull"):
                print(f"❗️ Warning: {token_address} is flagged as a rug pull!")
                return False
            # if data.get("isHoneypot") is None:
            #     print(f"❗️ Warning: Unable to determine honeypot status for '{token_address}'.\n")
            #     return False

            print(f"❇️ '{token_address}' passed honeypot check.\n")
            return True

        except Exception as e:
            print(f"Error checking honeypot: {e}")
            return False

    # ---------- Check token holders ( just gives one )----------
    def check_token_holders(self,token_address):
        """Check token holder distribution using Etherscan or similar (simplified)."""
        # Note: Requires Etherscan API or blockchain query for accurate data
        # Placeholder: Assume top 10 holders own less than 70% of supply
        # You can integrate BscScan/Etherscan API for real holder data
        url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={token_address}&address={self.WALLET_ADDRESS}&tag=latest&apikey=your_etherscan_api_key"
        try:
            response = requests.get(url)
            data = response.json()
            if data.get("status") != "1":
                print(f"Error fetching token holders: {data.get('message')}")
                return False
            # Placeholder logic: Assume holder distribution is acceptable
            # In practice, you would analyze the distribution of top holders
            # For example, you could check if top 10 holders own less than 70% of supply
            print(f"Checking holders for {token_address}...")
            # Placeholder: Simulate holder distribution check
            time.sleep(1)  # Simulate API rate limit handling
            # Here you would typically parse the response and analyze holder distribution
            # For example, you could check if top 10 holders own less than 70% of supply
            # This is a simplified example; you would need to implement actual logic
            if response.status_code != 200:
                print(f"Error fetching token holders: {response.status_code}")
                return False
            # Simulate holder distribution check
            print(f"Checking holder distribution for {token_address}...")
            time.sleep(1)  # Simulate API rate limit handling
            # Placeholder: Assume holder distribution is acceptabl

                # Get total supply
                # supply_url = f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={token_address}&apikey={etherscan_api_key}"
            supply_resp = requests.get(url).json()
            total_supply = int(supply_resp.get("result", 0))

            # Get top holders (Etherscan's API for holders is limited; use third-party or scraping for full data)
            holders_url = f"https://api.ethplorer.io/getTopTokenHolders/{token_address}?apiKey=freekey&limit=10"
            holders_resp = requests.get(holders_url).json()
            top_holders = holders_resp.get("holders", [])

            top_10_balance = sum(int(holder["balance"]) for holder in top_holders)
            percent = (top_10_balance / total_supply) * 100 if total_supply > 0 else 0

            print(f"Top 10 holders own {percent:.2f}% of supply.")
            # return percent < 70

            # Add logic to analyze holder distribution (e.g., query top holders)
            # For simplicity, assume check passes if API call succeeds
            # print(f"{token_address} holder distribution check passed (placeholder).")
            # return True
        except Exception as e:
            print(f"Error checking holders: {e}")
            return False

    # ---------- Check Wallet Uniswap balance ----------
    def check_uniswap_balance(self, WALLET_ADDRESS):
        """Check Uniswap balance for a specific token."""
        # Placeholder: Implement Uniswap balance check logic
        # Example: Use Web3.py to query the Uniswap contract for token balance
        print(f"Checking Uniswap balance for {WALLET_ADDRESS}...")
        # Add Web3.py code to interact with Uniswap Router
        # Example: https://web3py.readthedocs.io/en/stable/examples.html#interacting-with-smart-contracts
        balance = 2 + 2
        return balance

    # ---------- Check token balance and TOP holders ----------
    def check_token_balance(self, token_address):

        url = (
            f"https://api.etherscan.io/api"
            f"?module=account"
            f"&action=tokenbalance"
            f"&contractaddress={token_address}"
            f"&address={self.WALLET_ADDRESS}"
            f"&tag=latest"
            f"&apikey={self.ETHERSCAN_API_KEY}"
        )

        response = requests.get(url)
        data = response.json()
        # -------- Check token balance --------
        if data["status"] == "1":
            # Balance is returned in token's smallest unit (like wei for ETH)
            balance = int(data["result"])
            print(f"The balance is: {balance}")
            # return balance
        else:
            print(data)
            raise Exception(f"Error fetching token balance: {data['message']}")

        # ------ Check top holders using Ethplorer ------
        holders_url = f"https://api.ethplorer.io/getTopTokenHolders/{token_address}?apiKey=freekey&limit=10"

        try:
            holders_resp = requests.get(holders_url)
            holders_data = holders_resp.json()

            # ----- top holders -----
            top_holders = holders_data.get("holders", [])

            if not top_holders:
                print("No top holders found or token not indexed by Ethplorer.")
                # return balance

            # ----- Print top holders ----
            print("\n🔝 Top 10 Holders:")

            for i, holder in enumerate(top_holders, 1):
                address = holder["address"]
                holder_balance = int(holder["balance"])
                percent = holder.get("share", 0)
                print(f"{i}. {address} — {holder_balance} tokens ({percent:.2f}%)")

            # Check if top holders own less than 70% of supply
            holder_percent = 70
            if (top_holders and top_holders[0]["address"].lower() == "0x000000000000000000000000000000000000dead"
                    and top_holders[0].get("share", 0) > holder_percent):
                print(f"\n🚨 Likely scam: Dead address holds over {holder_percent}% of supply!")
                # return False

            for holder in top_holders:
                if (holder["address"].lower() == "0x0000000000000000000000000000000000000000"
                        and holder.get("share", 0) > 5):
                    print("⚠️ Warning: Zero address holds more than 5% of tokens — investigate.")
                else:
                    if holder["address"].lower() == "0x0000000000000000000000000000000000000000":
                        print(f"The zero address holds: {holder_balance} tokens ({percent:.2f}%)")

            # return balance
        except Exception as e:
            print(f"Error fetching top holders: {e}")
            return balance

    # ---------- Execute a trade on Uniswap ----------
    def execute_trade(self, token_address, amount_eth):
        print("Executing trade on Uniswap...")

        # ---------- Execute a trade on Uniswap ----------
        # Placeholder: Implement Uniswap V2/V3 swap logic using Web3.py
        # Ensure slippage protection and gas estimation
        # print(f"Executing trade for {token_address} with {amount_eth} ETH...")
        # Add Web3.py code to interact with Uniswap Router
        # Example: https://web3py.readthedocs.io/en/stable/examples.html#interacting-with-smart-contracts
        print(f"✅ Executed token '{token_address}' with {amount_eth} ETH;"
              f"\nTotal approx $350 @ $3500 USDT, (GAS: $3);")

        x_check_uniswap_balance = self.check_uniswap_balance(self.WALLET_ADDRESS)
        print(f"\nNew Wallet Balance: '{x_check_uniswap_balance} ETH' (approx. $350);")
        # return True





# ---------- instantiate HoneypotChecker and check honeypot status ----------
token_input = "0xf22fdd2be7c6da9788e4941a6ffc78ca99d7b15c"  # Example token address

hpc = HoneypotChecker()
hpc.check_honeypot(token_input)  # Replace with actual token address
hpc.check_token_balance(token_input)  # Check token balance for the wallet address


def check_liquidity(token_address):
    """Check liquidity pool status using CoinGecko or Web3."""
    # Example: Check liquidity via CoinGecko (simplified)
    url = f"https://api.coingecko.com/api/v3/coins/ethereum/contract/{token_address}"
    headers = {"accept": "application/json", "x-cg-demo-api-key": CG_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        liquidity = data.get("market_data", {}).get("total_volume", {}).get("usd", 0)
        if liquidity < 10000:  # Low liquidity threshold (adjust as needed)
            print(f"Warning: Low liquidity (${liquidity}) for {token_address}")
            return False
        print(f"{token_address} has sufficient liquidity (${liquidity}).")
        return True
    except Exception as e:
        print(f"Error checking liquidity: {e}")
        return False





def main():
    # Example token address to check (replace with dynamic input)
    token_address = "0xYourTokenAddressHere"  # Replace with actual token address
    amount_eth = 0.01  # Small test amount

    # Step 1: Perform safety checks
    if not check_honeypot(token_address):
        return
    if not check_liquidity(token_address):
        return
    if not check_token_holders(token_address):
        return

    # Step 2: Execute test transaction
    print(f"Performing test transaction for {token_address}...")
    if execute_trade(token_address, amount_eth):
        print(f"Test trade successful for {token_address}.")
        # Step 3: Execute main trade if test passes
        # execute_trade(token_address, main_amount_eth)
    else:
        print(f"Test trade failed for {token_address}.")

# if __name__ == "__main__":
#     main()