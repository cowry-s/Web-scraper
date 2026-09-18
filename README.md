# Web-scraper：新闻标题抓取

一个使用 `requests` 和 `BeautifulSoup` 抓取网页新闻标题并保存到 CSV 的入门项目。  
适合学习 HTTP 请求、HTML 解析、CSV 写入以及基本的反爬注意事项。

## ✨ 功能特性

- 使用 `requests` 发送 HTTP GET 请求
- 使用 `BeautifulSoup` 解析 HTML
- 提取网页中的新闻标题（可根据目标网站调整选择器）
- 将结果保存为 CSV 文件（`news.csv`）
- 支持自定义 User-Agent，模拟浏览器请求
- 添加请求间隔，避免高频访问
- 基本的异常处理（网络错误、解析失败等）
- 尊重 `robots.txt`（示例中会说明如何检查）

## 📁 项目结构

```
web-scraper/
├── scraper.py          # 主程序：请求 + 解析 + 写入 CSV
├── news.csv            # 输出文件（运行后生成）
├── requirements.txt    # 依赖列表
└── README.md           # 项目说明
```

> 如果你的文件名不同，请把下面命令中的文件名替换成实际文件名。

## 🚀 快速开始

### 环境要求

- Python 3.6 或更高版本
- 可访问互联网

### 安装依赖

```bash
pip install requests beautifulsoup4
```

或者使用 `requirements.txt`：

```bash
pip install -r requirements.txt
```

`requirements.txt` 内容：

```text
requests
beautifulsoup4
```

### 运行方式

```bash
python scraper.py
```

运行后程序会：

1. 请求目标网页
2. 解析 HTML 并提取新闻标题
3. 将标题写入 `news.csv`
4. 在控制台打印抓取数量

## 📖 代码说明

### 核心步骤

1. **发送请求**  
   ```python
   headers = {"User-Agent": "Mozilla/5.0 ..."}
   response = requests.get(url, headers=headers, timeout=10)
   response.raise_for_status()
   ```

2. **解析 HTML**  
   ```python
   soup = BeautifulSoup(response.text, "html.parser")
   titles = [tag.get_text(strip=True) for tag in soup.select("h2.news-title")]
   ```

3. **写入 CSV**  
   ```python
   import csv
   with open("news.csv", "w", newline="", encoding="utf-8-sig") as f:
       writer = csv.writer(f)
       writer.writerow(["序号", "标题"])
       for i, title in enumerate(titles, 1):
           writer.writerow([i, title])
   ```

4. **添加延迟**  
   ```python
   import time
   time.sleep(1)  # 每次请求间隔 1 秒
   ```

### 可调整的部分

- **目标 URL**：修改 `url` 变量。
- **CSS 选择器**：不同网站的标题标签不同，需根据实际情况调整 `soup.select(...)`。
- **输出文件名**：修改 `news.csv` 为其他名称。
- **请求头**：可添加更多头信息，如 `Referer`、`Accept-Language` 等。

## 📄 输出示例

`news.csv` 内容示例：

```csv
序号,标题
1,今日头条：科技创新引领未来
2,国内新闻：经济发展稳中向好
3,国际要闻：全球气候大会召开
```

## ⚠️ 反爬注意事项

1. **尊重 robots.txt**  
   在抓取前，先查看目标网站的 `robots.txt`，例如：  
   `https://example.com/robots.txt`  
   确认允许抓取的路径。可以使用 Python 的 `urllib.robotparser` 自动检查：
   ```python
   from urllib.robotparser import RobotFileParser
   rp = RobotFileParser()
   rp.set_url("https://example.com/robots.txt")
   rp.read()
   print(rp.can_fetch("*", "https://example.com/news"))
   ```

2. **避免高频请求**  
   每次请求之间至少间隔 1 秒，必要时可更长。  
   不要使用多线程高并发抓取，除非目标网站明确允许。

3. **设置合理的 User-Agent**  
   不要使用默认的 `python-requests`，建议模拟常见浏览器。

4. **遵守网站服务条款**  
   仅抓取公开数据，不抓取个人隐私或受版权保护的内容。

5. **处理异常**  
   网络请求可能失败，使用 `try/except` 捕获 `requests.RequestException`，避免程序崩溃。

6. **不要抓取登录后页面**  
   除非你有明确授权，否则不要模拟登录或绕过访问限制。

## 🧪 可选扩展练习

- 支持抓取多个页面（分页）
- 将标题、链接、时间等一起保存
- 增加命令行参数：`--url`、`--output`、`--delay`
- 使用 `pandas` 保存为 Excel 或 JSON
- 添加日志记录，便于排查问题
- 使用 `lxml` 解析器提升解析速度
- 为解析函数编写单元测试（使用本地 HTML 样本）

## 🧠 学习目标

这个项目适合练习：

- HTTP 请求：`requests.get`、状态码、请求头
- HTML 解析：`BeautifulSoup`、CSS 选择器、`.get_text()`
- 文件写入：`csv` 模块、编码处理（`utf-8-sig`）
- 反爬基础：`robots.txt`、请求间隔、User-Agent
- 异常处理：网络错误、超时、解析失败

## 📄 许可证

本项目仅供学习使用，请遵守目标网站的 robots.txt 和服务条款。可自由修改和分发。
