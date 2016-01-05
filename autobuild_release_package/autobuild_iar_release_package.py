#!/usr/bin/python
#Filename : autobuild_iar_release_package.py
#command line example:
#   python autobuild_iar_release_package.py Debug 
#   python autobuild_iar_release_package.py Release 

import re,os,sys,time,subprocess
from log_filter import __warning_log_filter, __error_log_filter, __output_log

# rootdir = r"E:\tmp\rc1\SDK_2.0_FRDM-K66F_all2\boards\frdmk66f"
rootdir = r"E:\tmp\rc1\SDK_2.0_FRDM-K66F_all\boards\frdmk66f"

iar_extension_name = '\\*.ewp'

iar_pass_number = 0
iar_warning_number = 0
iar_fail_number = 0

pass_project_list = []
warning_log_list = []
error_log_list = []

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

    iar_tmp_log_path = 'iar_%s_tmp_log.txt' % build_mode
    print iar_tmp_log_path
    f_log = open(iar_tmp_log_path, 'w')
    task = subprocess.Popen([cmd, filename_path, '-make', build_mode, '-log', 'info', '-parallel', '4'], 0, stdin=f_log, stdout=f_log, stderr=f_log, shell=True)
    ret = task.wait()
    f_log.close()

    # Get project name from file path
    proj_name = filename_path.split('\\')[-1]
        
    # If the project build failed
    if ret != 0 :
        iar_fail_number += 1
        error_log_list.append(proj_name + ' build failed\n')
        __error_log_filter(iar_tmp_log_path, error_log_list)
        print 78*'X'
        print filename + ' ' + 'build failed' + '\n'
    # If the project build passed, find the warnings
    else : 
        has_warning = __warning_log_filter(iar_tmp_log_path, warning_log_list, proj_name)
        if has_warning == 1:
            iar_warning_number += 1
            print 78*'W'
            print filename + ' ' + 'build pass with warnings' + '\n'
        else:
            iar_pass_number += 1
            print filename + ' ' + 'build pass without warnings' + '\n'
            pass_project_list.append(proj_name + '\n')
        
    os.remove(iar_tmp_log_path)


iar_bin_path = __search_iar()

# Start the program
for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        filename_path = os.path.join(parent,filename)
        iar_path = __search_iar()
        if re.search(r'\.ewp',filename_path):
            _run_command(iar_bin_path, filename_path, sys.argv[1])

log_member = (iar_pass_number, iar_warning_number, iar_fail_number, pass_project_list, warning_log_list, error_log_list, )

# Create log file
path_log_file = rootdir + '\\iar_%s_build_log.txt' % sys.argv[1]
f_final_log = open(path_log_file,'w')

__output_log(log_member, f_final_log)

f_final_log.close()

print 78*'*'
print 78*'*'
print "Please refer the %s for the build log " % path_log_file
 