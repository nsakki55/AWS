 # coding: utf-8
from flask import Flask,request
from decorator import requires_auth
import os
import re
import urllib

app = Flask(__name__)

@app.route("/")
def hello():
    print('AMAZON')
    return 'AMAZON\n'


@app.route("/secret/")
# decoratorを通す
@requires_auth
def basic():
    print('SUCCESS')
    return "SUCCESS\n"

@app.route("/calc")
def calc():
# 数式部分 math を取得
    base_url=str(request.base_url)
    total_url=str(request.url)
    
    total_url=urllib.unquote(total_url)
    print(base_url)
    print(total_url)
    
    base_length=len(base_url)+1
    math=total_url[base_length:]

# 文字列の数式を計算する関数calculateを作成

    ZERO = ord("0")
    NINE = ord("9")

    def paren(st):
        if st[0] == "(":
            ans, idx = first(st[1:])
            return ans, idx+2
        
        elif ZERO <= ord(st[0]) <= NINE:
            i = 1
            while i < len(st) and ZERO <= ord(st[i]) <= NINE:
                i += 1
            return int(st[:i]), i
        return 0, 0

    def second(st):
        ans, idx = paren(st)

        i = idx
        while i < len(st):
            if st[i] == "*":
                tmp, idx = paren(st[i+1:])
                ans *= tmp
                i += idx+1
            elif st[i] == "/":
                tmp, idx = paren(st[i+1:])
                ans /= tmp
                i += idx+1
            else:
                return ans, i
        return ans, i

    def first(st):
        ans, idx = second(st)

        i = idx
        while i < len(st):
            if st[i] == "+":
                tmp, idx = second(st[i+1:])
                ans += tmp
                i += idx+1
            elif st[i] == "-":
                tmp, idx = second(st[i+1:])
                ans -= tmp
                i += idx+1
            else:
                return ans, i
        return ans, i

# 関係ない文字列が入力されている場合はERRORとする
# first,second で (),*,/,+,-の順番に計算を行う
    def calculate(s):
        if s.count("(") != s.count(")") or re.search("[^\+\-\*\/()0-9]", s):
            return "ERROR"
        else:
            return first(s)[0]
    print(math)
    result=calculate(math)
    print(result)
   
    return  str(result)+"\n"
    

if __name__ == "__main__":
    app.run()
