from hotbit import HotbitAPI
from config import API_KEY, API_SECRET, ORDER_SIZE, TAKE_PROFIT_MULTIPLE, STOP_LOSS_PERCENT, DEBUG_MODE

# Instantiate the HOTBIT API object
hotbit = HotbitAPI(API_KEY, API_SECRET, debug=DEBUG_MODE)

def run_strategy(pair):
    # Check if we have any balance for the given pair
    balance = hotbit.get_balance(pair)['available']
    if balance == 0:
        # If not, place a new market buy order for the specified ORDER_SIZE
        order = hotbit.place_market_buy_order(pair, ORDER_SIZE)
        # Calculate the take profit price and place a limit sell order
        tp_price = round(float(order['price']) * TAKE_PROFIT_MULTIPLE, 8)
        hotbit.place_limit_sell_order(pair, ORDER_SIZE, tp_price)
    else:
        # If we already have a position, check the stop loss level
        avg_price = float(hotbit.get_avg_price(pair)['avg_price'])
        stop_loss_price = round(avg_price * (1 + STOP_LOSS_PERCENT/100), 8)
        if hotbit.get_ticker(pair)['last'] < stop_loss_price:
            # If the price drops below the stop loss level, double the position size
            new_size = balance + ORDER_SIZE
            # Cancel the existing limit sell order
            hotbit.cancel_all_orders(pair)
            # Place a new market buy order for the updated size
            order = hotbit.place_market_buy_order(pair, new_size)
            # Calculate the new take profit price and place a limit sell order
            tp_price = round(float(order['price']) * TAKE_PROFIT_MULTIPLE, 8)
            hotbit.place_limit_sell_order(pair, new_size, tp_price)

def run_all_pairs(pairs):
    for pair in pairs:
        run_strategy(pair)

