# README #  
This python script can do translation using Baidu translation API.  
You just need a Baidu \<APPID\> and \<SECRET_KEY\>.  
Python version must be 3.x.

## How to ##  
1. Write your \<APPID\> and \<SECRET_KEY\> to `config.txt`.  
    ```
    #config.txt
    APPID = xxxxxx
    SECRET_KEY = xxxxxxx
    ```
    
2. Just run `python3 translate_cli.py`  
    or write your own script using `BdTranClient`.  

## CLI Usage ##  
- Use set and get for options.  
    `set <key> = <value>` or `get <key>`.
    ```
    >>> set from_lang = jp
    >>> get to_lang
    to_lang=zh
    ```

- Use `> [<from_lang>,]<to_lang> ....` to specific language once.  
    ```
    >>> >en,zh hello
    你好
    >>> >en 你好    #from_lang is auto here.
    Hello,
    ```

- Use ' or " when your sentence has \n.  
    ```
    >>> 'This
    >    sentence
    >    has
    >    \n.'
    这个句子有
    ```
    
- Type `exit` or `quit` to exit.  
    
Just enjoy it! :)
