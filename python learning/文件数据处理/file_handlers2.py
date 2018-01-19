#_*_coding:utf-8_*_
from collections import OrderedDict

from pyexcel_xls import get_data
from pyexcel_xls import save_data


def read_xls_file():
    inpath = '.\你好.xlsx'
    #uipath = unicode(inpath, "utf8")
    xls_data = get_data(unicode(inpath,'utf-8'))
    Compute_name = '计算节点'
    uCompute_name = unicode(Compute_name,'utf-8')
    for i in  xls_data[uCompute_name]:
        print i
    for sheet_n in xls_data.keys():
        print sheet_n, ":", xls_data[sheet_n][2][3]


if __name__ == '__main__':
    read_xls_file()
