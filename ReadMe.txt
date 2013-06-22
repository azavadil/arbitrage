The attached program pulls real-time currency exchange rates from Yahoo finance and finds arbitrage cycles. Please note that the program is not intended for use in actual trading (the program ignores both the bid/ask spread and trading costs).

The program uses the queue based Bellman-Ford algorithm to detect negative cycles. Fx rates are converted to logs to enable addition. 

