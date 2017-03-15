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
        in_str = input('>>> ')
        
        in_str = in_str.strip()
        #When your sentence has \n, use " or '. 
        if in_str and in_str[0] in ('\'', '\"'):
            quote = in_str[0]
            str_list = [in_str]
            while True:
                in_str = input('>    ')
                in_str = in_str.strip()
                str_list.append(in_str)
                if in_str and in_str[-1] == quote:
                    break
            
            in_str = ' '.join(str_list)[1:-1]
            
        
        if in_str in ('exit', 'quit'): break
        if not in_str: continue 
        
        dst = client.trans(in_str)
        print(dst)
        
    