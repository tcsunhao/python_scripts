# !/usr/bin/python
# Filename : transfer_features2usb_examples.py

import os, sys, re, argparse, yaml

def __transfer_features2usb_examples(yml_path, soc_feature_dic):

    usb_examples_list = []

    # Check whether has the FSL_FEATURE_SOC_USB_COUNT
    has_usb_feature = 0
    for mem in soc_feature_dic:
        if mem == 'FSL_FEATURE_SOC_USB_COUNT':
            has_usb_feature = 1
            break

    if has_usb_feature == 1:
    
        f = file(yml_path)
        yf = yaml.load(f)
        f.close()

        for item in yf.items():
            if item[1] == None:
                usb_examples_list.append(item[0])
            else:
                has_all = 1
                dependlist = item[1].split(' ')
                for mem_dependlist in dependlist:
                    has_this = 0
                    for mem in soc_feature_dic:
                        if mem_dependlist == mem:
                            has_this = 1
                            break
                    if has_this == 0:
                        has_all = 0
                        break
                if has_all == 1:
                    usb_examples_list.append(item[0])

    return usb_examples_list