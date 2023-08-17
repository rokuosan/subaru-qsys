---
title: autosetup による自動セットアップについて
---

このプロジェクトをより簡単にセットアップするための仕組みとして**autosetup**というコマンドを用意しています。

事前に用意した設定ファイルをもとにデータを自動作成するコマンドです。

ここではそのコマンドの使い方について説明します。

## 手順

1. ``init.yaml``を作成する
2. データベースを準備する
3. autosetupを実行する

## 1. init.yamlを作成する

``init.yaml``は、autosetupを行う際に必要になる設定定義ファイルです。

このファイルには以下の項目を設定することができます。(v1.1.0時点)

- 問題難易度
- 問題カテゴリ
- CTF問題
- チーム
- ユーザー

また、ユーザーの作成については一気に作成する方法と詳細に1人ずつ用意する方法を提供しており、それらを同時に利用することができます。

以下に``init.yaml``のサンプルを示します。

この``init.yaml``を``manage.py``があるディレクトリと同じ場所に作成してください。

つまり以下のようなディレクトリ構成になっている必要があります。

```
.
└── qsys
    ├── app
    ├── qsys
    ├── static
    ├── Dockerfile
    ├── init.yaml  <- 今回作成するファイル
    ├── manage.py  <- コマンドの実行に必要なファイル
    └── requirements.txt
```

```yaml
qsys:
  difficulty:
    - Tutorial
    - Normal
  category:
    - Practice
    - Network
  team:
    - Team A
    - Team B
    - Team C
  user:
    roughed:
      - 'Sample User 1'
      - 'Sample User 2'
      - 'Sample User 3'
    detailed:
      - username: 'Yamada Taro'
        team: 'Team A'
        is_admin: false
        password: 'sample'
  question:
    - title: 'Prac 1'
      difficulty: Tutorial
      category: Practice
      flag: 'flag{practice-1}'
      content: 'This is a practice question.'
      point: 100
```

文法などの詳細については[init.yaml について](../developer/syntax-of-init-yaml.md)を参照してください。


## 2. データベースを準備する

まず、``manage.py``があるディレクトリに移動します。 このプロジェクトをcloneした場合はデフォルトで``./subaru-qsys/qsys/``に格納されています。

次にマイグレーションを行うために、以下のコマンドを順番に実行してください。

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

これでデータベースの準備を行うことができました。

## 3. autosetupを実行する

autosetupを用いて自動セットアップを行うには、``manage.py``と同じディレクトリで以下のコマンドを実行します。

```bash
$ python manage.py autosetup
```

コマンドが正常に終了したのち、以下のコマンドで開発サーバを起動し、セットアップの確認を行ってみましょう。

```bash
$ python manage.py runserver
```

- [localhost:8000](http://localhost:8000)

``init.yaml``で記述したものと同様の項目が作成されていると思います。

また、パスワードの指定を行わずにユーザーの作成を行った場合、``passwords_数字4桁.csv``が作成されています。

そこには、新規追加したユーザの名前とランダムに作成したパスワードが一覧で表示されます。

> **Note**
> 校内で実施する場合、このCSVファイルの印刷および切り取りを行うことで楽にアカウントの配布が行なえます。
