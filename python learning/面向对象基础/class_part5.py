#!/usr/bin/env python

# _*_ coding:utf-8 _*_


class China:

    pass


class Us:

    def info(self):

        print("US")


class My(China, Us):

    pass


c = My()

c.info()