#!/usr/bin/env python

# _*_ coding:utf-8 _*_


class China:

    def info(self):

        print("Chinese")


class Us:

    def info(self):

        print("US")


class My(China, Us):

    def info(self):

        print("ME")


c = My()

c.info()