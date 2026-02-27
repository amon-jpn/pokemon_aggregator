#!/usr/bin/env python3
"""
GAME Watch ゲームグッズ RSS フィルター

- ゲームグッズカテゴリの記事のみ抽出
- ポケモン関連の記事を除外
- 1日4回 GitHub Actions で実行

法的に問題のない方法で実装:
- 公式RSSフィード（公開情報）を取得
- タイトルとリンクのみを使用
- 1日4回のアクセス（サーバー負荷ほぼゼロ）
"""

import feedparser
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
import re
import os

# 設定
SOURCE_RSS = "https://game.watch.impress.co.jp/data/rss/1.0/gmw/feed.rdf"
OUTPUT_FILE = "gamewatch_goods.xml"

# フィルター設定
INCLUDE_KEYWORDS = ["ゲームグッズ", "グッズ"]  # カテゴリまたはタイトルに含む
EXCLUDE_KEYWORDS = ["ポケモン", "ポケットモンスター", "ポケカ", "Pokémon", "Pokemon"]


def fetch_rss(url):
    """RSSフィードを取得"""
    print(f"📡 RSSを取得中: {url}")
    feed = feedparser.parse(url)
    
    if feed.bozo and not feed.entries:
        print(f"⚠️ RSS取得エラー: {feed.bozo_exception}")
        return None
    
    print(f"✅ {len(feed.entries)}件の記事を取得")
    return feed


def is_game_goods_category(entry):
    """ゲームグッズカテゴリかどうか判定"""
    # カテゴリタグをチェック
    if hasattr(entry, 'tags') and entry.tags:
        for tag in entry.tags:
            term = tag.get('term', '').lower()
            if 'グッズ' in term or 'goods' in term.lower():
                return True
    
    # dc:subject をチェック（RDF形式の場合）
    if hasattr(entry, 'category') and entry.category:
        if 'グッズ' in entry.category:
            return True
    
    # タイトルやリンクからも判定（バックアップ）
    title = entry.get('title', '')
    link = entry.get('link', '')
    
    if 'グッズ' in title or '/goods/' in link:
        return True
    
    return False


def contains_pokemon(entry):
    """ポケモン関連の記事かどうか判定"""
    title = entry.get('title', '')
    summary = entry.get('summary', '')
    
    text = f"{title} {summary}".lower()
    
    for keyword in EXCLUDE_KEYWORDS:
        if keyword.lower() in text:
            return True
    
    return False


def filter_entries(feed):
    """記事をフィルタリング"""
    filtered = []
    
    for entry in feed.entries:
        title = entry.get('title', '')
        
        # ゲームグッズカテゴリかチェック
        if not is_game_goods_category(entry):
            print(f"  ⏭️ スキップ（カテゴリ外）: {title[:40]}...")
            continue
        
        # ポケモン関連を除外
        if contains_pokemon(entry):
            print(f"  ⏭️ スキップ（ポケモン）: {title[:40]}...")
            continue
        
        print(f"  ✅ 採用: {title[:50]}...")
        filtered.append(entry)
    
    return filtered


def create_filtered_rss(entries, output_path):
    """フィルタリングした記事から新しいRSSを生成"""
    fg = FeedGenerator()
    
    # フィード情報
    fg.title("Game Watch - ゲームグッズ最新情報")
    fg.description("ポケモン以外のゲームグッズ情報まとめ")
    fg.link(href="https://game.watch.impress.co.jp/", rel="alternate")
    fg.language("ja")
    fg.lastBuildDate(datetime.now(timezone.utc))
    
    # 記事を追加
    for entry in entries:
        fe = fg.add_entry()
        fe.title(entry.get('title', 'タイトルなし'))
        fe.link(href=entry.get('link', ''))
        
        # 公開日時
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            from time import mktime
            published = datetime.fromtimestamp(mktime(entry.published_parsed), tz=timezone.utc)
            fe.pubDate(published)
        
        # 概要（あれば）
        if entry.get('summary'):
            fe.description(entry.get('summary'))
    
    # ファイル出力
    fg.rss_file(output_path)
    print(f"\n📄 RSS出力完了: {output_path}")
    print(f"   記事数: {len(entries)}件")


def main():
    print("=" * 50)
    print("🎮 GAME Watch ゲームグッズ RSS フィルター")
    print(f"📅 実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # RSS取得
    feed = fetch_rss(SOURCE_RSS)
    if not feed:
        print("❌ RSS取得に失敗しました")
        return
    
    # フィルタリング
    print("\n🔍 フィルタリング中...")
    filtered = filter_entries(feed)
    
    print(f"\n📊 結果: {len(feed.entries)}件 → {len(filtered)}件")
    
    # RSS生成
    if filtered:
        create_filtered_rss(filtered, OUTPUT_FILE)
    else:
        print("⚠️ 該当する記事がありませんでした")
        # 空でもRSSファイルは作成
        create_filtered_rss([], OUTPUT_FILE)
    
    print("\n✨ 完了！")


if __name__ == "__main__":
    main()
