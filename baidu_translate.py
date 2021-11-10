# -*- coding:utf-8 -*-
import os
import csv
import xlrd
import time
import random
import execjs
import requests
from lxml import etree
from urllib.parse import urlencode

class BaiduTranslateJS(object):
    def __init__(self, query):
        self.query = query
        self.url = 'https://fanyi.baidu.com/v2transapi?from=zh&to=en'
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
            "Connection": "keep-alive",
            "Content-Length": "145",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "PSTM=1611535465; BIDUPSID=5C27039207EA8E479E7F6036C51B6605; __yjs_duid=1_7118f227c7ef52c7ffc3046d669f50a61619600827189; BAIDUID=D70D526D2096C24A6468C31E60517EE1:FG=1; MCITY=-%3A; BDSFRCVID=6ZuOJexroG0ksSQH7ha4u8pp02UGkuJTDYrEOwXPsp3LGJLVgoswEG0PtHuyjd0b_2AUogKKKgOTHICF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tbkD_C-MfIvDqTrP-trf5DCShUFsKfcTB2Q-XPoO3KtaeJj-y-jm0-CJ5Pnb54biWbRM2MbgylRp8P3y0bb2DUA1y4vpKMP8bmTxoUJ25DnJjlCzqfCWMR-ebPRiB-b9QgbA5hQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hD0wD5DMe5PVKgTa54cbb4o2WbCQyfI28pcN2b5oQTOLhPRHBnol0GCLsxnt5n6vOIJM0qOUWJDkXpJvQnJjt2JxaqRC5M56Hl5jDh3MQ5bX5-cCe4ROLKby0hvcWb3cShnVLUjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDNtDt60jfn3aQ5rtKRTffjrnhPF3XbkzXP6-hnjy3b4DQb8KWpjVf4jGeb32D5DUyN3MWh3RymJ42-39LPO2hpRjyxv4bUn-5toxJpOJ5JbMBqCEHlFWj43vbURvyP-g3-7A3M5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoK0hJC-2bKvPKITD-tFO5eT22-usJ55W2hcHMPoosItlKP--yM_bjUrtqnOjtnriaKJjBMbUoqRHXnJi0btQDPvxBf7p5208Ll5TtUJMeCnTMxFVqfTbMlJyKMniWKv9-pnY0hQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuDjA-e5QWDa_s5JtXKD600PK8Kb7VbIQL5fnkbJkXhPtjabJgLm-fBnD2bCn2qKt43fJO5fI7QbrH0xRfyNReQIO13hcdSR3vKnJpQT8r5-7th4TbtIrdoqjGab3vOpvTXpO1yftzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-FtqtJHKbDqoIIhtf2; BDSFRCVID_BFESS=6ZuOJexroG0ksSQH7ha4u8pp02UGkuJTDYrEOwXPsp3LGJLVgoswEG0PtHuyjd0b_2AUogKKKgOTHICF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tbkD_C-MfIvDqTrP-trf5DCShUFsKfcTB2Q-XPoO3KtaeJj-y-jm0-CJ5Pnb54biWbRM2MbgylRp8P3y0bb2DUA1y4vpKMP8bmTxoUJ25DnJjlCzqfCWMR-ebPRiB-b9QgbA5hQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hD0wD5DMe5PVKgTa54cbb4o2WbCQyfI28pcN2b5oQTOLhPRHBnol0GCLsxnt5n6vOIJM0qOUWJDkXpJvQnJjt2JxaqRC5M56Hl5jDh3MQ5bX5-cCe4ROLKby0hvcWb3cShnVLUjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDNtDt60jfn3aQ5rtKRTffjrnhPF3XbkzXP6-hnjy3b4DQb8KWpjVf4jGeb32D5DUyN3MWh3RymJ42-39LPO2hpRjyxv4bUn-5toxJpOJ5JbMBqCEHlFWj43vbURvyP-g3-7A3M5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoK0hJC-2bKvPKITD-tFO5eT22-usJ55W2hcHMPoosItlKP--yM_bjUrtqnOjtnriaKJjBMbUoqRHXnJi0btQDPvxBf7p5208Ll5TtUJMeCnTMxFVqfTbMlJyKMniWKv9-pnY0hQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuDjA-e5QWDa_s5JtXKD600PK8Kb7VbIQL5fnkbJkXhPtjabJgLm-fBnD2bCn2qKt43fJO5fI7QbrH0xRfyNReQIO13hcdSR3vKnJpQT8r5-7th4TbtIrdoqjGab3vOpvTXpO1yftzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-FtqtJHKbDqoIIhtf2; H_PS_PSSID=31660_26350; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; delPer=0; PSINO=5; BAIDUID_BFESS=78AE2FB5134CBE8BF7A688C684BF47AB:FG=1; BDRCVFR[tiixOo0cjw_]=mk3SLVN4HKm; BA_HECTOR=8h0l850k8gag0025041gokcc40q; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1636444281,1636447956; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1636447956; ab_sr=1.0.1_NTY3MzRlZjkzZGVlMDk5MjViMTE1NTgwM2Y1MGIyMGQ4Y2VkZTk3NmMxZTM0MDkwZjRkMzY0ZjJjMmE0MTcwMGQzOTYxYTdlNzI2ZWJmNzE5MzU3ZDFiNTlmZjUxNmExMWJhNTI3YzBjNjFmMmM5NmIxN2Q0MmRjZTk4ZDM5MDQyMGJkZDMxOTQ3ZDUzYWMxY2Q5MGI0OThlYmVhZDI4Ng==; __yjs_st=2_NjM1NTNjYmY4NmQyZTgzNDIxOTY5YjNkNTViMmFjOTE3Y2Y3YWE4ZmNhZGU1ZGM2ZWUyNzUyMzdkZTFiNTgzMWRmYjAyYzEyNzhlZWJkNGIzY2UzZmE0ZjMzZjk5YWZmYmZkMWEwY2MxMWRhNjNhMmJhMmZmNTEyNjdlNmFkYzhlMjEzMDg5MGEwZTM2ZTVjNTI1YjkxZTg5Mzk3MTQ3MjY1MzE0NzU5NDcyOGJhNjQ2MmNjNDhkY2FmMGNlZjJmNGM1OGQ1Y2FkZGNmZDMwNGM3YmUwOGZkNWFjZGZkOTdlYWE5ZDJhYTY4MGY4ODE2OTk5MTFiYTQ1OGIwNjRhNV83XzQ3NzgzYjZl",
            "Host": "fanyi.baidu.com",
            "Origin": "https://fanyi.baidu.com",
            "Referer": "https://fanyi.baidu.com/?aldtype=16047",
            "sec-ch-ua": "\"Google Chrome\";v=\"95\", \"Chromium\";v=\"95\", \";Not A Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.data = {
            "from": "en", # 从英文
            "to": "zh",   # 转换为中文
            "query": self.query,
            "transtype": "commen",
            "simple_means_flag": 3,
            "sign": "",
            "token": "ac822c2e9b7254e3ac14d97d4cd13950",
            "domain": "common"
        }

    def structure_form(self):
        with open("./js.txt", "r", encoding="utf-8") as f:
            ctx = execjs.compile(f.read())
        sign = ctx.call("e", self.query)
        self.data['sign'] = sign

    def get_response(self):
        self.structure_form()
        response = requests.post(self.url, headers = self.headers, data= self.data, timeout= (21, 21)).json()
        r = response['trans_result']['data'][0]['dst']
        return r

if __name__ == "__main__":
    baidu_translate_spider = BaiduTranslateJS("this is a test")
    result = baidu_translate_spider.get_response()
    print(result)
    print(BaiduTranslateJS("love").get_response())
    print(BaiduTranslateJS("tomhanks").get_response())