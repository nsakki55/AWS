BBbase_url="http://54.199.147.29/:80/"
total_url="http://54.199.147.29/:80/calc?abc"

calc=["+","-","*","/","(",")"]
nums=[str(i) for i in range(0,10)]

base_url=base_url.decode()
total_url=total_url.decode()
print(list(base_url))
print(list(total_url))

base_url=base_url.encode()
total_url=total_url.encode()

print(list(base_url))
print(list(total_url))

base_length=len(base_url)+5

math=total_url[base_length:]

import os
import re

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

def calc(s):
    if s.count("(") != s.count(")") or re.search("[^\+\-\*\/()0-9]", s):
        return "ERROR"
    else:
        return first(s)[0]   

print(calc(math))
