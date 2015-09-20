#! /bin/python
# -*- coding: utf-8 -*-

import os, json, time, hashlib

class memory():
    def __init__(self, cache_path=None, cache_name=None, cache_extension="cache", expired=3600):
        extension = cache_extension.lstrip(".") or "cache"
        self.extension = "." + extension

        self.expired = expired
        self.cache_name = cache_name or hashlib.md5(".").hexdigest()
        self.cache_path = cache_path or os.path.abspath("./cache")

    def __get_cache(self):
        path = self.cache_path+"/"+self.cache_name+self.extension
        try:
            fp = open(path, "r+")
            data = fp.read()
            return (fp, data)
        except IOError as e:
            print("Open file error : %s" % e)

    def __set_cache(self, data):
        path = self.cache_path+"/"+self.cache_name+self.extension
        fp = open(path, "w+")
        fp.write(data)

    def store(self, key, value, expired=None):
        expired = expired or self.expired
        store_value = {
            "time": time.time(),
            "expired": expired,
            "data": value
        }

        store_data = {
            "key": key,
            "value": store_value
        }

        fp, data = self.__get_cache()
        m = json.dumps(store_data)
        self.__set_cache(m.strip(""))


if __name__ == "__main__":
    memory = memory(cache_extension=".cache")
    memory.store("key", "value")
