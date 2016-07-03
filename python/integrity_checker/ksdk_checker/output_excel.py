#!/usr/bin/python
#Filename : __output_excel.py

import os, sys, re, argparse, yaml
import xlsxwriter

def __output_excel(excel_path, content_lists):
    col_names = ('driver_list', 'driver_exmaples_list', 'rtos_examples_list', 'demo_apps_list', 'usb_examples_list')
    
    workbook = xlsxwriter.Workbook(excel_path)
    worksheet = workbook.add_worksheet('check_list')

    # The xlsx cell format 
    top = workbook.add_format({'border':1,'align':'left','bg_color':'cccccc','font_size':13,'bold':True})
    green = workbook.add_format({'border':1,'align':'left','bg_color':'green','font_size':12})
    
    worksheet.set_column('A:E', 32)

    k = 0
    while k<len(content_lists):
        worksheet.write(0, k, col_names[k], top)
        i = 1 
        while i<=len(content_lists[k]):
            worksheet.write(i, k, content_lists[k][i-1], green)
            i = i + 1

        k = k + 1
    workbook.close()