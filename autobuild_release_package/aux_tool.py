#!/usr/bin/python
#Filename : aux_tool.py
from __future__ import division
import re, sys, argparse, os

class ProgressBar():
    """docstring for progressbar"""
    def __init__(self, allnum, width=80):
        self.pointer = 0
        self.width = width
        self.allnum = allnum

    def __call__(self, x):
        # x in percent
        self.pointer = int(self.width*(x/self.allnum))
        return "|" + ">"*self.pointer + "-"*(self.width-self.pointer)+\
            "|\n %d percent done" % (x/self.allnum*100) + '\n'

def __warning_log_filter(file_debug_log, file_pass_withwarning, proj_name):
    has_warning = 0
    first_warning = 1

    f_file_pass_withwarning = open(file_pass_withwarning, 'a+')
    f_debug_log = open(file_debug_log, 'r')

    for line in f_debug_log:
        if re.search(r'warning', line, re.I) != None :
            if re.search(r'Total number', line) == None and re.search(r'warning,', line) == None and re.search(r'CMake Warning', line) == None and re.search(r'0 Warning\(s\)', line) == None: 
                if line.find('ignored') != -1:
                    pass
                else:
                    if first_warning :
                        first_warning = 0
                        f_file_pass_withwarning.write(proj_name + ' build passed with warnings\n')
                        has_warning = 1
                    f_file_pass_withwarning.write('    >> ' + line)

    f_file_pass_withwarning.close()
    f_debug_log.close()

    return has_warning
        

# Get error msg
def __error_log_filter(file_debug_log, file_fail, proj_name):
    f_debug_log = open(file_debug_log, 'r')
    f_file_fail = open(file_fail, 'a+')
    first_error = 1

    for line in f_debug_log:
        if line.find('Error')!=-1 or line.find('error:')!=-1:
            if line.find('ignored') != -1: #kds
                pass 
            else:
                if first_error == 1:
                    f_file_fail.write(proj_name + ' ' + 'build failed' + '\n')
                    first_error = 0
                f_file_fail.write('    >> ' + line)
    
    f_debug_log.close()
    f_file_fail.close()

def __read_options():
    # Build arg parser.
    parser = argparse.ArgumentParser(
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description='Build projects')

    # Options
    parser.add_argument('-n', '--buildname', help='The build name. A build name is needed for every build to distinguish itself from others')
    parser.add_argument('-m', '--mode', default=None, help='The build mode, debug, release, all')

    return parser.parse_args()

def __output_log(proj_num_dict, file_pass, file_warning, file_fail, file_log):
    pass_number = 0
    warning_number = 0
    fail_number = 0

    f_log = open(file_log,'w')

    if proj_num_dict.has_key('projectbuild_pass_number'):
        pass_number = proj_num_dict['projectbuild_pass_number']
    else:
        pass_number = 0
    if proj_num_dict.has_key('projectbuild_warning_number'):
        warning_number = proj_num_dict['projectbuild_warning_number']
    else:
        warning_number = 0
    if proj_num_dict.has_key('projectbuild_fail_number'):
        fail_number = proj_num_dict['projectbuild_fail_number']
    else:
        fail_number = 0

    print 30*'*' + 'BUILD RESULT' + 30*'*'
    print >> f_log, 30*'*' + 'BUILD RESULT' + 30*'*'
    print '%s' %(pass_number) + ' projects build passed without warning:\n'
    print >> f_log, '%s' %(pass_number) + ' projects build passed without warning:\n'
    print '%s' %(warning_number) + ' projects build passed with warning:\n'
    print >> f_log,'%s' %(warning_number) + ' projects build passed with warning:\n'
    print '%s' %(fail_number) + ' projects build failed\n'
    print >> f_log, '%s' %(fail_number) + ' projects build failed\n'
    
    sys.stdout.flush()

    if pass_number != 0:
        print 'The passed projects without warning are :'
        print >> f_log, 'The passed projects without warning are :'
        f_file_pass = open(file_pass, 'r')
        for line in f_file_pass.readlines():
            print '  ' + line,
            print >> f_log, '  ' + line,
        f_file_pass.close()

    print >> f_log, '\n'
    print >> f_log, 68*'*'

    sys.stdout.flush()

    if warning_number != 0:
        print 'The warning logs are :'
        print >> f_log, 'The warning logs are :'
        f_file_warning = open(file_warning, 'r')
        for line in f_file_warning.readlines():
            print '  ' + line,
            print >> f_log, '  ' + line,
        f_file_warning.close()

    print >> f_log, '\n'
    print >> f_log, 68*'*'
    
    sys.stdout.flush()
    
    if fail_number != 0:
        print 'The failed logs are :'
        print >> f_log, 'The failed logs are :'
        f_file_fail = open(file_fail, 'r')
        for line in f_file_fail.readlines():
            print '  ' + line,
            print >> f_log, '  ' + line,
        f_file_fail.close()

    f_log.close()