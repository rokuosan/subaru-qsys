# Subaru Q-Sys

これは校内CTFを実施するためのDjangoアプリケーションです。

## Documentation

詳細なドキュメントは[docs/README.md](docs/README.md)を参照してください。

## Requirements

- Python 3.10+
- Docker
- Docker Compose
- Git

## Installation

> **Note**
> ここではPythonのコマンドを``python``として記述します。

このリポジトリをクローンします。

```bash
$ git clone git@github.com:rokuosan/subaru-qsys.git
$ cd subaru-qsys
```

> **Note**
> 仮想環境を作成して実行することを推奨します。以下のコマンドで仮想環境を作成することができます。
> ```
> $ python -m venv venv
> ```

以下のコマンドで依存パッケージをインストールします。

```bash
$ cd qsys
$ pip install -r requirements.txt
```

以下コマンドを使ってデータベースを作成します。

```bash
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

以下のURLからダッシュボードに接続します。

- [http://localhost/](http://localhost/)

## Libraries

使用したライブラリは以下の通りです。

| Name | Version |
| :- | :-: |
| Django | 4.2.4 |
| Bootstrap | 5.2.3 |
| django-bootstrap5 | 23.3 |
| django-prometheus | 2.3.1 |

