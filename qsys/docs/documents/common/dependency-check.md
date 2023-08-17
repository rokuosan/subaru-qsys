---
title: 前提アプリケーションのインストール確認
---

ここでは、前提となるアプリケーションがインストールされているかを確認する手順を説明します。

## 前提アプリケーション

このプロジェクトを利用するには以下のアプリケーションが必要です。

- Python 3.10+
- Docker (+ Docker Compose)
- git

## 前提アプリケーションがインストールされているか確認する

インストールされてるか確認するためには以下のコマンドを実行してください。

エラーが発生する場合はインストールされていません。

```bash
$ python -V
$ docker -v
$ docker compose version
$ git version
```

実行例を以下に示します。

```bash
$ python -V
Python 3.11.4

$ docker -v
Docker version 20.10.25+azure-2, build b82b9f3a0e763304a250531cb9350aa6d93723c9

$ docker compose version
Docker Compose version 2.19.0+azure-1

$ git version
git version 2.41.0
```
