import feedparser
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
import difflib
import time

# 設定
RSS_SOURCES = [
    "https://game.watch.impress.co.jp/data/rss/1.0/gmw/feed.rdf",
    "https://www.ndw.jp/feed/",
    "https://www.4gamer.net/publisher/013/P01387/contents.xml",
    "https://hobby.watch.impress.co.jp/data/rss/1.0/hbw/feed.rdf"
]
OUTPUT_FILE = "pokemon_news.xml"
KEYWORD = "ポケモン"
SIMILARITY_THRESHOLD = 0.85  # レベル3: 類似度85%以上を重複と判定

def get_similarity(a, b):
    """タイトルの類似度を計算"""
    return difflib.SequenceMatcher(None, a, b).ratio()

def main():
    all_entries = []
    
    # 1. 各フィードから記事を取得
    for url in RSS_SOURCES:
        print(f"📡 取得中: {url}")
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get('title', '')
            summary = entry.get('summary', entry.get('description', ''))
            
            # キーワード「ポケモン」が含まれるか判定
            if KEYWORD in title or KEYWORD in summary:
                # 投稿日時を取得
                pub_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime.fromtimestamp(time.mktime(entry.published_parsed), tz=timezone.utc)
                
                all_entries.append({
                    'title': title,
                    'link': entry.link,
                    'date': pub_date,
                    'summary': summary
                })

    # 2. 重複排除（レベル3：類似度判定）
    unique_entries = []
    for entry in all_entries:
        is_duplicate = False
        for existing in unique_entries:
            # タイトルの類似度をチェック
            if get_similarity(entry['title'], existing['title']) > SIMILARITY_THRESHOLD:
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_entries.append(entry)

    # 3. 日付順にソート（新しい順）
    unique_entries.sort(key=lambda x: x['date'] if x['date'] else datetime.min.replace(tzinfo=timezone.utc), reverse=True)

    # 4. 新しいRSSを生成
    fg = FeedGenerator()
    fg.title("ポケモン最新ニュースまとめ")
    fg.description("複数サイトからポケモン関連の記事を重複なく集約")
    fg.link(href="https://github.com/", rel="alternate")
    fg.language("ja")
    fg.lastBuildDate(datetime.now(timezone.utc))

    for item in unique_entries:
        fe = fg.add_entry()
        fe.title(item['title'])
        fe.link(href=item['link'])
        fe.description(item['summary'])
        if item['date']:
            fe.pubDate(item['date'])

    fg.rss_file(OUTPUT_FILE)
    print(f"✅ 完了: {len(unique_entries)}件の記事を抽出しました。")

if __name__ == "__main__":
    main()
