#!/usr/bin/python
#Filename : log_filter.py

import re

def __warning_log_filter(log_file, warning_log_list, proj_name):
    has_warning = 0
    first_warning = 1

    # Reopen the log file
    f_log = open(log_file, 'r')

    for line in f_log:
        if re.search(r'warning', line, re.I) != None :
            if re.search(r'Total number', line) == None :
                if first_warning :
                    first_warning = 0
                    warning_log_list.append(proj_name + ' build passed with warnings\n')
                    has_warning = 1
                warning_log_list.append('    >> ' + line)
    
    f_log.close()
    return has_warning
        

# Get error msg
def __error_log_filter(log_file, error_log_list):
    # Reopen the log file
    f_log = open(log_file, 'r')
    for line in f_log:
        if line.find('Error') != -1:
            error_log_list.append('    >> ' + line)
    f_log.close()