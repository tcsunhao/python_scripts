# !/usr/bin/python
# Filename : load.py

import re,os,sys,time,subprocess,fnmatch,json

f = file('default_config.json');
s = json.load(f)
f.close()

for key in s.keys():
    print s.get(key,'')
