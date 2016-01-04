#!/usr/bin/python
#Filename : autobuild_iar.py
#command line example:
#   python autobuild_iar.py Debug 

import re,os,sys,time,subprocess
from log_filter import __warning_log_filter, __error_log_filter

# rootdir = r"E:\tmp\rc1\SDK_2.0_FRDM-K66F_all2\boards\frdmk66f"
rootdir = r"E:\tmp\rc1\SDK_2.0_FRDM-K66F_all\boards\frdmk66f"

iar_extension_name = '\\*.ewp'

iar_pass_number = 0
iar_fail_number = 0
iar_warning_number = 0

pass_project_list = []
error_log_list = []
warning_log_list = []



# Find iarBuild.exe path in system
def __search_iar():
    try:
        workbenchPath = os.environ['IAR_WORKBENCH']
    except KeyError:
        raise RuntimeError("IAR_WORKBENCH environment variable is not set.")
    else:
        iarBuildPath = os.path.normpath(os.path.join(workbenchPath, "common", "bin", "IarBuild.exe"))

        if not os.path.isfile(iarBuildPath):
            raise RuntimeError("IarBuild.exe does not exist at: {}".format(iarBuildPath))

        return iarBuildPath

def _run_command(cmd, filename_path, build_mode):
    global iar_pass_number
    global iar_fail_number
    global iar_warning_number
    global has_warning
    global first_warning

    print '%s %s -make %s -log info -parallel 4' % (cmd, filename_path, build_mode)
    sys.stdout.flush()

    f_log = open('tmp_log.txt', 'w')
    task = subprocess.Popen([cmd, filename_path, '-make', build_mode, '-log', 'info', '-parallel', '4'], 0, stdin=f_log, stdout=f_log, stderr=f_log, shell=True)
    ret = task.wait()
    f_log.close()

    # Get project name from file path
    proj_name = filename_path.split('\\')[-1]
        
    # If the project build failed
    if ret != 0 :
        iar_fail_number += 1
        error_log_list.append(proj_name + ' build failed\n')
        __error_log_filter('tmp_log.txt', error_log_list)
    # If the project build passed, find the warnings
    else : 
        has_warning = __warning_log_filter('tmp_log.txt', warning_log_list, proj_name)
        if has_warning == 1:
            iar_warning_number += 1
            print filename + ' ' + 'build pass with warnings' + '\n'
        else:
            iar_pass_number += 1
            print filename + ' ' + 'build pass without warnings' + '\n'
            pass_project_list.append(proj_name + '\n')
        
    os.remove('tmp_log.txt')

# Create log file
path_log_file = rootdir + '\\iar_build_log.txt'
f_final_log = open(path_log_file,'w')

iar_workbench_path = __search_iar()

# Start the program
for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        filename_path = os.path.join(parent,filename)
        iar_path = __search_iar()
        if re.search(r'\.ewp',filename_path):
            _run_command(iar_workbench_path, filename_path, sys.argv[1])

print 30*'*' + 'BUILD RESULT' + 30*'*'
print >> f_final_log, 30*'*' + 'BUILD RESULT' + 30*'*'
print '%s' %(iar_pass_number) + ' projects build passed without warning:\n'
print >> f_final_log, '%s' %(iar_pass_number) + ' projects build passed without warning:\n'
print '%s' %(iar_warning_number) + ' projects build passed with warning:\n'
print >> f_final_log,'%s' %(iar_warning_number) + ' projects build passed with warning:\n'
print '%s' %(iar_fail_number) + ' projects build failed\n'
print >> f_final_log, '%s' %(iar_fail_number) + ' projects build failed\n'

if iar_pass_number != 0:
    print 'The passed projects without warning are :'
    print >> f_final_log, 'The passed projects without warning are :'
    for mem in pass_project_list:
        print '  ' + mem,
        print >> f_final_log, '  ' + mem,

print >> f_final_log, '\n'
print >> f_final_log, 68*'*'

if iar_warning_number != 0 :
    print '\n'
    print 'The warning log is :' 
    print >> f_final_log, 'The warning log is :' 
    for mem in warning_log_list:
        print '  ' + mem,
        print >> f_final_log, '  ' + mem,

print >> f_final_log, '\n'
print >> f_final_log, 68*'*'

if iar_fail_number != 0 :
    print '\n'
    print 'The error log is :' 
    print >> f_final_log, 'The error log is :' 
    for mem in error_log_list:
        print '  ' + mem,
        print >> f_final_log, '  ' + mem,
 
f_final_log.close()
print 78*'*'
print 78*'*'
print "Please refer the C:\\iar_build_log_file\\final_log.txt for the build log"
 