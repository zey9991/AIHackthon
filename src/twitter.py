import tweepy

import pandas as pd
import requests

# 替换为你的 Twitter API 凭据
API_KEY = ""
API_SECRET = ""
BEARER_TOKEN = ""

# 初始化 Twitter API 客户端
client = tweepy.Client(bearer_token=BEARER_TOKEN)


def fetch_tweets(hashtag, max_results=10):
    """
    搜索指定 hashtag 的推文
    :param hashtag: 要搜索的 hashtag（如 #Python）
    :param max_results: 返回的最大推文数量（Twitter API 每次最多 100 条）
    """
    query = f"#{hashtag} -is:retweet lang:en"  # 只获取英文推文
    tweets = client.search_recent_tweets(query=query, tweet_fields=["id", "text", "author_id", "created_at"],
                                         max_results=max_results)
    data = []
    if tweets.data:
        for tweet in tweets.data:
            data.append({
                "id": tweet.id,
                "author_id": tweet.author_id,
                "text": tweet.text,
                "created_at": tweet.created_at
            })
    return pd.DataFrame(data)

# 示例调用
if __name__ == "__main__":
    hashtag_to_search = "Python"  # 替换为你的 hashtag
    fetch_tweets(hashtag_to_search, max_results=10)
