# Subaru Q-Sys

これは校内CTFを実施するためのDjangoアプリケーションです。

## Documentation

詳細なドキュメントは[docs/README.md](./docs/README.md)を参照してください。

## Requirements

- Python 3.10+
- Docker
- Docker Compose
- Git

## Installation

> **Note**
> ここではQ-Sysの起動方法を説明します。

このリポジトリをクローンします。

```bash
$ git clone git@github.com:rokuosan/subaru-qsys.git
$ cd subaru-qsys
```

Docker Composeを利用してサービスを起動します。

```bash
$ docker compose up -d
```

以下のURLからダッシュボードに接続します。

初回起動ではDBのセットアップが行われるため、接続までに時間がかかる場合があります。

- [http://localhost/](http://localhost/)

## Libraries

使用した主要なライブラリは以下の通りです。

| Name | Version |
| :- | :-: |
| Django | 4.2.4 |
| Bootstrap | 5.2.3 |
| django-bootstrap5 | 23.3 |
| django-prometheus | 2.3.1 |

