import datetime
import time
import pandas as pd
import requests
import random
from tqdm import tqdm
import os
from datetime import datetime


BASE_URL = "https://api.binance.com/api/v3/"

def interval_to_seconds(interval):
    number = int(''.join(filter(str.isdigit, interval)))
    if 'm' in interval:
        return number * 60
    elif 'h' in interval:
        return number * 60 * 60
    elif 'd' in interval:
        return number * 60 * 60 * 24

def get_klines(
        symbol: str,
        interval: str,
        start_time: str,
        end_time: str,
        limit: int = 1000,
        clean: bool = True
) -> pd.DataFrame:

    all_data = []

    start_timestamp = int(time.mktime(datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").timetuple())) * 1000
    end_timestamp = int(time.mktime(datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").timetuple())) * 1000

    temp_timestamp = start_timestamp
    interval_seconds = interval_to_seconds(interval)

    total_intervals = (end_timestamp - start_timestamp) / (interval_seconds * 1000)

    with requests.Session() as s, tqdm(total=total_intervals, desc="Downloading") as pbar:
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
            all_data.extend(data)
            if len(data) < limit:
                break
            temp_timestamp = data[-1][0] + interval_seconds * 1000  
            
            pbar.update(len(data))

            time.sleep(random.uniform(0.1, 0.2))  # 随机时间间隔，防止被ban
    print('====完成数据获取====')
    if clean:
        df = pd.DataFrame(all_data, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                             'quote_asset_volume', 'number_of_trades', 'taker_buy_base',
                                             'taker_buy_quote', 'ignored'])
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)
        df.drop(columns=['ignored'], inplace=True)
        
        return df
    else:
        
        return all_data
def filename_friendly_date(date_str: str) -> str:
    """Convert a date string into a filename-friendly format."""
    return date_str.replace(':', '-').replace(' ', '_')

def getsave_data(symbol: str, start_time: str, end_time: str, interval: str) -> pd.DataFrame:
    """获取存储
    
    example input:
    symbol = 'BTCUSDT'
    start_time = '2020-01-01 00:00:00'
    end_time = '2020-01-02 00:00:00'
    interval = '1m'
    """
    friendly_start_time = filename_friendly_date(start_time)
    friendly_end_time = filename_friendly_date(end_time)
    
    filename = f'{symbol}_{friendly_start_time}_{friendly_end_time}_{interval}.csv'
    filepath = os.path.join('data', filename)

    try:
        data = pd.read_csv(filepath)
        pass
    except FileNotFoundError:
        data = get_klines(symbol=symbol, start_time=start_time, end_time=end_time, interval=interval)
        print(f'{symbol}_{friendly_start_time}_{friendly_end_time}_{interval}下载成功啦')
        data.to_csv(filepath, index=False)
    
    

def get_data(symbol: str, start_time: str, end_time: str, interval: str):
        symbol = symbol
        start_time = start_time
        end_time = end_time
        interval = interval
        getsave_data(symbol=symbol, start_time=start_time, end_time=end_time, interval=interval)   

def get_data_list(symbol_list: list, start_time: str, end_time: str, interval: str):       
    for symbol in symbol_list:
        get_data(symbol=symbol, start_time=start_time, end_time=end_time, interval=interval)
        print(f'{symbol}下载完成')
        

symbol_list = ['DOGEUSDT','ETHUSDT']        
get_data_list(symbol_list=symbol_list, start_time='2017-01-01 00:00:00', 
              end_time='2024-6-15 00:00:00', 
              interval='1d')