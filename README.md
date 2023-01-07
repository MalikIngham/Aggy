# OrderBookAggregator

An Order Book Aggregator for Coinbase, Gemini, and Kraken.

Getting Started

To use this script, you will need to have Python 3 installed on your machine.

Running the script

The script can be run using the following command:

python3 order_book.py

By default, the script will return the ask and bid prices for 10 BTC. You can specify a custom quantity using the --quantity flag:

python3 order_book.py --quantity <quantity>

For example:

python3 order_book.py --quantity 32.1

This fetches the ask and bid prices for 32.1 BTC.

Functionality

This script aggregates the order books from Coinbase, Gemini, and Kraken and returns the ask and bid prices for a specified quantity of BTC. The ask price is the minimum price at which you can buy the specified quantity of BTC and the bid price is the maximum price at which you can sell the specified quantity of BTC.

The script first fetches the order books from the three exchanges and separates the ask and bid orders. It then sorts the orders by price and calculates the total price for the specified quantity of BTC using the order_calculator function. The ask and bid prices are returned in a dictionary with the keys "Ask" and "Bid".

The script also implements a cache to store the fetched order books so that subsequent requests for the same exchange and URL do not need to make an API call. This helps to improve the performance of the script.