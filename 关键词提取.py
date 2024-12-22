# -*- encoding:utf-8 -*-
from __future__ import print_function

import pandas as pd
from textrank4zh import TextRank4Keyword
import codecs

def load_stopwords(stopword_file):
    """
    加载停用词表
    :param stopword_file: 停用词文件路径
    :return: 停用词集合
    """
    stopwords = set()
    with codecs.open(stopword_file, 'r', 'utf-8') as f:
        for line in f.readlines():
            stopwords.add(line.strip())  # 移除每行的换行符
    return stopwords

def extract_keywords_from_text(text, top_k=20, stopwords=None):
    """
    使用 TextRank 提取关键词，并去除停用词
    :param text: 输入的文本
    :param top_k: 提取的关键词数量
    :param stopwords: 停用词集合
    :return: 提取的关键词列表 [(word, weight), ...]
    """
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=2)

    # 获取关键词及其权重，并去除停用词
    keywords = []
    for item in tr4w.get_keywords(top_k, word_min_len=1):
        word = item.word
        weight = item.weight
        if stopwords and word not in stopwords:  # 如果不在停用词表中，才加入
            keywords.append((word, weight))

    return keywords

def main():
    # 输入文件路径
    input_file = "mediacrawler_weibo_2024-12-21.xlsx"
    output_file = "keywords_extraction_results.csv"
    stopword_file = "百度停用词表.txt"  # 停用词表文件路径

    # 加载停用词表
    stopwords = load_stopwords(stopword_file)

    # 读取 Excel 文件
    df = pd.read_excel(input_file, engine='openpyxl')
    text_data = df['content']

    # 用于存储提取结果
    results = []

    print("开始进行关键词提取...")

    for idx, text in enumerate(text_data):
        if pd.isna(text) or not text.strip():
            print(f"第 {idx + 1} 条微博内容为空，跳过...")
            continue

        print(f"正在提取第 {idx + 1} 条微博内容的关键词...")

        # 提取关键词
        try:
            keywords = extract_keywords_from_text(text, stopwords=stopwords)
            for word, weight in keywords:
                results.append({
                    "content": text,
                    "keyword": word,
                    "weight": weight
                })
        except Exception as e:
            print(f"提取第 {idx + 1} 条微博内容时出错：{e}")
            results.append({
                "content": text,
                "keyword": None,
                "weight": None
            })

    print("关键词提取完成，正在保存结果到 CSV 文件...")

    # 将提取结果保存到 CSV 文件
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"关键词提取结果已成功保存到文件：{output_file}")


if __name__ == "__main__":
    main()
