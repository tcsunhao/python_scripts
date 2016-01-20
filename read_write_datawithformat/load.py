# !/usr/bin/python
# Filename : load.py

import re, os, sys, time, subprocess, fnmatch, json, yaml

############################
## The typical way to load a json file
# f = file('default_config.json');
# s = json.load(f)
# f.close()

# for key in s.keys():
#     print s.get(key,'')


############################
## The typical way to load yaml file
# feature = {'FSL_FEATURE_SOC_CMP_COUNT': True,
#            'FSL_FEATURE_SOC_EMVSIM_COUNT':True,
#            'FSL_FEATURE_SOC_XBAR_COUNT':2}

# driver_module_list = []
# example_driver_dic = {}

# ## Input the yml
# f = file('demo_app.yml')
# yf = yaml.load(f)

# for item in yf.items():
#     tmp_driver_module_list = item[1]['modules'].keys()
#     if len(tmp_driver_module_list) != 0:
#         for mem in tmp_driver_module_list:
#             if (mem=='pinset' or mem=='clock' or mem=='demo' or mem=='example' 
#                 or mem=='demo' or mem==('fsl_'+item[0]) or mem=='port' or mem=='uart' or mem=='mcglite'
#                 or mem=='lpuart' or mem=='lpsci' or mem=='gpio' or mem=='sim' or mem=='osc' or mem=='mcg'):
#                 pass
#             else:
#                 driver_module_list.append(mem)
#     example_driver_dic[item[0]] = driver_module_list
#     driver_module_list = []

# items = example_driver_dic.items()
# items.sort()

f = file('all_usb.yml','r')
yf = yaml.load(f)
f.close()

proj_list = []
raw_proj_list = yf['__load__']

for mem in raw_proj_list:
    proj_list.append(mem.split('\\')[-1].split('.')[0])

proj_list.sort()

f = open('map_features2usb_examples.yml','w')

for mem in proj_list:
    print >> f, mem + ':'
    print >> f, '    and:'
    print >> f, '\n',

f.close()

#### Output the yml
# f = file('newdata.yaml','w')
# yaml.dump(example_driver_dic,f)
# f.close()

###############################
### read and write excel

# import xlsxwriter

# workbook = xlsxwriter.Workbook('zm6.xlsx')
# worksheet = workbook.add_worksheet('sheet No.1')
# worksheet.write(0, 0, 'hello world')
# workbook.close()