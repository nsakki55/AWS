 # coding: utf-8
from flask import Flask,request
from decorator import requires_auth
import os
import re
import urllib
import json

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

@app.route("/stocker")
def stock():
    stock_path="/var/www/flask/data/stock.json"
    function=request.args.get("function")
    print(function)
# functionの値で分ける
    if function=="deleteall":
# 保存先ファイルを削除
        if os.path.exists(stock_path):
            print("delete")
            os.remove(stock_path)
        return ""
       
    elif function=="addstock":
        name=request.args.get("name")
       # name=str(name.decode())
        amount=request.args.get("amount")
        print(amount)
        print(type(amount))
        amount=float(amount)
        print(amount)
        if amount==None:
            amount=1
        
        if amount<0 or not amount.is_integer():
            return "ERROR\n"
        amount=int(amount)
# 保存先ファイルがない場合は新規作成            
        if not os.path.exists(stock_path):
            print("no exists")
            with open(stock_path,'w') as f:
                data_dict={name:amount}
                json.dump(data_dict,f)
                f.close()
            return ""
# 既にファイルがある場合
        else:
            print("exists")
            with open(stock_path,'r+') as f:
                data_update=json.load(f)
                f.close()

            print("before:",data_update)
# nameが既にある場合
            if name in data_update:
                data_update[name]=int(data_update[name])
                data_update[name]+=amount
# nameがない場合
            else:
                data_update[name]=amount
            print("after:",data_update)
# 更新して保存
            with open(stock_path,'w',) as uf:
                json.dump(data_update,uf)
                uf.close()
            return ""
# 売る操作   
    elif function=="sell":
        name=request.args.get("name")

        amount=request.args.get("amount")
        if amount==None:
            amount=1
        amount=int(amount)

        price=request.args.get("price")
        if price==None:
            price=0
        price=float(price)
# データ読み込み
        with open(stock_path,'r+') as f:
            data_update=json.load(f)
            f.close()
        print("before:",data_update)
# nameの数を減らす
        data_update[name]-=amount

# salesが既にある場合
        if "sales" in data_update:
            data_update["sales"]+=amount*price
# ない場合
        else:
            data_update["sales"]=amount*price

        print("after:",data_update)
# 更新して保存
        with open(stock_path,'w',) as uf:
            json.dump(data_update,uf)
            uf.close()
        return ""

# 在庫出力
    elif function=="checkstock":
        name=request.args.get("name")
        with open(stock_path,'r+') as f:
            data_dict=json.load(f)
            f.close()
# name指定された場合
        if name !=None:
            print(name+":",data_dict[name])
            return "{}: {}".format(name,data_dict[name])+'\n'
# 全部表示
        else:
            sort_dict=sorted(data_dict.items(),key=lambda x:x[0])
            top=True
            for n ,count in sort_dict:
                if top:
                    if count !=0:
                        if n !="sales":
                            result='{}: {}'.format(n,count)+'\n'
                            top=False
                else:
                    if count!=0:
                        if n !="sales":
                            tmp='{}: {}'.format(n,count)+'\n'
                            result+=tmp

            return result
# 売上表示   
    elif function=='checksales':
        with open(stock_path,'r+') as f:
            data_dict=json.load(f)
            f.close()
        sale_amount=data_dict["sales"]
# 整数の場合
        if sale_amount.is_integer():
            return  "sales: {}".format(int(sale_amount))+'\n'
# 少数の場合
        else:
            return "sales: {0:.2f}".format(data_dict["sales"])+'\n'


if __name__ == "__main__":
    app.run()
