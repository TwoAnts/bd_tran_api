#!/usr/bin/env python3
# -*- coding : utf-8 -*-

from bd_tran_api import BdTranClient

if __name__ == '__main__':
    from util import load_config
    config = load_config()

    APPID = config['APPID']
    SECRET_KEY = config['SECRET_KEY']
    
    client = BdTranClient(APPID, SECRET_KEY)
    print('Start trans from %s to %s:' %(client.get_option('from_lang'),\
            client.get_option('to_lang'))\
         )
         
    while True:
        in_str = input('>>>')
        if in_str in ('exit', 'quit'): break
        
        dst = client.trans(in_str)
        print(dst)
        
    