---
title: WSLへのポートフォワーディングを行う方法
---

WSLでこのアプリケーションを実行した場合、外部からの接続を実現するためには、Windowsマシンからのポートフォワーディングもしくはトンネリングする必要があります。

ここでは、Windowsマシンからポートフォワーディングを行ってWSL内部のCTFに接続する方法について説明します。

## 前提条件

- WSLで利用しているディストリビューションはUbuntu系であること
- WSL2であること

## 手順

1. WSL内部のIPアドレスを調べる
2. WindowsホストのIPアドレスを調べる
3. コマンドを実行して、ポートフォワーディングを行う

## 1. WSL内部のIPアドレスを調べる

WSL内部で以下のコマンドを実行してください。

以下のコマンドではWSL内部に割り当てられているホストと接続するためのIPアドレスを取得することができます。

```bash
$ ip address show eth0 | awk '/inet / {print $2}' | awk -F / '{print $1}'
```

## 2. WindowsホストのIPアドレスを調べる

WindowsホストのIPアドレスを調べるには以下のコマンドを実行してください。

各インターフェースでのIPアドレスが表示されるため、ネットワークの接続状態に適したIPアドレスを選択してください。

```powershell
PS C:\Users\admin> ipconfig
```

> **Note**
> 執筆時点ではWiFiを利用した実施が想定されるため、WiFiアダプタのIPアドレスを使用してください。

## 3. コマンドを実行して、ポートフォワーディングを行う

以下のコマンドを利用してポートフォワーディングを行うための設定を流し込むことができます。

```powershell
PS C:\Users\admin> netsh interface portproxy add v4tov4 listenaddress=ホストIPアドレス listenport=ポート番号 connectaddress=WSL2のIPアドレス connectport=ポート番号
```

すでに条件が同じエントリーが存在し、新規追加することができない場合は以下のコマンドを実行してください。

```powershell
PS C:\Users\admin> netsh interface portproxy delete v4tov4 listenaddress=ホストのIPアドレス listenport=ポート番号
```

## 参考文献

- [WSL2のポートフォワードを自動化する](https://zenn.dev/fate_shelled/scraps/f6252654277ca0)
