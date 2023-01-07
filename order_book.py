import argparse
import requests

def main():
    '''Main driver'''
    parser = argparse.ArgumentParser\
        (description="An Order Book Aggregator for Coinbase, Gemini & Kraken. ")
    parser.add_argument('--quantity', \
        type=float, help='Adjusts quantity of the order. By default the order quantity is 10.')
    args = parser.parse_args()

    if args.quantity is not None:
        print('Custom quantity: ', args.quantity)
        quantity = args.quantity
    else:
        quantity = 10.0

    print(order_book_aggregator(quantity))


def order_book_aggregator(quantity):
    """
    Parameter -> quantity: is the quanity of BTC, by default its 10 but can be custom
    Return -> A two-key dictionary containing the Ask and Bid price for the quantity of BTC across
    the aggregated order books of Gemini, Coinbase, and Kraken.
    """

    asks = []
    bids = []
    
    exhanges = [("Coinbase", "https://api.pro.coinbase.com/products/BTC-USD/book?level=2"),
            ("Kraken", "https://api.kraken.com/0/public/Depth?pair=XBTUSD"),
            ("Gemini", "https://api.gemini.com/v1/book/BTCUSD")]

    for exchange,url in exhanges:
        asks, bids = fetch_order_book(exchange, url)

    asks.sort()
    ask_price = order_calculator(asks, quantity)

    bids.sort(key=lambda x: float(x[0]), reverse = True)
    bid_price = order_calculator(bids, quantity)

    return {"Ask": round(ask_price,2), "Bid": round(bid_price,2)}


def fetch_order_book(exchange: str, url: str):
    """
    Parameter -> exchange: name of exchange to fetch order book from
                url: API url to fetch order book from
    Return -> A List of all ask and bid orders from the specified exchange.
    "asks" and "bids" are nested lists.

    This function fetches the order book from the specified exchange API and separates the
    bids and asks from each other.
    """

    cache_key = (exchange, url)
    if cache_key in cache:
        return cache[cache_key]

    if exchange == "Gemini":
        response = requests.get(url).json()
        bids = response["bids"]
        asks = response["asks"]
        order_book = [orderbook_flattener(asks), orderbook_flattener(bids)]
    else:
        response = requests.get(url).json()
        if exchange == "Coinbase":
            order_book = [response["asks"], response["bids"]]

        else: #exchange == "Kraken"
            order_book = [response["result"]["XXBTZUSD"]["asks"], \
                response["result"]["XXBTZUSD"]["bids"]]

    cache[cache_key] = order_book
    return order_book

def orderbook_flattener(response):
    """
    Parameter -> response: a JSON object of ask or bid order book data
    Return -> A list of orders in the format [price, quantity]

    This function is designed to flatten an order book so all exchanges have the same level.
    """
    orders = []
    for order in response:
        orders.append([order["price"], order["amount"]])
    return orders

def order_calculator(orders: list[list[float, float]], quantity: float):
    """
    Parameter -> orders: a list of ask or bid orders in the format [price, quantity]
                quantity: the number of BTC in the order
    Return -> price: the total price of the order

    This function parses the orders and calculates the total price to buy or sell the
    specified quantity of BTC.
    """
    
    price = 0
    for order in orders:
        if quantity >= float(order[1]):
            price += float(order[0]) * float(order[1])
            quantity -= float(order[1])
        else:
            price += float(order[0]) * quantity
            break
    return price

cache = {}
main()