#!/usr/bin/env python
# -*- coding: utf-8 -*-
#http://search.maven.org/remotecontent?filepath=org/python/jython-standalone/2.7-b1/jython-standalone-2.7-b1.jar
from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator

from java.util import List, ArrayList

import random


class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
  def registerExtenderCallbacks(self, callbacks):
    self._callbacks = callbacks
    self._helpers = callbacks.getHelpers()

    callbacks.registerIntruderPayloadGeneratorFactory(self)

    return

  def getGeneratorName(self):
    return "BHP Payload Generator"

  def createNewInstance(self, attack):
    return BHPFuzzer(self, attack)

class BHPFuzzer(IIntruderPayloadGenerator):
  def __init__(self, extender, attack):
    self._extender = extender
    self._helpers  = extender._helpers
    self._attack   = attack
    print "BHP Fuzzer initialized"
    self.max_payloads = 1000
    self.num_payloads = 0

    return


  def hasMorePayloads(self):
    print "hasMorePayloads called."
    if self.num_payloads == self.max_payloads:
      print "No more payloads."
      return False
    else:
      print "More payloads. Continuing."
      return True


  def getNextPayload(self,current_payload):

    # 文字列に変換する
    payload = "".join(chr(x) for x in current_payload)

    # POSTメソッドによるファジングを行う関数を呼び出す
    payload = self.mutate_payload(payload)

    # ファジングの回数のカウンターをインクリメントする
    self.num_payloads += 1

    return payload

  def reset(self):

    self.num_payloads = 0

    return

  def mutate_payload(self,original_payload):

    # ファジングの方法をひとつ選ぶ、もしくは外部スクリプトを呼び出す
    picker = random.randint(1,3)

    # ペイロードからランダムな箇所を選ぶ
    offset  = random.randint(0,len(original_payload)-1)
    payload = original_payload[:offset]

    # 先ほど選んだ箇所でSQLインジェクションを試す
    if picker == 1:
      payload += "'"

    # クロスサイトスクリプティングの脆弱性がないか試す
    if picker == 2:
      payload += "<script>alert('BHP!');</script>";

    # オリジナルのペイロードのランダムな箇所で、選択した部分を繰り返す
    if picker == 3:

      chunk_length = random.randint(len(payload[offset:]),len(payload)-1)
      repeater     = random.randint(1,10)

      for i in range(repeater):
        payload += original_payload[offset:offset+chunk_length]

    # 残りの部分を追加する
    payload += original_payload[offset:]

    return payload
