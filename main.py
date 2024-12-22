from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time
import pandas as pd

# 设置 Selenium 的 EdgeOptions，避免打开浏览器界面
edge_options = Options()
edge_options.add_argument('--headless')  # 无头模式
edge_options.add_argument('--disable-gpu')  # 禁用 GPU 加速

# 创建 WebDriver 实例，使用 Edge WebDriver
driver_path = "D:/edgedriver_win64/edgedriver_win64/msedgedriver.exe"  # 请替换为您的 Edge WebDriver 路径
service = Service(driver_path)
driver = webdriver.Edge(service=service, options=edge_options)

# 初始化数据存储列表
topic_titles = []
discussion_counts = []
view_counts = []

# 循环遍历页面
for page in range(1, 21):
    # 构造 URL
    url = f"https://s.weibo.com/topic?q=%E6%AD%A6%E6%B1%89%E5%A4%A7%E5%AD%A6&pagetype=topic&topic=1&Refer=weibo_topic&page={page}"
    driver.get(url)

    # 等待页面加载
    time.sleep(5)

    # 模拟滚动页面，加载更多内容
    for _ in range(3):  # 向下滚动三次
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 等待2秒加载新内容

    # 查找话题卡片列表
    cards = driver.find_elements(By.XPATH, "//div[@class='card card-direct-a card-direct-topic']")

    # 遍历每个话题卡片，提取数据
    for card in cards:
        try:
            # 提取话题标题
            title = card.find_element(By.CLASS_NAME, "name").text

            # 提取第二个 <p> 标签，包含讨论数和阅读量
            p_tags = card.find_elements(By.TAG_NAME, "p")
            if len(p_tags) >= 2:
                stats = p_tags[1].text.strip()  # 第二个 <p> 标签内容
                discussion, views = stats.split(" ")  # 根据空格分隔数据
            else:
                discussion, views = "无数据", "无数据"

            # 存储数据
            topic_titles.append(title)
            discussion_counts.append(discussion)
            view_counts.append(views)

        except Exception as e:
            print("提取数据时出错：", e)

# 存储数据到 DataFrame
data = {
    "话题标题": topic_titles,
    "讨论数": discussion_counts,
    "阅读量": view_counts
}
df = pd.DataFrame(data)

# 打印结果
print(df)

# 保存为 CSV 文件
df.to_csv("wuhan_university_weibo_topic_data.csv", index=False, encoding='utf-8-sig')

# 关闭浏览器
driver.quit()
