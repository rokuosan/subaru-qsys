# init.yaml について

``init.yaml``は``autosetup``を行うための、設定定義ファイルです。

ここでは、``init.yaml``の仕様について説明します。

## フォーマット

``init.yaml``は拡張子からわかるように、YAMLファイルとなっています。

書き方についてはYAMLの文法を調べてください。

## 文法

### 記述可能オブジェクト

``init.yaml``で記述可能なオブジェクトを以下に記します。

- qsys
  - difficulty
  - category
  - team
  - user
    - roughed
    - detailed
  - question

### qsys

このアプリケーション全体で利用するオブジェクトです。

名前空間の確保だけに用います。

### difficulty

| 型 | 対応するモデル |
| :-: | :-: |
| List | qsys.app.models.difficulty.CtfQuestionDifficulty |

CTFの問題の難易度を表すオブジェクトです。

サンプルを以下に示します

```yaml
qsys:
  difficulty:
    - Tutorial
    - Easy
    - Normal
    - Hard
```

### category

| 型 | 対応するモデル |
| :-: | :-: |
| List | qsys.app.models.category.CtfQuestionCategory |

CTFの問題のカテゴリを表すオブジェクトです。

サンプルを以下に示します

```yaml
qsys:
  category:
    - Practice
    - Network
    - Pwn
```

### team

| 型 | 対応するモデル |
| :-: | :-: |
| List | qsys.app.models.team.CtfTeam |

CTFのチームを表すオブジェクトです。

サンプルを以下に示します

```yaml
qsys:
  team:
    - Team A
    - Team B
    - Team C
```

### user

| 型 | 対応するモデル |
| :-: | :-: |
| Hash | qsys.app.models.app_user.AppUser |

Q-Sys全体のユーザーを表すオブジェクトです。

``user``を親にもつオブジェクトとして、``detailed``と``roughed``の2つが存在します。
これらはそれぞれ、詳細にユーザーを定義できるオブジェクトと、名前だけでユーザーを登録するオブジェクトです。

|オブジェクト|型|
|:-:|:-:|
| detailed | List [Object] |
| roughed | List [String] |

``detailed``の子要素にあるオブジェクトのプロパティを以下に示します。

| プロパティ | 型 | 説明 | 必須 |
| :-: | :-: | :-: | :-: |
| username | String | ユーザー名 | ◯ |
| password | String | パスワード(省略した場合、ランダムに作成されます) | |
| team | String | 所属させるチーム名 | |
| is_admin | Boolean | 管理者フラグ(Trueにすると管理者権限を持ちます) | |


サンプルを以下に示します

```yaml
qsys:
  user:
    # ユーザを簡易に追加する場合は以下のように記述する
    # パスワードはランダムに生成される
    roughed:
      - 'Sample User 1'
      - 'Sample User 2'
      - 'Sample User 3'
      - 'Sample User 4'

    # ユーザを詳細に設定する場合は以下のように記述する
    # username以外は省略可能
    detailed:
      - username: 'Yamada Taro'
        team: 'Team A'
        is_admin: false
        password: 'sample'
      - username: 'Suzuki Hanako'
        team: 'Team B'
        is_admin: false
        password: 'sample'
```

### question

| 型 | 対応するモデル |
| :-: | :-: |
| List [Object] | qsys.app.models.question.CtfQuestion |

CTFの問題を表すオブジェクトです。

``question``の子要素オブジェクトを以下に示します。

| プロパティ | 型 | 説明 | 必須 |
| :-: | :-: | :-: | :-: |
| title | String | 問題タイトル | ◯ |
| content | String | 問題文(指定しない場合、問題タイトルと同じになります) |  |
| difficulty | String | 難易度名 | ◯ |
| category | String | 問題カテゴリ | ◯ |
| flag | String | 問題フラグ(指定しない場合、ランダムに作成されます) | |
| point | Int | 問題の点数(指定しない場合、0になります) |  |

サンプルを以下に示します

```yaml
qsys:
  question:
    # 問題「Prac 1」
    - title: 'Prac 1'
      difficulty: Tutorial
      category: Practice
      flag: 'flag{1}'
      content: 'Practice 1'
      point: 100

    # 問題「Prac 2」
    - title: 'Prac 2'
      difficulty: Tutorial
      category: Practice
      flag: 'flag{2}'
      content: 'Practice 2'
      point: 200
```
