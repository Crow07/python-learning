# -*- coding:utf-8 -*-
import sys
import os

if len(sys.argv) <=4:
    print "usage: ./file_replace.py old_text new_text file_name"
old_text,new_text = sys.argv[1],sys.argv[2]
file_name = sys.argv[3]
