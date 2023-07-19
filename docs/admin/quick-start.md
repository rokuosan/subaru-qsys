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
7. 問題の難易度を作成する
8. 問題を作成する
9. CTF開催情報を作成する
10. CTFを開催中にする

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

## 5. ユーザーを作成します

ユーザーを作成する方法はいくつか存在しますが、推奨する方法を2つ紹介します。

それぞれのメリット・デメリットを紹介します。

| 手段                     | メリット                                     | デメリット                                                   |
|:-----------------------: | :------------------------------------------: | :----------------------------------------------------------: |
| 1人ずつ作成する          | 任意のパスワードと管理者ユーザーを追加できる | 複数人追加する場合は手間がかかる                             |
| 複数人をまとめて作成する | 複数人を一度に追加できる                     | パスワードがランダムに設定される。管理者ユーザーを作れない。 |

### 1人ずつ作成する

管理者ユーザーでログイン後、[User Manager](http://localhost/manager/user/)に接続する。

表示されるフォームに名前とパスワード、管理者フラグを設定して、送信ボタンを押してください。

![image](https://github.com/rokuosan/subaru-qsys/assets/85651386/1e4ba11f-9559-4202-aae5-42ce2e07c544)

### 複数人をまとめて作成する

管理者ユーザーでログイン後、[User Manager](http://localhost/manager/user/)に接続する。

「複数のユーザーを一括追加」タブを選択する。

![image](https://github.com/rokuosan/subaru-qsys/assets/85651386/1c708f66-53cf-4273-b724-ee2fcb2adb8b)

ユーザー名を1行ずつ書いてください。記入例を以下に示します。

![image](https://github.com/rokuosan/subaru-qsys/assets/85651386/31c83efd-de44-41ad-8a32-70a837c4bc29)

すべての入力が終われば、送信ボタンを一度だけおして、しばらく待機してください。

すべてのユーザーの作成が完了すると、ユーザー名と一時パスワードが書かれたCSVファイルがダウンロードされます。

> **Warning**
> 送信ボタンは一度だけ押してください！予期せぬエラーが発生する可能性があります！

### ユーザーをチームに追加する

作成したユーザーはどこかのチームに所属させることを推奨します。

Django管理サイトからユーザーの欄を選択すると、ユーザー一覧が表示されます。

ユーザー一覧からチームに所属させたいユーザーを選択します。

「Team」というドロップダウンメニューから所属させたいチームを選択し、ページ下部にある保存を押してください。

> **Warning**
> 保存を押さないと変更が適用されません！

## 6. 問題カテゴリを作成する

Django管理サイトからカテゴリの欄にある「+追加」ボタンを押してください。

Nameと書かれたフィールドにカテゴリ名を入力してください。

> **Warning**
> Nameの内容がそのままカテゴリ名として表示されます。
> 先頭の文字のみ、自動的に小文字から大文字に変換されます。
>
> (例) sample category -> Sample category

## 7. 問題の難易度を作成する

Django管理サイトから難易度の欄にある「+追加」ボタンを押してください。

Nameと書かれたフィールドに難易度名を入力してください。

> **Warning**
> Nameの内容がそのままカテゴリ名として表示されます。

## 8. 問題を作成する

Django管理サイトからCTF問題の欄にある「+追加」ボタンを押します。

太字になっているフィールドをすべて埋めて、ページ下部にある保存ボタンを押して問題を作成します。

``is_published``のチェックボックスは、問題の可視性を操作します。チェックを入れない場合、その問題はユーザーに表示されません。

## 9. CTF開催情報を作成する

Django管理サイトからCTF情報の欄にある「+追加」ボタンを押します。

太字になっているフィールドをすべて埋めて、ページ下部にある保存ボタンを押して作成します。

QuestionsとParticipantsは複数選択が可能です。Shiftとクリックで範囲選択、Ctrlとクリックで選択追加することができます。

is_activeは、そのCTFが開催中であるかを管理します。チェックは外したままにしておいてください。

is_pausedは、開催中のCTFを一時停止するときに利用するフラグのため、無視してください。

Show team/player ranking についてはお好みで選択してください。

## 10. CTFを開催中にする

スーパーユーザーでログイン後、ナビゲーションバーのControlから[CTF Manager](http://localhost/manager/ctf/)を選択します。

9の手順でCTF情報を1つ追加している場合、このような表示になります。

![image](https://github.com/rokuosan/subaru-qsys/assets/85651386/281cb960-bbf0-42fb-a768-5aae71e804cb)


> もし、CTF情報を登録する際に``is_active``にチェックを入れている場合は、以下のような表示になります。
>
> ![image](https://github.com/rokuosan/subaru-qsys/assets/85651386/a187b2d9-f71d-4d20-b643-ae73a6af4b08)


「再実施する」ボタンを押すとモーダルが表示されます。注意事項をよく読んだ上で「再開する」ボタンを押してください。

![image](https://github.com/rokuosan/subaru-qsys/assets/85651386/6495bf45-48b5-47ce-8d15-30f6cec1be78)

CTFが正常に再開されると、以下のような表示になります。

![image](https://github.com/rokuosan/subaru-qsys/assets/85651386/bbd8e635-09ac-4cc3-8e35-71e5b4c17e92)

これで、CTFが実施していることになりました。

ただし、このままだと表示にもあるようにこのCTFは「一時停止中」です。

再開する場合は「再開」ボタンを押してください。

モーダルが表示されますが、ここも「再開する」ボタンを押すことで再開することができます。

正常に再開できれば、右上の表示が実施中に変わっています。

![image](https://github.com/rokuosan/subaru-qsys/assets/85651386/621fc981-7217-4c66-8d05-28e7be3d227d)

