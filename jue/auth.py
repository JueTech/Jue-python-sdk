#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser, json
from http import http
from memory import memory

__package__     = "Jue-php-sdk/request"
__author__      = "homeway"
__version__     = "2015.10.07"
__copyright__   =  "Copyright(c) 2015"
__link__        = "https://github.com/JueTech/Jue-python-sdk"

class auth(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.oauth = self.config.get("jue", "api_oauth")

        self.memory = memory(cache_name="auth")

    def get_auth(self, grant_type="client_credentials"):
        if grant_type == "client_credentials":
            return self.client_credentials()
        elif grant_type == "password":
            return self.password()
        else:
            pass

    def password(self):
        query = {
            "grant_type": "password",
            "username": self.config.get("jue", "username"),
            "password": self.config.get("jue", "password"),
            "client_id": self.config.get("jue", "access_key"),
            "client_secret": self.config.get("jue", "access_secret"),
        }
        response = http().RawRequest(action=self.config.get("jue", "api_oauth")+"PasswordCredentials", method="POST", query=query)
        if response["status_code"] == 200:
            try:
                self.memory.set(key="auth", value=response["text"])
                self.access_token = json.loads(response["text"])["access_token"]
            except:
                pass
            return response["text"]
        else:
            pass

    def client_credentials(self):
        query = {
            "grant_type": "client_credentials",
            "client_id": self.config.get("jue", "access_key"),
            "client_secret": self.config.get("jue", "access_secret"),
        }
        response = http().RawRequest(action=self.config.get("jue", "api_oauth")+"ClientCredentials", method="POST", query=query)
        if response["status_code"] == 200:
            try:
                self.memory.set(key="auth", value=response["text"])
                self.access_token = json.loads(response["text"])["access_token"]
            except:
                pass
            return response["text"]
        else:
            pass

if __name__ == "__main__":
    jue_auth = auth()
    print(jue_auth.get_auth("client_credentials"))

