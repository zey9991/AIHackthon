import openai
import pandas as pd
import requests
import time
from datetime import datetime, timedelta
from tqdm import tqdm
import random
import os

# Binance API 的基础 URL
BASE_URL = "https://api.binance.com/api/v3/"

# 数据存储目录
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def interval_to_seconds(interval):
    """
    将 Binance 的时间间隔转为秒
    """
    number = int(''.join(filter(str.isdigit, interval)))
    if 'm' in interval:
        return number * 60
    elif 'h' in interval:
        return number * 60 * 60
    elif 'd' in interval:
        return number * 60 * 60 * 24

def get_klines(symbol, interval, start_time, end_time, limit=1000):
    """
    从 Binance API 获取 K线数据
    """
    start_timestamp = int(time.mktime(datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").timetuple())) * 1000
    end_timestamp = int(time.mktime(datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").timetuple())) * 1000

    all_data = []
    temp_timestamp = start_timestamp
    interval_seconds = interval_to_seconds(interval)

    with requests.Session() as s, tqdm(desc=f"Downloading {symbol}", total=(end_timestamp - start_timestamp) // (interval_seconds * 1000)) as pbar:
        while temp_timestamp < end_timestamp:
            params = {
                'symbol': symbol,
                'interval': interval,
                'startTime': temp_timestamp,
                'endTime': end_timestamp,
                'limit': limit
            }
            response = s.get(f"{BASE_URL}klines", params=params)
            data = response.json()

            if not data:
                break

            all_data.extend(data)
            if len(data) < limit:
                break

            temp_timestamp = data[-1][0] + interval_seconds * 1000
            pbar.update(len(data))
            time.sleep(random.uniform(0.1, 0.2))  # 随机时间间隔，防止被限制

    df = pd.DataFrame(all_data, columns=[
        'open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
        'quote_asset_volume', 'number_of_trades', 'taker_buy_base', 'taker_buy_quote', 'ignored'
    ])
    df = df[['open_time', 'open', 'high', 'low', 'close', 'volume']]
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    return df

def format_price_data(df):
    """
    格式化价格数据为字符串，适合输入到 GPT
    """
    price_lines = []
    for _, row in df.iterrows():
        date = datetime.fromtimestamp(row['open_time'] / 1000).strftime('%Y-%m-%d')
        price_lines.append(f"Date: {date} | Open: {row['open']:.4f} | High: {row['high']:.4f} | Low: {row['low']:.4f} | Close: {row['close']:.4f} | Volume: {row['volume']:.2f}")
    return "\n".join(price_lines)