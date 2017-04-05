#!/usr/bin/env python3
# -*- coding : utf-8 -*-

from bd_tran_api import BdTranClient

import re

ONCE_OPT_PATTERN = re.compile('^\s*>\s*([a-z]+)(\s*,\s*(?P<to_lang>[a-z]+))?\s*')
OPT_PATTERN = re.compile('^\s*((?P<get>get)|(?P<set>set))\s+(?P<key>\w+)\s*(?(set)=\s*(?P<value>\w+)\s*)$')

if __name__ == '__main__':
    from util import load_config
    config = load_config()

    APPID = config['APPID']
    SECRET_KEY = config['SECRET_KEY']
    
    client = BdTranClient(APPID, SECRET_KEY)
    print('Start trans from %s to %s:' %(client.get_option('from_lang'),\
            client.get_option('to_lang'))\
         )
    
    options = {}
    while True:
        in_str = input('>>> ')
        
        #match 'get <key>' or 'set <key> = <value>'
        m = OPT_PATTERN.match(in_str)
        if m:
            try:
                if m.group('get'):
                    if m.group('key') == 'status':
                        for k,v in client.options.items():
                            print('%s=%s' %(k, v))
                    else:
                        print('%s=%s' %(m.group('key'), client.get_option(m.group('key'))))
                elif m.group('set'):
                    client.update_option(m.group('key'), m.group('value'))
            except Exception as e:
                print(e)
            continue
        
        in_str = in_str.strip()
        
        #specific from_lang and to_lang for translate_call once.
        m = ONCE_OPT_PATTERN.search(in_str)
        if m: 
            if m.group('to_lang'):
                options['from_lang'] = m.group(1)
                options['to_lang'] = m.group('to_lang')
            elif m.group(1):
                options['from_lang'] = 'auto'
                options['to_lang'] = m.group(1)
            
            in_str = in_str[m.end():]
        
                
            
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
        
        
        dst = client.trans(in_str, **options)
        if options: options.clear()
        
        print(dst)
        
    