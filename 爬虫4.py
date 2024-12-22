from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import csv
import time

# Edge WebDriver 路径
edge_driver_path = r"D:\edgedriver_win64\edgedriver_win64\msedgedriver.exe"  # 请根据你下载的 WebDriver 路径调整

# 设置Selenium的Edge浏览器选项
edge_options = Options()
edge_options.add_argument("--headless")  # 无头模式
edge_options.add_argument("--disable-gpu")  # 禁用GPU加速
edge_options.add_argument("--no-sandbox")  # 解决一些环境问题
edge_options.add_argument('--disable-extensions')  # 禁用扩展

# 启动Edge浏览器
driver = webdriver.Edge(service=Service(edge_driver_path), options=edge_options)

# 基础 URL
base_url = "https://s.weibo.com/weibo?q=%E6%AD%A6%E6%B1%89%E5%A4%A7%E5%AD%A6&Refer=weibo_weibo&page={}"

# 存储所有页面数据的列表
all_user_names = []
all_post_times = []
all_contents = []
all_reposts = []
all_comments = []
all_likes = []

# 遍历1到50页
for page in range(1, 51):
    url = base_url.format(page)
    try:
        driver.get(url)  # 使用Selenium加载页面
        time.sleep(3)  # 等待页面加载完成，时间可根据网络状况调整

        # 获取页面内容
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 查找微博卡片
        cards = soup.find_all('div', class_='card-wrap')

        user_names = []
        post_times = []
        contents = []
        reposts = []
        comments = []
        likes = []

        for card in cards:
            try:
                # 提取用户名
                user_name = card.find('div', class_='info').find('a', class_='name').text
                # 提取发帖时间
                post_time = card.find('div', class_='from').find('a').text
                # 提取正文内容
                content = card.find('div', class_='content').find('p', class_='txt').text
                # 提取转发数、评论数、点赞数
                action_buttons = card.find('div', class_='card-act').find('ul').find_all('li')
                # 提取转发数
                repost_text = action_buttons[0].find('a').text
                repost = int(repost_text) if repost_text.isdigit() else 0
                # 提取评论数
                comment_text = action_buttons[1].find('a').text
                comment = int(comment_text) if comment_text.isdigit() else 0
                # 提取点赞数
                like_text = action_buttons[2].find('a').find('span', class_='woo-like-count').text
                like = int(like_text) if like_text.isdigit() else 0

                user_names.append(user_name)
                post_times.append(post_time)
                contents.append(content)
                reposts.append(repost)
                comments.append(comment)
                likes.append(like)
            except Exception as e:
                print(f"提取第 {page} 页数据时出错：", e)

        all_user_names.extend(user_names)
        all_post_times.extend(post_times)
        all_contents.extend(contents)
        all_reposts.extend(reposts)
        all_comments.extend(comments)
        all_likes.extend(likes)

    except Exception as e:
        print(f"请求第 {page} 页时出错：", e)

    time.sleep(2)  # 避免请求过快被封 IP

# 将所有数据追加到 CSV 文件
csv_file_path = "爬虫4.csv"
with open(csv_file_path, 'a', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['用户名', '发帖时间', '正文内容', '转发数', '评论数', '点赞数']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if csvfile.tell() == 0:  # 如果文件为空，则写入表头
        writer.writeheader()
    for i in range(len(all_user_names)):
        writer.writerow({
            '用户名': all_user_names[i],
            '发帖时间': all_post_times[i],
            '正文内容': all_contents[i],
            '转发数': all_reposts[i],
            '评论数': all_comments[i],
            '点赞数': all_likes[i]
        })

# 关闭浏览器
driver.quit()
