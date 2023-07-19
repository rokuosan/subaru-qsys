# クイックスタートガイド

ここではこのアプリケーションを利用してCTFを開催するまでの手順を簡単に説明します。

このアプリケーションを実行するPCに以下の前提となるアプリケーションが
インストールされていることを確認してください。

前提アプリケーションがインストールされているかを確認するには以下のドキュメントを参照してください。

- [前提アプリケーションのインストール確認](../common/dependency-check.md)

## おおまかな手順

1. データベースの作成
2. スーパーユーザー(管理者アカウント)の作成
3. サービスの起動
4. チームを作成する
5. ユーザーを作成する
6. 問題カテゴリを作成する
7. 問題を作成する
8. CTF開催情報を作成する
9. CTFを開催中にする

## 1. データベースの作成

``manage.py``が存在するディレクトリで以下のコマンドを実行してください。

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

実行例を示します。

エラー以外の出力については、必ずこの結果になるとは限りません。

```bash
## 現在の作業ディレクトリを確認します
$ pwd
/workspaces/subaru-qsys/qsys
$ ls
Dockerfile  app  dev_requirements.txt  manage.py  qsys  requirements.txt  static  static.tar.gz

## データベースを作成するコマンドを実行します
$ python manage.py makemigrations
No changes detected
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, app, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  (※途中省略)
  Applying sessions.0001_initial... OK
```

## 2. スーパーユーザーの作成

スーパーユーザー(管理者アカウント)を作成します。

``manage.py``があるディレクトリで以下のコマンドを実行してください。

もし誤ってスーパーユーザーを削除してしまった場合も同様の手順で作成することができます。

```bash
$ python manage.py createsuperuser
```

実行例を示します。

Usernameをadminにする必要はありません。

```bash
$ python manage.py createsuperuser
Username: admin
Password: (※表示されません)
Password (again): (※表示されません)
Superuser created successfully.
```

## 3. サービスの起動

``compose.yaml``があるディレクトリで以下のコマンドを実行してください。

```bash
$ docker compose up -d
```

実行例を以下に示します。

```bash
$ docker compose up -d
[+] Running 4/4
 ✔ Network subaru-qsys_default         Created
 ✔ Container subaru-qsys-prometheus-1  Started
 ✔ Container subaru-qsys-grafana-1     Started
 ✔ Container subaru-qsys-server-1      Started
```

停止する場合は、先に示したコマンドの代わりに以下のコマンドを実行してください。

```bash
$ docker compose down
```

## 4. チームを作成する

ここからはコマンドの操作ではなく、ダッシュボードに接続してからの操作になります。

まず、[http://localhost/](http://localhost/)に接続してください。

接続すると以下のようなサイトが表示されます。

![image](https://github.com/rokuosan/subaru-qsys/assets/85651386/c8912cc0-5422-46c2-89d5-700c2001d18d)

右上、あるいは画面中央にあるログインボタンから、ログイン画面に移動します。

3の手順で作成したスーパーユーザーでログインします。

ログインすると以下のような画面にダッシュボードが変化します。

![image](https://github.com/rokuosan/subaru-qsys/assets/85651386/7df06e5f-2096-4872-908e-448294aba84c)

画面上にあるナビゲーションバーの一番右にある「Control」と書かれたドロップダウンリストを開く、一番下にある「Django Admin Panel」に移動します。

![image](https://github.com/rokuosan/subaru-qsys/assets/85651386/ffc0fbf5-16a8-4571-9c51-d612eccfe090)

このような画面になっていることを確認してください。

**このページのことを今後は「Django管理サイト」と呼ぶので、このページへの接続方法は覚えておいてください。**

![image](https://github.com/rokuosan/subaru-qsys/assets/85651386/67847b15-adcc-4489-b432-23d47254bc73)

Django管理サイトのチーム欄にある「+追加」を押すとチーム名とチェックボックスがあるフォームが表示されます。

ここからチームを好きなだけ追加してください。

