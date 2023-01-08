import argparse
import heapq
import requests

def main():
    '''Main driver'''
    parser = argparse.ArgumentParser\
        (description="An Order Book Aggregator for Coinbase, Gemini & Kraken. ")
    parser.add_argument('--quantity', \
        type=float, help='Adjusts quantity of the order. By default the order quantity is 10.')
    args = parser.parse_args()

    if args.quantity is not None:
        quantity = args.quantity
    else:
        quantity = 10.0

    print(order_book_aggregator(quantity))


def order_book_aggregator(quantity: float):
    """
    Parameters
    ----------
    Quanity: quantity of BTC that is being purchased/sold.
    
    Combines all of the orderbooks into a heap. And displays the ask/bid price.
    """

    asks = []
    bids = []
    
    exhanges = [("Coinbase", "https://api.pro.coinbase.com/products/BTC-USD/book?level=2"),
            ("Kraken", "https://api.kraken.com/0/public/Depth?pair=XBTUSD"),
            ("Gemini", "https://api.gemini.com/v1/book/BTCUSD")]

    for exchange,url in exhanges:
        asks, bids = fetch_order_book(exchange, url)

    heapq.heapify(asks)

    ask_price = order_calculator(asks, quantity)

    heapq.heapify(bids)
    bids = bids[::-1]

    bid_price = order_calculator(bids, quantity)

    return {"Ask": round(ask_price,2), "Bid": round(bid_price,2)}


def fetch_order_book(exchange: str, url: str):
    """
    Parameters
    ----------
    
    exchange: name of the exchange to get the orderbook from

    url: the API link that corresponds to an orderbook

    This function gets the order book from the specified exchange API and separates the
    bids and asks from each other. While returning a nested list of all bids and asks
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

        else:
            order_book = [response["result"]["XXBTZUSD"]["asks"], \
                response["result"]["XXBTZUSD"]["bids"]]

    cache[cache_key] = order_book
    return order_book

def orderbook_flattener(response):
    """
    Parameters
    ----------
    response: A JSON object of ask or bid order book data

    Returns a list of orders [price, amount]

    This function is designed to flatten an order book so all exchanges have the same level.
    """
    orders = []
    for order in response:
        orders.append([order["price"], order["amount"]])
    return orders

def order_calculator(orders: list[list[float, float]], quantity: float):
    """
    Parameters
    ----------
    orders: A nested list of floats that contains ask or bid orders in the format [price, quantity]

    quantity: The number of BTC in the order

    This function parses the orders and calculates the total price to buy or sell the
    specified quantity of BTC. And returns the price.
    """
    
    price = 0
    for order in orders:
        if quantity >= float(order[1]):
            price += float(order[0]) * float(order[1])
            quantity -= float(order[1])
            if quantity == 0:
                break
        else:
            price += float(order[0]) * quantity
            break
    return price

cache = {}
main()