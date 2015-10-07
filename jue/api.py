#! /bin/python
# -*- coding: utf-8 -*-

import configparser, json, hashlib, sys, logging, auth
from http import http
from memory import memory

__package__     = "Jue-php-sdk/request"
__author__      = "homeway"
__version__     = "2015.10.07"
__copyright__   =  "Copyright(c) 2015"
__link__        = "https://github.com/JueTech/Jue-python-sdk"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='jue-python-sdk.log',
    filemode='w'
)

__author__ = 'homeway'
__version__ = '2015.10.07'

class api(object):
    def __init__(self, access_token):
        self.access_token = access_token
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.memory = memory(cache_name="secret")

    def secret_portal(self, uid, cfrom="cloud.jue.so", token=""):
        query = {
            "access_token": self.access_token,
            "client_id": self.config.get("jue", "access_key"),
            "client_secret": self.config.get("jue", "access_secret"),
            "uid":  uid,
            "from": cfrom,
            "token": token or hashlib.md5(".").hexdigest()
        }
        response = http().RawRequest(action=self.config.get("jue", "api_resource")+"secret/portal", method="POST", query=query)
        if response["status_code"] == 200:
            try:
                user_info = json.loads(response["text"])
                self.memory.set("userinfo", user_info["data"])
            except:
                pass
            return user_info["data"] or response["text"]
        else:
            pass

    def cloud_add_app_file(self, **file_info):
        query = {
            "access_token": self.access_token,
        }

        for k in file_info.keys():
            query[k] = file_info[k]

        response = http().RawRequest(action=self.config.get("jue", "api_resource")+"callback/add_app_file", method="POST", query=query)
        if response["status_code"] == 200:
            return response["text"]
        else:
            pass

    def get_upload_token(self, uuid, parent=""):
        query = {
            "access_token": self.access_token,
            "client_id": self.config.get("jue", "access_key"),
            "client_secret": self.config.get("jue", "access_secret"),
            "uuid": uuid,
            "parent": parent
        }
        response = http().RawRequest(action=self.config.get("jue", "api_resource")+"cloud/get_upload_token", method="POST", query=query)
        return self.result(response)

    def result(self, response):
        if response["status_code"] == 200:
            try:
                data = json.loads(response["text"])
            except:
                #response not json, maybe error
                logging.info("response json encode except: %s" % response["text"])
            return data or response["text"]
        else:
            #request error
            logging.error("response error: %s" % json.dumps(response))
        return None
    
