#!/usr/bin/python
# -*- coding: UTF-8 -*-

##题目：有四个数字：1、2、3、4，能组成多少个互不相同且无重复数字的三位数？各是多少？

for a in range(1,5):
    for b in range(1,5):
        for c in range(1,5):
            if a != b and b != c and a != c:
                print a,b,c


##使用列表append
d = []
for a in range(1,5):
    for b in range(1,5):
        for c in range(1,5):
            if a != b and b != c and a != c:
                d.append((a,b,c))
print("数量",len(d))
print d

