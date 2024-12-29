from flask import Flask, request, jsonify
import pandas as pd
import talib

app = Flask(__name__)

@app.route("/place_trade", methods=["POST"])
def place_trade():
    try:
        # Parse input parameters
        data = request.get_json()
        mt5_login = data.get("mt5_login")
        mt5_password = data.get("mt5_password")
        mt5_server = data.get("mt5_server")
        license_key = data["license_key"]
        symbol = data["symbol"]
        timeframe = data["timeframe"]
        take_profit = data["take_profit"]
        stop_loss = data["stop_loss"]

        # Validate MT5/MT4 login details
        if not (mt5_login and mt5_password and mt5_server):
            return jsonify({"error": "MT5/MT4 login details are missing"}), 400

        # Example price data (replace this with live data from an API)
        prices = {
            "open": [100, 102, 104, 103, 105],
            "high": [102, 105, 106, 104, 107],
            "low": [99, 100, 101, 102, 104],
            "close": [101, 104, 103, 105, 106]
        }
        df = pd.DataFrame(prices)

        # Calculate indicators
        # 1st Strategy Indicators
        df["RSI"] = talib.RSI(df["close"], timeperiod=14)
        df["Upper_Band"], df["Middle_Band"], df["Lower_Band"] = talib.BBANDS(df["close"], timeperiod=20)
        df["Fast_MA"] = talib.SMA(df["close"], timeperiod=10)
        df["Slow_MA"] = talib.SMA(df["close"], timeperiod=50)

        # 2nd Strategy Indicators
        df["MACD"], df["MACD_Signal"], _ = talib.MACD(df["close"], fastperiod=12, slowperiod=26, signalperiod=9)
        df["Parabolic_SAR"] = talib.SAR(df["high"], df["low"], acceleration=0.02, maximum=0.2)
        df["Williams_R"] = talib.WILLR(df["high"], df["low"], df["close"], timeperiod=14)

        # 3rd Strategy Indicators
        df["BB_Upper"], df["BB_Middle"], df["BB_Lower"] = talib.BBANDS(df["close"], timeperiod=20)
        df["Fast_MA_3"] = talib.SMA(df["close"], timeperiod=10)
        df["Slow_MA_3"] = talib.SMA(df["close"], timeperiod=50)

        # Trading logic
        latest = df.iloc[-1]

        # Example trading logic (combine multiple strategies)
        if latest["RSI"] < 30 and latest["close"] > latest["Lower_Band"] and latest["Fast_MA"] > latest["Slow_MA"]:
            action = "Buy"
        elif latest["RSI"] > 70 and latest["close"] < latest["Upper_Band"] and latest["Fast_MA"] < latest["Slow_MA"]:
            action = "Sell"
        elif latest["MACD"] > latest["MACD_Signal"] and latest["Williams_R"] < -80:
            action = "Buy"
        elif latest["MACD"] < latest["MACD_Signal"] and latest["Williams_R"] > -20:
            action = "Sell"
        else:
            action = "Hold"

        # Simulate trade placement logic (can be extended to connect to MT5/MT4 terminal)
        trade_response = {
            "action": action,
            "symbol": symbol,
            "timeframe": timeframe,
            "take_profit": take_profit,
            "stop_loss": stop_loss
        }

        return jsonify({
            "message": "Trade decision made successfully.",
            "trade": trade_response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
