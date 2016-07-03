# !/usr/bin/python
# Filename : __transfer_drivers2examples_demos.py

import re, os, sys, time, subprocess, fnmatch, json, yaml

def __transfer_drivers2examples_demos(yml_path, driver_list):

    exmaple_list = []
    
    f = file(yml_path)
    yf = yaml.load(f)
    f.close()
    
    for item in yf.items():
        and_have = 0
        or_have = 0
        for key in item[1].keys():
            if key == 'or':
                or_have = 0
                if item[1][key] != None:
                    drivers = item[1][key].split(' ')
                    if len(drivers) != 0:
                        find_one = 0
                        for mem_drivers in drivers:
                            for mem_driver_list in driver_list:
                                if mem_driver_list == mem_drivers:
                                    find_one = 1
                                    break
                        if find_one == 0:
                            or_have = 0
                            break
                        else:
                            or_have = 1
                else:
                    or_have = 1                    
            if key == 'and':
                and_have = 0
                if item[1][key] != None:
                    drivers = item[1][key].split(' ')
                    if len(drivers) != 0:
                        find_all = 0
                        for mem_drivers in drivers:
                            for mem_driver_list in driver_list:
                                if mem_driver_list == mem_drivers:
                                    find_all = find_all + 1
                        if find_all != len(drivers):
                            and_have = 0
                            break
                        else:
                            and_have = 1
                else:
                    and_have = 1

            if and_have==1 and or_have==1:
                exmaple_list.append(item[0])
    
    return exmaple_list