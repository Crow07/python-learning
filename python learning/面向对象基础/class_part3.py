#!/usr/bin/python
# -*- encoding:utf-8 -*-
class People:
    def __init__(self):
        print("""
        People test""")
class Chinese(People):            #类继承
    def info(self):
        print ("""
        Chinese""")
class Asian(People):
    def info(self):
        print ("""
        Asian
        """)

m = Chinese()
m.info()

n = Asian()
n.info()
