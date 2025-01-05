import openai
import pandas as pd

openai.api_base = ""
openai.api_key = ""

def analyze_tweets_with_chatgpt(tweets_df, keyword):
    """
    使用 OpenAI GPT API 分析推文情绪，并判断代币市场趋势
    """
    prompt_template = """
    You are a financial analyst specializing in cryptocurrency markets. Analyze the following tweets for their sentiment (positive, neutral, or negative) 
    and indicate whether they are likely to suggest a price increase or decrease for the memecoin '{keyword}'.
    Provide a recommendation on how this sentiment affects the portfolio weight for this coin (0-100%).

    Tweets:
    {tweets}

    Return the analysis in the following format for each tweet:
    1. Sentiment (positive/neutral/negative)
    2. Price trend prediction (increase/decrease)
    3. Suggested weight adjustment (percentage).
    """
    results = []
    for index, row in tweets_df.iterrows():
        prompt = prompt_template.format(keyword=keyword, tweets=row['text'])
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an expert cryptocurrency analyst."},
                      {"role": "user", "content": prompt}]
        )
        analysis = response['choices'][0]['message']['content']
        results.append({
            "tweet_id": row['id'],
            "author_id": row['author_id'],
            "text": row['text'],
            "analysis": analysis
        })
    return pd.DataFrame(results)

def agent_wo_crypto(tweets_df, tokens):
    """
    使用 OpenAI GPT API 分析所有推文，直接输出代币的整体权重分配
    :param tweets_df: 包含推文的 DataFrame
    :param tokens: 需要评估的代币列表（如 ['Shiba Inu', 'Dogecoin']）
    """
    # 合并所有推文文本
    combined_tweets = "\n\n".join(tweets_df["text"].tolist())

    # Prompt 模板，输入所有推文，要求 GPT 给出最终权重分配
    prompt = f"""
    You are a financial analyst specializing in cryptocurrency investments. 
    Analyze the following tweets and determine the overall portfolio weight allocation (in percentages) for the tokens: {', '.join(tokens)}.

    Tweets:
    {combined_tweets}

    Return the portfolio weight for each token in the following format:
    Token 1: xx%
    Token 2: xx%
    ...

    The sum of weights across all tokens should be 100%.
    """

    # 调用 GPT 进行分析
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert cryptocurrency analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    # 提取 GPT 的回复内容
    analysis = response["choices"][0]["message"]["content"]
    return analysis

def agent_with_crypto(price_data, tweets, tokens):
    """
    调用 OpenAI GPT 进行分析，结合价格数据和推文，预测代币权重
    """
    prompt = f"""
    You are a cryptocurrency investment analyst. Based on the historical price data and recent tweets provided below, determine the portfolio weight allocation (in percentages) for the tokens: {', '.join(tokens)}.

    Historical price data:
    {price_data}

    Relevant tweets:
    {tweets}

    Return the portfolio weight for each token in the following format:
    Token 1: xx%
    Token 2: xx%
    ...

    The sum of weights across all tokens should be 100%.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert cryptocurrency analyst."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']