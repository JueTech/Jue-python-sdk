#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser
from http import http

class auth():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.oauth = self.config.get("jue", "api_oauth")

    def get_auth(self):
        requestd = http()
        query = {
            "grant_type": "client_credentials",
            "client_id": self.config.get("jue", "access_key"),
            "client_secret": self.config.get("jue", "access_secret"),
        }
        text = requestd.RawRequest(action=self.config.get("jue", "api_oauth")+"ClientCredentials", method="POST", query=query)
        print(text)

if __name__ == "__main__":
    jue_auth = auth()
    jue_auth.get_auth()

