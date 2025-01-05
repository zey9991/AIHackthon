import pandas as pd

from gpt_agent import analyze_tweets_with_chatgpt, agent_wo_crypto, agent_with_crypto
from price_getter import get_klines, format_price_data
from twitter import fetch_tweets
from utils import calculate_portfolio_weights

if __name__ == "__main__":
    # 输入代币关键词
    hashtags = ["SHIB", "DOGE", "PEPE", "BONK", "PENGU", "WIF", "FLOKI"]
    tokens = ["SHIBUSDT", "DOGEUSDT", "PEPEUSDT", "BONKUSDT", "PENGUUSDT", "WIFUSDT", "FLOKIUSDT"]

    symbol_list = ["SHIBUSDT", "DOGEUSDT", "PEPEUSDT", "BONKUSDT", "PENGUUSDT", "WIFUSDT", "FLOKIUSDT"]

    start_time = '2024-12-28 00:00:00'
    end_time = '2025-01-04 00:00:00'
    interval = '1d'

    all_price_data = []
    for symbol in symbol_list:
        print(f"Fetching data for {symbol}...")
        df = get_klines(symbol, interval, start_time, end_time)
        price_data = format_price_data(df)
        all_price_data.append(f"Price data for {symbol}:\n{price_data}")

    # 爬取推文
    all_tweets = []
    for hashtag in hashtags:
        tweets_df = fetch_tweets(hashtag, max_results=10)
        all_tweets.append(tweets_df)
    all_tweets_df = pd.concat(all_tweets, ignore_index=True)

    # GPT 分析所有推文并生成整体权重预测
    overall_analysis = agent_wo_crypto(all_tweets_df, tokens)
    print("整体投资组合权重预测：")
    print(overall_analysis)
