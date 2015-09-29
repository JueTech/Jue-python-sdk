#! /bin/python
# -*- coding: utf-8 -*-

import os, json, time, hashlib

class memory():
    def __init__(self, cache_path=None, cache_name=None, cache_extension="cache", expired=3600):
        extension = cache_extension.lstrip(".") or "cache"
        self.extension = "." + extension

        self.expired = expired
        self.cache_name = cache_name or hashlib.md5(".").hexdigest()

        if cache_path and os.path.exists(cache_path) == True:
            self.cache_path = cache_path
        else:
            self.cache_path = os.path.abspath("./cache")

    def __get_cache(self):
        path = self.cache_path+"/"+self.cache_name+self.extension
        try:
            fp = open(path, "r+")
            data = fp.read()
            return (fp, data)
        except IOError as e:
            fp = open(path, "w+")
            data = "{}"
            return (fp, data)

    def __set_cache(self, data):
        path = self.cache_path+"/"+self.cache_name+self.extension
        fp = open(path, "w+")
        fp.write(data)

    def get_hash(self):
        return self.cache_name

    def set_exipired(self, expired=3600):
        self.expired = expired or self.expired
        return self.expired

    def set_cache_name(self, name):
        self.cache_name = hashlib.md5(name).hexdigest()
        return self.cache_name

    def get_cache_name(self):
        return self.cache_name

    def set_cache_dir(self, dir):
        if os.path.exists(dir) == True:
            self.cache_path = dir
        return self.cache_path

    def get(self, key):
        fp, data = self.__get_cache()
        data = json.loads(data)
        if data.has_key(key):
            item = data[key]
            if item["time"] + item["expired"] < int(time.time()):
                '''data expired'''
                del data[key]
                self.__set_cache(json.dumps(data))
                return None
            else:
                return item
        return None

    def set(self, key, value, expired=None):
        expired = expired or self.expired
        fp, data = self.__get_cache()

        try:
            data = json.loads(data)
        except:
            data = {}

        store_value = {
            "time": int(time.time()),
            "expired": expired,
            "data": value
        }
        data[key] = store_value
        m = json.dumps(data)
        self.__set_cache(m.strip(""))

if __name__ == "__main__":
    memory = memory(cache_extension=".cache")
    memory.set("key", "value")
    print memory.get("123")
