スマートウィキ
==============

開発環境
--------

* Python 2.7
* Google App Engine 1.5.4
* Python-Markdown 2.0.3

特徴
----

* Google App Engine 上で動く wiki エンジン
* 既存の軽量マークアップ言語を wiki 記法に採用 (Markdown Extra)
* ページ名を検出して本文に自動リンク
* 自動 URL リンク

作成について
------------

Google の cccwiki を参考に作成。

作成者: 稲尾 遊
作成期間: 1週間

TODO
----

* Twitter アカウントベースのログイン機能
* ログイン編集者と匿名編集者の権限変更
* 編集履歴の保存
* テンプレートエンジンを Genshi に変更
* 複数軽量マークアップ言語への対応 (reStructuredText 等)
