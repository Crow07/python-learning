def testfunction():
    print("func1")
testfunction()

def testfunction1():
    return("func2")
print(testfunction1())

def testfunction2(a,b):
    print("a+b = %d" %(a+b))
testfunction2(3,4)

def testfunction3(a,b):
    return(a+b)
print testfunction3(3,4)

def ask_ok(hint,retries=4,complaint="yes or no ,please"):   #参数可以传递默认值
    while True:
        u = input(hint)
        if u in ('y','yes'):
            return True
        if u in ('n','no'):
            return False
        retries = retries - 1
        if retries <=0:
            raise IOError('refuse user')  #
        print(complaint)
result1 = ask_ok("y")
print result1
