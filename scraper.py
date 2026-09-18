"""
Web 爬虫入门：抓取网页新闻标题并保存到 CSV。

用法示例：
    python scraper.py
    python scraper.py --url https://news.ycombinator.com/ --selector ".titleline > a"
    python scraper.py --output my_news.csv --delay 2
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

# ---------- 默认配置 ----------
DEFAULT_URL = "https://news.ycombinator.com/"
DEFAULT_OUTPUT = "news.csv"
DEFAULT_SELECTOR = ".titleline > a"   # Hacker News 的标题选择器
DEFAULT_DELAY = 1.0                   # 每次请求间隔（秒）
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)
TIMEOUT = 10


# ---------- robots.txt 检查 ----------
def is_allowed(url: str, user_agent: str = "*") -> bool:
    """检查 robots.txt 是否允许抓取该 URL。"""
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    rp = RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except Exception as exc:
        print(f"⚠️ 无法读取 robots.txt（{robots_url}）：{exc}")
        # 读不到时保守起见，默认不允许
        return False

    allowed = rp.can_fetch(user_agent, url)
    if not allowed:
        print(f"🚫 robots.txt 不允许抓取：{url}")
    return allowed


# ---------- 请求页面 ----------
def fetch_html(url: str, headers: dict | None = None, timeout: int = TIMEOUT) -> str:
    """发送 GET 请求，返回 HTML 文本。"""
    headers = headers or {"User-Agent": USER_AGENT}
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"请求失败：{exc}") from exc

    # 尽量使用服务器声明的编码，避免中文乱码
    resp.encoding = resp.apparent_encoding or resp.encoding
    return resp.text


# ---------- 解析标题 ----------
def parse_titles(html: str, selector: str) -> list[str]:
    """用 CSS 选择器提取标题文本，去重并保持顺序。"""
    soup = BeautifulSoup(html, "html.parser")
    titles: list[str] = []
    seen: set[str] = set()

    for tag in soup.select(selector):
        text = tag.get_text(strip=True)
        if text and text not in seen:
            seen.add(text)
            titles.append(text)

    return titles


# ---------- 保存 CSV ----------
def save_csv(titles: list[str], path: str | Path) -> None:
    """将标题写入 CSV，第一列为序号。"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["序号", "标题"])
        for i, title in enumerate(titles, 1):
            writer.writerow([i, title])


# ---------- 主流程 ----------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="抓取网页新闻标题并保存到 CSV")
    parser.add_argument("--url", default=DEFAULT_URL, help="目标网页 URL")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="输出 CSV 文件路径")
    parser.add_argument("--selector", default=DEFAULT_SELECTOR,
                        help="CSS 选择器，用于定位标题元素")
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY,
                        help="请求间隔秒数（默认 1 秒）")
    parser.add_argument("--ignore-robots", action="store_true",
                        help="跳过 robots.txt 检查（请谨慎使用）")
    args = parser.parse_args(argv)

    # 1) 检查 robots.txt
    if not args.ignore_robots:
        if not is_allowed(args.url, USER_AGENT):
            print("已停止：请遵守目标网站的 robots.txt。")
            return 1

    # 2) 请求页面
    print(f"正在请求：{args.url}")
    try:
        html = fetch_html(args.url)
    except RuntimeError as exc:
        print(f"❌ {exc}")
        return 2

    # 3) 解析标题
    titles = parse_titles(html, args.selector)
    if not titles:
        print("⚠️ 未找到任何标题，请检查 --selector 是否正确。")
        return 3

    # 4) 保存 CSV
    save_csv(titles, args.output)
    print(f"✅ 已抓取 {len(titles)} 条标题，保存到：{args.output}")

    # 5) 礼貌延迟（如果将来扩展多页抓取，可放在循环里）
    if args.delay > 0:
        time.sleep(args.delay)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())