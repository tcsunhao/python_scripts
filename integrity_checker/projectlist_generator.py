#!/usr/bin/python
#Filename : projectlist_generator.py
#command line examples:
#   python projectlist_generator.py -d MK64F12 -c MK64FN1M0VDC12 
#   python projectlist_generator.py -d MK50D10 -c MK50DN512CLL10 
#   python projectlist_generator.py -d MK50D10 -c MK50DX256CLK10 
#   python projectlist_generator.py -d MKS22F12 -c MKS22FN128VLL12
#   python projectlist_generator.py -d MKW22D5

import os, sys, re, argparse, yaml
import xlsxwriter

from ksdk_checker.get_featurelist import __get_featurelist
from ksdk_checker.transfer_features2drivers import __transfer_features2drivers
from ksdk_checker.transfer_drivers2examples_demos import __transfer_drivers2examples_demos
from ksdk_checker.transfer_features2usb_examples import __transfer_features2usb_examples
from ksdk_checker.output_excel import __output_excel

def __read_options():
    # Build arg parser.
    parser = argparse.ArgumentParser(
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description='Build projects')

    # Options
    parser.add_argument('-d', '--device', help='The device name, such as MK64F12')
    parser.add_argument('-c', '--chipmodule', default=None, help='The chipmodule, such as MK64FN1M0VDC12')

    return parser.parse_args()


if __name__ == '__main__':
        
    soc_feature_dic = {}
    driver_list = []
    driver_exmaples_list = []
    rtos_examples_list = []
    demo_apps_list = []
    usb_examples_list = []

    # Gets the arg
    the_args = __read_options()

    # Gets the feature file path for parsing
    projectlist_generator_path = os.getcwd().replace('\\', '/')
    feature_file_path  = '/'.join(projectlist_generator_path.split('/')[0:-3]) + '/devices/' + the_args.device + '/' + the_args.device + '_%s'%'features.h'
    
    # Gets the feature list for the chip module
    soc_feature_dic = __get_featurelist(feature_file_path, the_args)

    # Gets the usb_examples_list from the soc_feature_dic
    map_features2usb_examples_yml_path = './maps/map_features2usb_examples.yml'
    usb_examples_list = __transfer_features2usb_examples(map_features2usb_examples_yml_path, soc_feature_dic)
    usb_examples_list.sort()

    # Gets the driver_list from the soc_feature_dic
    map_features2drivers_yml_path = './maps/map_features2drivers.yml'
    driver_list = __transfer_features2drivers(map_features2drivers_yml_path, soc_feature_dic)
    driver_list.sort()

    # Gets the driver_exmaples_list from the driver_list
    driver_examples_yml_path = './maps/map_drivers2driver_examples.yml'
    driver_exmaples_list = __transfer_drivers2examples_demos(driver_examples_yml_path,driver_list)    
    driver_exmaples_list.sort()    

    # Gets the rtos_examples_list from the driver_list 
    rtos_example_yml_path = './maps/map_drivers2rtos_examples.yml'
    rtos_examples_list = __transfer_drivers2examples_demos(rtos_example_yml_path,driver_list)
    rtos_examples_list.sort()

    # Gets the demo_apps_list from the driver_list
    demo_apps_yml_path = './maps/map_drivers2demo_apps.yml'
    demo_apps_list = __transfer_drivers2examples_demos(demo_apps_yml_path, driver_list)
    demo_apps_list.sort()
    
    # Removes the 'mcg', 'mcglite', the two are just for getting the driver_list
    for mem in driver_list:
        if mem=='mcg' or mem=='mcglite':
            driver_list.remove(mem)
        else:
            pass
    
    # Create the excel files
    if the_args.chipmodule != None:
        excel_path = '%s_checklist.xlsx' % the_args.chipmodule
    else:
        excel_path = '%s_checklist.xlsx' % the_args.device

    content_lists = (driver_list, driver_exmaples_list, rtos_examples_list, demo_apps_list, usb_examples_list)
    __output_excel(excel_path, content_lists)