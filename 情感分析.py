import requests
import json
import pandas as pd
from pprint import pprint
import openpyxl

def analyze_sentiment(text, url, headers):
    """
    调用百度AI情感分析接口进行情感分析
    :param text: 需要分析的文本
    :param url: 百度情感分析API地址
    :param headers: 请求头
    :return: 情感分析结果（正面概率、负面概率等）
    """
    # 将正文内容打包成请求参数
    payload = json.dumps({
        "text": text
    })
    # 发送POST请求
    response = requests.post(url, data=payload, headers=headers)

    # 如果响应成功，返回结果
    if response.status_code == 200:
        return response.json()  # 返回JSON格式结果
    else:
        print(f"请求失败，状态码: {response.status_code}, 原因: {response.text}")
        return None


def main():
    # 百度情感分析API请求地址（需替换为您的 access_token）
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=24.2cdc2694772a3c5df7afd55f3bb0ee26.2592000.1737367894.282335-116757841"

    # 请求头
    headers = {
        'content-type': "application/json",
        "Accept": "application/json"
    }

    # 读取Excel文件，提取“正文内容”列
    input_file = "mediacrawler_weibo_2024-12-21.xlsx"  # Excel文件路径
    df = pd.read_excel(input_file,engine='openpyxl')  # 读取Excel文件
    text_data = df['content']  # 提取“正文内容”列

    # 用于存储分析结果
    results = []

    print("开始进行情感分析...")

    # 遍历每条文本，进行情感分析
    for idx, text in enumerate(text_data):
        print(f"正在分析第 {idx + 1} 条微博内容...")
        result = analyze_sentiment(text, url, headers)  # 调用情感分析函数

        if result:
            sentiment = result.get('items', [{}])[0]  # 获取情感分析结果
            positive_prob = sentiment.get('positive_prob', 0)  # 正面概率
            negative_prob = sentiment.get('negative_prob', 0)  # 负面概率
            sentiment_class = sentiment.get('sentiment', -1)  # 情感分类（0：负面，1：中性，2：正面）

            # 将结果存储到列表中
            results.append({
                "content": text,
                "positive_prob": positive_prob,
                "negative_prob": negative_prob,
                "sentiment_class": sentiment_class  # 0：负面，1：中性，2：正面
            })
        else:
            # 如果接口请求失败，记录为None
            results.append({
                "content": text,
                "positive_prob": None,
                "negative_prob": None,
                "sentiment_class": None
            })

    print("情感分析完成，正在保存结果...")

    # 将分析结果保存到CSV文件
    output_file = "sentiment_results.csv"
    results_df = pd.DataFrame(results)  # 转换为DataFrame
    results_df.to_csv(output_file, index=False, encoding="utf-8-sig")  # 保存为CSV文件

    print(f"情感分析结果已保存到文件：{output_file}")


if __name__ == '__main__':
    main()
