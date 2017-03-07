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
        #print('%s %s %s' %(q, from_lang, to_lang))
        

        try_times = 0
        except_msg = None
        while try_times < 3:
            try_times += 1
            try:
                self.client.request('GET', url)
                response = self.client.getresponse()
                resp = json.loads(response.read().decode('utf-8'))
                r = []
                for tr in resp['trans_result']:
                    r.append(tr['dst'])
                return ','.join(r)
            except Exception as e:
                except_msg = traceback.format_exc()
        
        print('Try %s times, but failed.\n%s' %(try_times, except_msg))
        return None
        
if __name__ == '__main__':
    from util import load_config
    
    config = load_config()
    APPID = config['APPID']
    SECRET_KEY = config['SECRET_KEY']
    
    tran_client = BdTranClient(APPID, SECRET_KEY, from_lang='jp')
    dst = tran_client.trans(u'笑顔')
    print(dst)
    tran_client.close()
        
        
        
        
