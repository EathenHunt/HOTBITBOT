import time
from datetime import datetime
from config import *
from strategy import *
from config import API_KEY, API_SECRET, ORDER_SIZE, TAKE_PROFIT_MULTIPLE, STOP_LOSS_PERCENT, DEBUG_MODE


# Define the Hotbit API endpoint and create a HotbitAPI object
api_endpoint = 'https://api.hotbit.io'
hotbit_api = HotbitAPI(api_endpoint)

# Get the available trading pairs from Hotbit
pairs = hotbit_api.get_trading_pairs()

# Print the list of available trading pairs
print("Available trading pairs:")
for pair in pairs:
    print(pair)

# Loop over each trading pair and execute the trading strategy
for pair in pairs:
    try:
        # Get the current balance of the trading pair
        balance = hotbit_api.get_balance(pair)

        # Execute the trading strategy
        execute_strategy(hotbit_api, pair, balance)

    except Exception as e:
        print(f"Error executing strategy for {pair}: {e}")

    # Sleep for the specified interval before executing the next strategy
    time.sleep(INTERVAL)
