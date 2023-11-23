import requests
import os
from dotenv import load_dotenv

# Load environment variables from secret.env file
load_dotenv(dotenv_path='secret.env')

# User inputs their crypto address
def get_user_address():
    while True:
        user_address = input("Please enter your crypto address: ")
        url = f"https://api.opensea.io/api/v2/accounts/{user_address}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return user_address
        else:
            print("Invalid address. Please try again.")

# Calculate total value of the given address
def get_total_liquidity(user_address):
    url = f"https://api.opensea.io/api/v2/chain/ethereum/account/{user_address}/nfts?limit=200"
    response = requests.get(url, headers=headers)
    data = response.json()

    total_liquidity = 0.0
    
    for nft in data['nfts']:
        collection_url = f"https://api.opensea.io/api/v2/collections/{nft['collection']}/stats"
        collection_response = requests.get(collection_url, headers=headers)
        collection_stats = collection_response.json()
        total_liquidity += collection_stats["total"]["floor_price"]

    return round(total_liquidity, 2)

def main():
    user_address = get_user_address()
    total_liquidity = get_total_liquidity(user_address)

    url = f"https://api.opensea.io/api/v2/accounts/{user_address}"
    response = requests.get(url, headers=headers)
    data = response.json()

    if data["username"] == "":
        print(f"Unnamed wallet's total liquidity is worth {total_liquidity} ETH")
    else:
        print(f"{data['username']}'s total liquidity is worth {total_liquidity} ETH")

if __name__ == "__main__":
    # Access the API key
    headers = {
        "accept": "application/json",
        "x-api-key": os.environ.get("OPENSEA_API_KEY")
    }
    main()

