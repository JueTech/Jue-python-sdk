#! /bin/python
# -*- coding: utf-8 -*-

import requests, configparser

__package__     = "Jue-php-sdk/request"
__author__      = "homeway"
__version__     = "2015.09.20"
__copyright__   =  "Copyright(c) 2015"
__link__        = "https://github.com/JueTech/Jue-python-sdk"

class http():
    def __init__(self):
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'api.jue.so',
            'Referer': 'http://api.jue.so/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
        }
        self.cookies = {
            'appver': '1.5.2',
            }
        self.default_timeout = 1

    def RawResponse(self, status_code, header, text, cookies=None):
        return text

    def RawRequest(self, action, method, query=None, files=None, urlencoded=None, callback=None, timeout=None, cookies=None):
        if (method == "GET"):
            url = action if (query == None) else (action + '?' + query)
            connection = requests.get(url, headers=self.header, timeout=self.default_timeout, cookies=cookies)
        elif (method == "POST"):
            connection = requests.post(
                action,
                data=query,
                files=files,
                headers=self.header,
                timeout=timeout,
                cookies=self.cookies,
            )
        connection.encoding = "UTF-8"
        res = connection
        return self.RawResponse(res.status_code, res.headers, res.text, res.cookies)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    requestd = http()

    query = {
        "grant_type": "client_credentials",
        "client_id": config.get("jue", "access_key"),
        "client_secret": config.get("jue", "access_secret"),
        }
    text = requestd.RawRequest(action=config.get("jue", "api_oauth")+"ClientCredentials", method="POST", query=query)
    print(text)
