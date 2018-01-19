#!/usr/bin/python
# -*- encoding:utf-8 -*-
class Foo:
    def ret(self):
        print(self.name)  #输出name变量的内容
obj = Foo()               #定义对象
obj.name = "hello"        #在对象中创建name变量
obj.ret()                 #调用对象的ret方法

class Foo_better:
    ## 进入类的时候首先执行__init__方法
    def __init__(self,name):
        """
        __init__称之为构造方法

        :param name: Foo传递过来的参数
        """
        # 在类中创建一个成员Name，它的值是传过来的形参name
        self.Name = name
        # 类的方法
    def ret(self):
        print(self.Name)
obj = Foo_better("hcy")
obj.ret()


###实例

class example:
    def __init__(self,name,age):
        self.Name = name
        self.Age = age
    def info(self):                          #3三单引号和三双引号中间的字符串在输出时保持原来的格式。
        print("""
My name is : %s
        My age is : %d
        """ % (self.Name,self.Age))
hcy = example("hcy",18)
hcy.info()