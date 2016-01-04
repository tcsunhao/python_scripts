#!/ usr / bin / python
#Filename : autobuild_keil.py
#command line example:
# python autobuild_keil.py Debug
# python autobuild_keil.py Release

import re,os,sys,time,subprocess
from log_filter import __warning_log_filter, __error_log_filter, __output_log

rootdir = r"E:\tmp\rc1\SDK_2.0_FRDM-K66F_all1\boards\frdmk66f"

keil_extension_name = '\\*.uvprojx'

pass_project_list = []
warning_log_list = []
error_log_list = []

keil_pass_number = 0
keil_warning_number = 0
keil_fail_number = 0

def _run_command(cmd, proj_name):
    global keil_pass_number
    global keil_warning_number
    global keil_fail_number

    task = subprocess.Popen(cmd, 0, stdin=None, stdout=None, stderr=None,shell = True)
    returncode = task.wait()

    if returncode == 0:    
        print proj_name + " build passed without warnings.\n"
        keil_pass_number += 1
        pass_project_list.append(proj_name + '\n')
    elif returncode == 1:
        print 78*'W'
        print proj_name + " build passed with warnings.\n"
        keil_warning_number += 1
        __warning_log_filter(rootdir + '\\tmp_log.txt', warning_log_list, proj_name)
    else:
        print 78*'X'
        print proj_name + " build failed.\n"
        keil_fail_number += 1
        error_log_list.append(proj_name + ' build failed\n')
        __error_log_filter(rootdir + '\\tmp_log.txt', error_log_list)

    os.remove(rootdir + '\\tmp_log.txt')

for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        filename_path = os.path.join(parent,filename)
        if re.search(r'uvprojx',filename_path):
            proj_name = filename_path.split('\\')[-1].split('.')[0]
            keil_cmd = '''UV4.exe -b %s -o %s\\tmp_log.txt -j0 -t "%s %s"''' %(filename_path, rootdir, proj_name, sys.argv[1])
            print keil_cmd
            sys.stdout.flush()
            _run_command(keil_cmd, proj_name)


log_member = (keil_pass_number, keil_warning_number, keil_fail_number, pass_project_list, warning_log_list, error_log_list, )

# Create log file
path_log_file = rootdir + '\\keil_build_log.txt'
f_final_log = open(path_log_file,'w')

__output_log(log_member, f_final_log)

f_final_log.close()

print 78*'*'
print 78*'*'
print "Please refer the %s for the build log " % path_log_file