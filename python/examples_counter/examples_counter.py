#!/usr/bin/python
#Filename : examples_counter.py
#command line example:

import re, os, sys, time, subprocess, fnmatch, json, yaml
import  xml.dom.minidom


rootdir = r"E:\git_sdk_2.0_feature_common(generator)\mcu-sdk-2.0\bin\generator\records\ksdk\sdk_example"
rootdir = r"E:\git_sdk_2.0_feature_common(generator)\mcu-sdk-2.0\bin\generator\records\ksdk\usb_example"

project_num = 0

for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        filename_path = parent + '\\' + filename
        print filename_path
        f = file(filename_path)
        yf = yaml.load(f)
        f.close()
        for item in yf.items():
            if item == '__hierarchy__':
                pass
            else:
                project_num += 1

print 'project_num is : %d ' % project_num + '\n'
