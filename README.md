# Subaru Q-Sys

これは校内CTFを実施するためのDjangoアプリケーションです。

## Installation

### Requirements

- Python 3.10+
- Docker
- Docker Compose

### Setup

> **Note**
> Q-Sysを起動して、ダッシュボードを起動するまでの方法をここに記載します。
> CTFの開催などは[docs/README.md](docs/README.md)を確認してください。

このアプリケーションをダウンロードします。

```bash
$ git clone git@github.com:rokuosan/subaru-qsys.git
$ cd subaru-qsys
```

> **Note**
> もしPython仮想環境を利用する場合は以下のコマンドで仮想環境を作成できます。
> ```
> $ python -m venv venv
> ```

以下コマンドを使ってデータベースを作成します。

```bash
$ cd qsys
$ python manage.py makemigrations
$ python manage.py migrate
```

スーパーユーザー(管理者アカウント)を作成します。

```bash
$ python manage.py createsuperuser
Username: 任意の名前を入力
Password: パスワードを入力(表示されません)
Password (again): パスワードを再入力(表示されません)
```

サーバーとその他サービスを起動します。

```bash
$ cd ..
$ docker compose up -d
```

## Libraries

使用したライブラリは以下の通りです。

| Name | Version |
| :-: | :-: |
| Django | 4.2.2 |
| Bootstrap | 5.2.3 |
| django-bootstrap5 | 23.3 |
| django-prometheus | 2.3.1 |

## Documentation

詳細なドキュメントは[docs/README.md](docs/README.md)を参照してください。
