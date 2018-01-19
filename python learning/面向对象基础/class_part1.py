#!/usr/bin/python
# -*- encoding:utf-8 -*-
class class_test:    #define a class
    def ret(self):   #define a methond
        print("test")
obj = class_test()
obj.ret()            
class_test.ret(obj)

class class_basic:
    def ret(self,):
        print('方法ret的self内存地址', id(self))

obj_1 = class_basic()
print('obj对象内存地址',id(obj_1))
obj_1.ret()