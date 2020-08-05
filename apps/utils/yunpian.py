# -*- coding: utf-8 -*-
"""
@author = 'ethan'
"""

import json
import requests


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.singel_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_msg(self, code, mobile):
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "您的验证码是{code}".format(code),

        }

        response = requests.post(self.singel_send_url, data=parmas)

        re_dict = json.loads(response.text)