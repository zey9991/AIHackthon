def calculate_portfolio_weights(analysis_df, coins):
    """
    根据 GPT 分析结果，计算代币的投资权重
    """
    weights = {}
    for coin in coins:
        relevant_analysis = analysis_df[analysis_df['analysis'].str.contains(coin, case=False)]
        positive_count = relevant_analysis['analysis'].str.contains("positive").sum()
        total_count = len(relevant_analysis)
        if total_count > 0:
            weight = (positive_count / total_count) * 100  # 计算正面情绪比例
            weights[coin] = round(weight, 2)
        else:
            weights[coin] = 0
    return weights
