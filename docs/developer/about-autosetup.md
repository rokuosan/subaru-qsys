# autosetup について

ここでは、自動セットアップコマンド``autosetup``について説明します。

## 概要

``autosetup``はDjangoの管理CLIツールである``manage.py``のサブコマンドとして動作します。

``autosetup``ではDjangoのORマッパーを利用したデータベースの操作を行い、初期セットアップにおける煩雑さから運用者と開発者を解放します。

設定定義ファイルを複製することで、様々な場所で同じ環境をすぐさま再現することができます。

## 仕組み

``autosetup``では設定定義ファイルとして、``init.yaml``からデータを取得します。

このため、``autosetup``実行時には作業ディレクトリに``init.yaml``を用意しておく必要があります。

ファイル名については、拡張子のフォールバックなどは行わないため必ず``init.yaml``を利用してください。

## ソースコード

ソースコードは[./qsys/app/management/commands/autosetup.py](../../qsys/app/management/commands/autosetup.py)にあります。
