#!/ usr / bin / python
#Filename : autobuild_keil_release_package.py
#command line example:
# python autobuild_keil_release_package.py Debug
# python autobuild_keil_release_package.py Release

import re,os,sys,time,subprocess
from log_filter import __warning_log_filter, __error_log_filter, __output_log

rootdir = r"E:\tmp\rc1\SDK_2.0_FRDM-K66F_all\boards\frdmk66f"

keil_extension_name = '\\*.uvprojx'

pass_project_list = []
warning_log_list = []
error_log_list = []

keil_pass_number = 0
keil_warning_number = 0
keil_fail_number = 0

def __search_keil():
    try:
        workbenchPath = os.environ['KEIL']
    except KeyError:
        raise RuntimeError("KEIL environment variable is not set.")
    else:
        keilBuildPath = os.path.normpath(os.path.join(workbenchPath, "UV4.exe"))

        if not os.path.isfile(keilBuildPath):
            raise RuntimeError("UV4.exe does not exist at: {}".format(keilBuildPath))

        return keilBuildPath

def _run_command(cmd, proj_name):
    global keil_pass_number
    global keil_warning_number
    global keil_fail_number

    keil_tmp_log_path = '\\keil_%s_tmp_log.txt' % sys.argv[1]

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
        __warning_log_filter(rootdir + keil_tmp_log_path, warning_log_list, proj_name)
    else:
        print 78*'X'
        print proj_name + " build failed.\n"
        keil_fail_number += 1
        error_log_list.append(proj_name + ' build failed\n')
        __error_log_filter(rootdir + keil_tmp_log_path, error_log_list)

    os.remove(rootdir + keil_tmp_log_path)

for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        filename_path = os.path.join(parent,filename)
        if re.search(r'uvprojx',filename_path):
            proj_name = filename_path.split('\\')[-1].split('.')[0]
            keil_bin_path = __search_keil()
            keil_cmd = '''%s -b %s -o %s\\keil_%s_tmp_log.txt -j0 -t "%s %s"''' %(keil_bin_path, filename_path, rootdir,sys.argv[1],proj_name, sys.argv[1])
            print keil_cmd
            sys.stdout.flush()
            _run_command(keil_cmd, proj_name)


log_member = (keil_pass_number, keil_warning_number, keil_fail_number, pass_project_list, warning_log_list, error_log_list, )

# Create log file
path_log_file = rootdir + '\\keil_%s_build_log.txt' % sys.argv[1]
f_final_log = open(path_log_file,'w')

__output_log(log_member, f_final_log)

f_final_log.close()

print 78*'*'
print 78*'*'
print "Please refer the %s for the build log " % path_log_file