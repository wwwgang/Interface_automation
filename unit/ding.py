import time
import hmac
import hashlib
import base64
from urllib.parse import quote_plus
import json
import requests


def getsign():
    timestamp = round(time.time() * 1000)
    secret = 'SEC7663fb83e3bbaa067d1b97dee93893d3f3414ff1fb25cb5f5e3012d862bb0e4b'
    secret_enc = bytes(secret, encoding='utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = bytes(string_to_sign, encoding='utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = quote_plus(base64.b64encode(hmac_code))
    return {'timestamp': timestamp, 'sign': sign}


def sendmessage(message, **kwargs):
    timestamp = kwargs.get('timestamp')
    sign = kwargs.get('sign')
    url = 'https://oapi.dingtalk.com/robot/send?access_token' \
          '=976f344b12655ab5751742a28967f99c1183780eaed3332089c22ae86b7c5959&timestamp={}&sign={}'.format(
        timestamp, sign)
    # data = json.dumps({"msgtype": "text", "text": {"content": message}})
    data = json.dumps(
        {
            "msgtype": "markdown",
            "markdown": {
                "title": "测试报告",
                "text": message,
                # "text": "#### 杭州天气 @156xxxx8827\n" +
                #         "> 9度，西北风1级，空气良89，相对温度73%\n\n" +
                #         "> ![screenshot](https://gw.alicdn.com/tfs/TB1ut3xxbsrBKNjSZFpXXcXhFXa-846-786.png)\n" +
                #         "> ###### 10点20分发布 [天气](http://www.thinkpage.cn/) \n"
            },
            "at": {
                "atMobiles": [
                ],
                "isAtAll": True
            }
        }
    )
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url=url, data=data, headers=headers)
    raw = r.text
    return raw