#!/usr/bin/python
#Filename : log_filter.py

import re,sys

def __warning_log_filter(log_file, warning_log_list, proj_name):
    has_warning = 0
    first_warning = 1

    # Reopen the log file
    f_log = open(log_file, 'r')

    for line in f_log:
        if re.search(r'warning', line, re.I) != None :
            if re.search(r'Total number', line) == None and re.search(r'warning,', line) == None and re.search(r'CMake Warning', line) == None: 
                if line.find('ignored') != -1:
                    pass
                else:
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
        if line.find('Error')!=-1 or line.find('error:')!=-1:
            if line.find('ignored') != -1: #kds
                pass 
            else:
                error_log_list.append('    >> ' + line)
    f_log.close()

def __output_log(log_member, f_log):
    print 30*'*' + 'BUILD RESULT' + 30*'*'
    print >> f_log, 30*'*' + 'BUILD RESULT' + 30*'*'
    print '%s' %(log_member[0]) + ' projects build passed without warning:\n'
    print >> f_log, '%s' %(log_member[0]) + ' projects build passed without warning:\n'
    print '%s' %(log_member[1]) + ' projects build passed with warning:\n'
    print >> f_log,'%s' %(log_member[1]) + ' projects build passed with warning:\n'
    print '%s' %(log_member[2]) + ' projects build failed\n'
    print >> f_log, '%s' %(log_member[2]) + ' projects build failed\n'
    
    sys.stdout.flush()

    if log_member[0] != 0:
        print 'The passed projects without warning are :'
        print >> f_log, 'The passed projects without warning are :'
        for mem in log_member[3]:
            print '  ' + mem,
            print >> f_log, '  ' + mem,

    print >> f_log, '\n'
    print >> f_log, 68*'*'

    if log_member[1] != 0 :
        print '\n'
        print 'The warning log is :' 
        print >> f_log, 'The warning log is :' 
        for mem in log_member[4]:
            print '  ' + mem,
            print >> f_log, '  ' + mem,

    print >> f_log, '\n'
    print >> f_log, 68*'*'

    if log_member[2] != 0 :
        print '\n'
        print 'The error log is :' 
        print >> f_log, 'The error log is :' 
        for mem in log_member[5]:
            print '  ' + mem,
            print >> f_log, '  ' + mem,