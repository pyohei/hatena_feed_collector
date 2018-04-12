## 概要

指定しはてなユーザのブックマークから関連ユーザを調査し、自分に合う記事をレコメンドするスクリプトです。  
元は、[はてなブックマーク記事のレコメンドシステムを作成　PythonによるはてなAPIの活用とRによるモデルベースレコメンド](http://overlap.hatenablog.jp/entry/2013/06/30/232200)を参考にさせていただきました。  

## 使い方

### 環境

以下の環境が必要です。

* Python(2.7)

### インストール

このリポジトリをクローンするだけです。

```
git clone https://github.com/pyohei/hatena-bookmark-recommender
cd hatena-bookmark-recommender
```

### 実行

以下のコマンドで実行できます。

```
python2.7 main.py `はてなユーザー名`
```

実行後にレコメンド結果を表示します。  
サンプルは以下。  

```

```


## その他

何度やればちょっとずつ精度は上がると思います（多分）。  
データ自体は実行ディレクトリの直下の`hatena.db`に格納されます。  
日本のブログのため、READMEも日本語で記載しています。  

## ライセンス

* MIT
