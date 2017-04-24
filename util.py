#!/usr/bin/env python3
# -*- coding : utf-8 -*-

import os
CONFIG_FILE = 'config.txt'
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
CF_PATH = os.path.join(CUR_DIR, CONFIG_FILE)

#You need a baidu translate <appid> and <secret_key> 
#config.txt -> 
#APPID = xxxxxxx
#SECRET_KEY = xxxxxx

def load_config(fn=CF_PATH):
    config = {}
    
    with open(fn, 'r', encoding='utf-8') as f:
        for line in f:
            #allow some notes in config file.
            ignore = line.find('#')
            if ignore >= 0: line = line[:ignore]
            
            kv = line.split('=', 1)
            if len(kv) != 2: continue
            k, v = kv[0].strip(), kv[1].strip()
            config[k] = v
            
    return config
    
if __name__ == '__main__':
    config = load_config()
    print(config['APPID'], config['SECRET_KEY'])