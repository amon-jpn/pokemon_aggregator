# Pokemon News Aggregator

複数のゲームニュースサイトから「ポケモン」に関する最新情報だけを自動で収集し、重複を除去して配信する自分専用のRSSフィード生成器です。

## 主な機能

* **キーワード抽出**: 「ポケモン」という単語が含まれる記事のみを厳選します。
* **高度な重複排除**: 
    * `difflib` を使用したタイトル類似度判定を実装。
    * サイト間でタイトルが微妙に異なる場合（例：末尾の「！」の有無など）でも、同じ内容なら1つに集約します。
* **完全自動運用**: 
    * GitHub Actionsにより、1日4回（日本時間 6:00, 12:00, 18:00, 24:00）自動更新。
    * サーバーの維持費は一切かかりません。

---

## 購読用RSS URL

お手持ちのRSSリーダー（Feedly, Inoreaderなど）に以下のURLを登録してください。
```text
https://amon-jpn.github.io/pokemon_aggregator/pokemon_news.xml
```

取得元ソース

GAME Watch

Nintendo DREAM WEB

4Gamer.net

Hobby Watch
