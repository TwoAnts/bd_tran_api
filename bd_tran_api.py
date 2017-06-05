#!/usr/bin/env python3
# -*- coding : utf-8 -*-

import http.client
import traceback
import json
import hashlib
import urllib.parse
import random
import logging

logging.basicConfig(level=logging.INFO)

LANG_SET = set(('auto', 'zh', 'en', 'yue', 'wyw', 'jp', 'kor',
    'fra', 'spa', 'th', 'ara', 'ru', 'pt', 'de', 'it', 'el', 'nl',
    'pl', 'bul', 'est', 'dan', 'fin', 'cs', 'rom', 'slo', 'swe',
    'hu', 'cht', 'vie'))

QP_SET = set(('from_lang', 'to_lang'))

TRAN_SITE = 'api.fanyi.baidu.com'
TRAN_URL = '/api/trans/vip/translate'

class BdTranClient:
    LANG_SET = LANG_SET
    def __init__(self, appid, secret_key, **kwargs):
        self.url = TRAN_URL
        self.appid = appid
        self.secret_key = secret_key
        self.options = {'from_lang':'en', 'to_lang':'zh'}
        for key in QP_SET:
            if key in kwargs: self.options[key] = kwargs[key]
        self.client = None
        self.init_client()
        
    def update_option(self, key, value):
        if key not in QP_SET:
            raise ValueError('Unsupport option: %s' %key, 'in BdTranClient')
        if key in ('from_lang', 'to_lang') and value not in LANG_SET:
            raise ValueError('Unsupport language: %s' %value, 'in BdTranClient')
        
        self.options[key] = value
        
    def get_option(self, key):
        return self.options.get(key)
        
    def __get_opt__(self, key, default=None, opts=None):
        if key not in QP_SET:
            raise ValueError('Unsupport option: %s' %key, 'in BdTranClient')
            
        if opts and key in opts:
            return opts[key]
        
        return self.options.get(key, default)
        
    def init_client(self):
        if self.client: self.client.close()
        self.client = http.client.HTTPConnection(TRAN_SITE)
        
    def close(self):
        if self.client:
            self.client.close()
            self.client = None
        
    def trans(self, content, **kwargs):
        q = content
        from_lang = self.__get_opt__('from_lang', opts=kwargs)
        to_lang = self.__get_opt__('to_lang', opts=kwargs)
        if from_lang not in LANG_SET or to_lang not in LANG_SET:
            raise ValueError('Unsupport language: %s->%s' %(from_lang, to_lang), 'in BdTranClient')
            
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
            except http.client.CannotSendRequest as e:
                logging.info(e)
                if except_msg is None: except_msg = []
                except_msg.append(traceback.format_exc())
                #Here should getresponse for previous request
                self.init_client()
            except Exception as e:
                logging.debug(e)
                if except_msg is None: except_msg = []
                except_msg.append(traceback.format_exc())
                self.client.close()
        
        print('Try %s times, but failed.\n%s' %(try_times, '\n'.join(except_msg)))
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
        
        
        
        
