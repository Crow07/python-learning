'''
f = file('class1.txt','r')
for line in f.readlines():
    line = line.strip('\n').split(':')
    print line
'''

f = file('class1.txt','a')
f = f.write('test2222')
