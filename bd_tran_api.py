#!/usr/bin/env python3
# -*- coding : utf-8 -*-

import http.client
import traceback
import json
import hashlib
import urllib.parse
import random

QP_SET = set(['from_lang', 'to_lang'])

TRAN_SITE = 'api.fanyi.baidu.com'
TRAN_URL = '/api/trans/vip/translate'

APPID = '20170302000040187'
SECRET_KEY = 'qM5ZHlRVQX84tBkzBW3n'

class BdTranClient:
    def __init__(self, appid, secret_key, **kwargs):
        self.url = TRAN_URL
        self.appid = appid
        self.secret_key = secret_key
        self.options = {'from_lang':'en', 'to_lang':'zh'}
        for key in QP_SET:
            if key in kwargs: self.options[key] = kwargs[key]
        self.client = http.client.HTTPConnection(TRAN_SITE)
        
    def update_option(self, key, value):
        if key not in QP_SET:
            raise ValueError('Unsupport option: %s' %key, 'in BdTranClient')
        
        self.options[key] = value
        
    def get_option(self, key):
        return self.options.get(key)
        
    def __get_opt__(self, key, default=None, opts=None):
        if key not in QP_SET:
            raise ValueError('Unsupport option: %s' %key, 'in BdTranClient')
            
        if opts and key in opts:
            return opts[key]
        
        return self.options.get(key, default)
        
    def close(self):
        self.client.close()
        
    def trans(self, content, **kwargs):
        q = content
        from_lang = self.__get_opt__('from_lang', opts=kwargs)
        to_lang = self.__get_opt__('to_lang', opts=kwargs)
        salt = random.randint(32768, 65536)
        
        sign = self.appid+q+str(salt)+self.secret_key
        sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
        
        url = self.url+'?appid='+self.appid+'&q='+urllib.parse.quote(q)\
                +'&from='+from_lang+'&to='+to_lang\
                +'&salt='+str(salt)+'&sign='+sign
        print('%s %s %s' %(q, from_lang, to_lang))
            
        try:
            self.client.request('GET', url)
            response = self.client.getresponse()
            resp = json.loads(response.read())
            trans_result = resp['trans_result'][0]
            return trans_result['dst']
           
        except Exception as e:
            print(traceback.format_exc())
            return None
        
if __name__ == '__main__':
    tran_client = BdTranClient(APPID, SECRET_KEY, from_lang='jp')
    dst = tran_client.trans(u'笑顔')
    print(dst)
    tran_client.close()
        
        
        
        