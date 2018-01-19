#_*_coding:utf-8_*_
f = file('./class1.txt')
for i in f.readlines():
    #print i.strip()
    #print i.strip("\n")
    #print i.split()
    print i.decode("utf-8")
f.close()

fi = file('./class1.txt','a')
fi.write(u'我哈你'.encode('utf-8'))
fi.close()

fi = file('./class1.txt','w')
fi.write(u'你好'.encode('utf-8'))
fi.close()


