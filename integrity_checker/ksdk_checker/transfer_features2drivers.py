#!/usr/bin/python
#Filename : transfer_features2drivers.py

import os, sys, re, argparse, yaml


def __transfer_features2drivers(yml_path, soc_feature_dic):
    
    driver_list = []
    
    # Loads the map_feature2driver.yml for getting the driver list
    f = file(yml_path)
    yf = yaml.load(f)
    f.close()

    for item in yf.items():
        if item[0] == 'flash':
            driver_list.append('flash')
        elif item[0] == 'wdog':
            if soc_feature_dic.has_key('FSL_FEATURE_SOC_WDOG_COUNT'):
                if soc_feature_dic.has_key('FSL_FEATURE_WDOG_HAS_32BIT_ACCESS'):
                    if soc_feature_dic['FSL_FEATURE_WDOG_HAS_32BIT_ACCESS'] == 'true':
                        driver_list.append('wdog32')
                else:
                    driver_list.append('wdog')
            else:
                pass
        elif item[0] == 'wdog32':
            pass
        elif item[0] == 'rtc':
            if soc_feature_dic.has_key('FSL_FEATURE_SOC_RTC_COUNT'):
                if soc_feature_dic.has_key('FSL_FEATURE_RTC_IS_IRTC'):
                    if soc_feature_dic['FSL_FEATURE_RTC_IS_IRTC'] == 'true':
                        driver_list.append('irtc')
                else:
                    driver_list.append('rtc')
            else:
                pass
        elif item[0] == 'irtc':
            pass    
        elif item[0] == 'tsi_v2':
            if soc_feature_dic.has_key('FSL_FEATURE_SOC_TSI_COUNT'):
                if soc_feature_dic['FSL_FEATURE_TSI_VERSION'] == '2':
                        driver_list.append('tsi_v2')
                elif soc_feature_dic['FSL_FEATURE_TSI_VERSION'] == '4':
                    driver_list.append('tsi_v4')
                else:
                    pass
            else:
                pass
        elif item[0] == 'tsi_v4':
            pass                    
        else:
            key = item[1].keys()[0]
            if key == 'and':
                has_driver = 1
                for keymem in item[1].values()[0].keys():
                    if soc_feature_dic.has_key(keymem) == False:
                        has_driver = 0
                        break
                if has_driver == 1:
                    driver_list.append(item[0])
            elif key == 'or':
                has_driver = 0
                for keymem in item[1].values()[0].keys():
                    if soc_feature_dic.has_key(keymem) == True:
                        has_driver = 1
                        break
                if has_driver == 1:
                    driver_list.append(item[0])
    
    return driver_list