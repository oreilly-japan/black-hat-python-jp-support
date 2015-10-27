#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import urllib
import threading
import Queue

threads        = 5
target_url     = "http://testphp.vulnweb.com"
wordlist_file  = "/tmp/all.txt" # SVNDiggerから
resume         = None
user_agent     = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"

def build_wordlist(wordlist_file):

    # 単語の辞書を読み取る
    fd = open(wordlist_file,"rb")
    raw_words = fd.readlines()
    fd.close()

    found_resume = False
    words        = Queue.Queue()

    for word in raw_words:

        word = word.rstrip()

        if resume is not None:

            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print "Resuming wordlist from: %s" % resume

        else:
            words.put(word)

    return words


def dir_bruter(extensions=None):

    while not word_queue.empty():
        attempt = word_queue.get()

        attempt_list = []

        # ファイル拡張子があるかどうかチェックする。もしなければディレクトリの
        # パスとして総当たり攻撃の対象とする。
        if "." not in attempt:
            attempt_list.append("/%s/" % attempt)
        else:
            attempt_list.append("/%s" % attempt)

        # 拡張子の総当たりをしたい場合
        if extensions:
            for extension in extensions:
                attempt_list.append("/%s%s" % (attempt,extension))

        # 作成したリストの最後まで繰り返す
        for brute in attempt_list:

            url = "%s%s" % (target_url,urllib.quote(brute))

            try:
                headers = {}
                headers["User-Agent"] = user_agent
                r = urllib2.Request(url,headers=headers)


                response = urllib2.urlopen(r)

                if len(response.read()):
                    print "[%d] => %s" % (response.code,url)

            except urllib2.HTTPError,e:

                if e.code != 404:
                    print "!!! %d => %s" % (e.code,url)

                pass


word_queue = build_wordlist(wordlist_file)
extensions = [".php",".bak",".orig",".inc"]

for i in range(threads):
            t = threading.Thread(target=dir_bruter,args=(extensions,))
            t.start()
