# !/usr/bin/python
# Filename : load.py

import re, os, sys, time, subprocess, fnmatch, json, yaml

############################
# # The typical way to load a json file
# f = file('default_config.json');
# s = json.load(f)
# f.close()

# for key in s.keys():
#     print s.get(key,'')

############################
# The typical way to load yaml file

feature = {'FSL_FEATURE_SOC_CMP_COUNT': True,
           'FSL_FEATURE_SOC_EMVSIM_COUNT':True,
           'FSL_FEATURE_SOC_XBAR_COUNT':2}

f = file('tmp_project.yml')
yf = yaml.load(f)

for item in yf.items():
    print item[1]['modules'].keys()
# print yf

# for item in yf.items():
#     if item[0] == 'flash':
#         pass
#     else:
#         key = item[1].keys()[0]
#         if key == 'and':
#             for keymem in item[1].values()[0].keys():
#                 # print keymem
#                 if item[1].values()[0][keymem] != True:
#                     print keymem
#                     print item[1].values()[0][keymem]
    # print item[1].values()[0]

