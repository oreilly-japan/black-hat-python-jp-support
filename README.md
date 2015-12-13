# 『サイバーセキュリティプログラミング』のサポートページ

本リポジトリはオライリー・ジャパン発行書籍『[サイバーセキュリティプログラミング](http://www.oreilly.co.jp/books/9784873117317/)』（原書名『[Black Hat Python](https://www.nostarch.com/blackhatpython)』） のサポートサイトです。

## サンプルコード

サンプルコードの解説は本書籍をご覧ください。

## 正誤表

下記の通り、誤記がありましたので訂正いたします。ご迷惑をおかけいたしましたことをお詫び申し上げます。
本ページに掲載されていない誤植・間違いを見つけた方は、japan_at_oreilly.co.jpまでお知らせください。

### 第1刷および第2刷をお持ちの方

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

#### P144 上から9行目

誤

```
サンドバックス
```

正

```
サンドボックス
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
