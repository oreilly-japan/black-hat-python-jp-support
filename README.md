# 『サイバーセキュリティプログラミング』のサポートページ

本リポジトリはオライリー・ジャパン発行書籍『[サイバーセキュリティプログラミング](http://www.oreilly.co.jp/books/9784873117317/)』（原書名『[Black Hat Python](https://www.nostarch.com/blackhatpython)』） のサポートサイトです。

## サンプルコード

サンプルコードの解説は本書籍をご覧ください。

### 補足事項

#### （付録A）bhpasm.pyが異常終了する事象について

2015/10/28にmiasmの`parse_txt`関数の戻り値が[変更](https://github.com/cea-sec/miasm/commit/dfdcae8bfeefc5c4395ee1e909bab83e211ffefb)されました。
この変更に伴い、2015/10/28以降のmiasmがセットアップされた状態でbhpasm.pyを実行すると、以下のような例外が発生します。
```sh
$ python bhpasm.py
Traceback (most recent call last):
  File "bhpasm.py", line 57, in <module>
    native_code = assemble_text(asm_helloworld, [("L_MAIN", 0)])
  File "bhpasm.py", line 15, in assemble_text
    patches = asmbloc.asm_resolve_final(mnemo, sections[0], symbol_pool)
  File "/usr/local/lib/python2.7/dist-packages/miasm2/core/asmbloc.py", line 1050, in asm_resolve_final
    sanity_check_blocks(blocks)
  File "/usr/local/lib/python2.7/dist-packages/miasm2/core/asmbloc.py", line 1031, in sanity_check_blocks
    blocks_graph = basicblocs(blocks)
  File "/usr/local/lib/python2.7/dist-packages/miasm2/core/asmbloc.py", line 1097, in __init__
    self.add_blocs(ab)
  File "/usr/local/lib/python2.7/dist-packages/miasm2/core/asmbloc.py", line 1107, in add_blocs
    for b in ab:
TypeError: 'asm_bloc' object is not iterable
```

対処としては、本書執筆時点の[miasm](https://github.com/cea-sec/miasm/tree/dcc488ec39d9a96b70c728ccdbcd43e62b25ae99)をご利用ください。
具体的には、付録Aに記載されている[Dockerfile](/appendix-A/bhp_miasm/Dockerfile)のコメント記号（#）を削除しイメージを再構築することで、本書執筆時点のmiasmをご利用いただけます。

## 正誤表

下記の通り、誤記がありましたので訂正いたします。ご迷惑をおかけいたしましたことをお詫び申し上げます。
本ページに掲載されていない誤植・間違いを見つけた方は、japan_at_oreilly.co.jpまでお知らせください。

### 第1刷、第2刷、第3刷、第4刷をお持ちの方

#### P39の図2-3内
誤

```
ssh -L 8008:web:80 justin@sshserver
```

正

```
ssh -R 8008:web:80 justin@sshserver
```

#### P59の3行目
誤

```
191.68.0.0/24
```

正

```
192.168.0.0/24
```


### 第1刷および第2刷をお持ちの方

#### P10の1行目

誤

```
3行目
```

正

```
2行目
```

#### P18 ページ下部のソースコード

誤

```python
print "Usage: bhpnet.py -t target_host -p port"
```

正

```python
print "Usage: bhnet.py -t target_host -p port"
```

#### P19 ソースコード

誤

```python
print "bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
print "bhpnet.py -t 192.168.0.1 -p 5555 -l -u c:\\target.exe"
print "bhpnet.py -t 192.168.0.1 -p 5555 -l -e \"cat /etc/passwd\""
print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
```

正

```python
print "bhnet.py -t 192.168.0.1 -p 5555 -l -c"
print "bhnet.py -t 192.168.0.1 -p 5555 -l -u c:\\target.exe"
print "bhnet.py -t 192.168.0.1 -p 5555 -l -e \"cat /etc/passwd\""
print "echo 'ABCDEFGHI' | ./bhnet.py -t 192.168.11.12 -p 135"
```

#### P79 ソースコード

誤

```python
filters   = [".jpg",".gif","png",".css"]
```

正

```python
filters   = [".jpg",".gif",".png",".css"]
```

#### P122 コマンド実行

誤

```
$ pip install github3
```

正

```
$ pip install github3.py
```

#### P122 注釈

誤

```
【＊1.】ライブラリは<https://github.com/copitux/python-github3/>から入手可能。
```

正

```
【＊1.】ライブラリは<https://github.com/sigmavirus24/github3.py/>から入手可能。
```

#### P144 上から9行目

誤

```
サンドバックス
```

正

```
サンドボックス
```

#### P162 「10.1 必要要素のインストール」の17行目

誤

```
1. 次のzipファイルをダウンロードする。
http://www.nostarch.com/blackhatpython/bhpservice.zip
2. バッチファイル`install_service.bat`を使用してサービスをインストールする。`Administrator`同等の権限で実行することを忘れずに。
```

正

```
1. 本書日本語版のサポートページにある次のリポジトリを複製する。
https://github.com/oreilly-japan/black-hat-python-jp-support/tree/master/chapter-10

2. `bhservice.rtf`を参考にサービスをインストールする（`Administrator`同等の権限で実行することを忘れずに）。
```



#### P173 「10.5 コードインジェクション」の4行目

誤

```
そこでコンパイル済みバージョンのbhpnet.py（2章で作成）
```

正

```
そこでコンパイル済みバージョンのbhnet.py（2章で作成）
```

#### P173 ページ下部のソースコード

誤

```python
command = "C:\\WINDOWS\\TEMP\\bhpnet.exe -l -p 9999 -c"
```

正

```python
command = "C:\\WINDOWS\\TEMP\\bhnet.exe -l -p 9999 -c"
```

#### P175 「試してみる」の6行目

誤

```
スクリプトbhpnet.pyを使用して、
```

正

```
スクリプトbhnet.pyを使用して、
```

#### P175 「試してみる」の実行結果

誤

```shell-session
justin$ ./bhpnet.py -t 192.168.1.10 -p 9999
```

正

```shell-session
justin$ ./bhnet.py -t 192.168.1.10 -p 9999
```
