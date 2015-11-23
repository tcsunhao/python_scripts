#!/ usr / bin / python
#Filename : autobuild_keil.py
#command line example:
# python autobuild_keil.py b Debug
# python autobuild_keil.py b Release

import re,os,sys,time,subprocess

error_log_list = []
warning_log_list = []

pass_project_list = []

keil_extension_name = '\\*.uvprojx'
rootdir = "E:\\git_sdk_2.0_ks22_rel\\mcu-sdk-2.0\\boards\\mapsks22\\usb"
# rootdir = "E:\\sdk_release\\SDK_2.0_MAPS-KS22_all_RC1_b111115\\examples\\mapsks22\\driver_examples"

keil_pass_number = 0
keil_warning_number = 0
keil_fail_number = 0

def _run_command(cmd, filename):
    global keil_pass_number
    global keil_warning_number
    global keil_fail_number
    # print cmd
    task = subprocess.Popen(cmd, 0, stdin=None, stdout=None, stderr=None,shell = True)
    returncode = task.wait()
    if returncode == 0:    
        print filename + " build passed without warnings.\n"
        keil_pass_number += 1
        pass_project_list.append(filename)
    elif returncode == 1:
        print filename + " build passed with warnings.\n"
        keil_warning_number += 1
        __warning_log_filter(filename)
    else:
        print filename + " build failed"
        print "*"*76
        __error_log_filter(returncode, filename)
        keil_fail_number += 1

# Get warning msg
def __warning_log_filter(filename):
    warning_log_list.append(filename + ' build passed with warning\n')
    # print log
    f = open('C:\\keil_build_log_file\\tmp_log.txt', 'r')
    for line in f:
        if line.find("warning:") != -1:
            warning_log_list.append('    >> ' + line)
    f.close()

# Get error msg
def __error_log_filter(errno, filename):
    # error_log_list = []
    
    error_dict = {
        2:  "Code Error",
        3:  "Fatal Error",
        11: "Cannot open project files for writting",
        12: "Device with given name in not found in database",
        13: "Error writing project file",
        15: "Error reading import XML file"
    }
    error_log_list.append(filename + ' build failed\n')
    error_log_list.append('    >> Error Code (' + str(errno) + ') : ' + error_dict.get(errno, "Other errors") + '\n')
    # print log
    f = open('C:\\keil_build_log_file\\tmp_log.txt', 'r')
    for line in f:
        if line.find("rror:") != -1:
            error_log_list.append('    >> ' + line)
    f.close()
    
    # return "".join(error_log_list)
if os.path.exists("C:\\keil_build_log_file"):
    pass
else :
    os.mkdir("C:\\keil_build_log_file") 

for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        filename_path = os.path.join(parent,filename)
        if re.search(r'uvprojx',filename_path):
            # print filename_path
            proj_name = filename_path.split('\\')[-1].split('.')[0]
            # print proj_name
            keil_cmd = '''UV4.exe -%s %s -o C:\\keil_build_log_file\\tmp_log.txt -j0 -t "%s %s"''' %(sys.argv[1], filename_path, proj_name, sys.argv[2])
            print keil_cmd + '\n'
            sys.stdout.flush()
            _run_command(keil_cmd, filename)



f_final_log = open('C:\\keil_build_log_file\\final_log.txt','w')

print 30*'*' + 'BUILD RESULT' + 30*'*'
print >> f_final_log, 30*'*' + 'BUILD RESULT' + 30*'*'
print '%s' %(keil_pass_number) + ' projects build passed without warning:\n'
print >> f_final_log, '%s' %(keil_pass_number) + ' projects build passed without warning:\n'
print '%s' %(keil_warning_number) + ' projects build passed with warning:\n'
print >> f_final_log,'%s' %(keil_warning_number) + ' projects build passed with warning:\n'
print '%s' %(keil_fail_number) + ' projects build failed\n'
print >> f_final_log, '%s' %(keil_fail_number) + ' projects build failed\n'

if keil_pass_number != 0:
    print 'The passed projects without warning are :'
    print >> f_final_log, 'The passed projects without warning are :'
    for mem in pass_project_list:
        print '  ' + mem,
        print >> f_final_log, '  ' + mem

print >> f_final_log, '\n'
print >> f_final_log, 68*'*'

if keil_warning_number != 0 :
    print 'The warning log is :' 
    print >> f_final_log, 'The warning log is :' 
    for mem in warning_log_list:
        print >> f_final_log, '  ' + mem,
        print '  ' + mem,

print >> f_final_log, '\n'
print >> f_final_log, 68*'*'

if keil_fail_number != 0 :
    print 'The error log is :' 
    print >> f_final_log, 'The error log is :' 
    for mem in error_log_list:
        print >> f_final_log, '  ' + mem,
        print '  ' + mem,
 
 
f_final_log.close()

print 78*'*'
print 78*'*'
print "Please refer the C:\\keil_build_log_file\\final_log.txt for the build log"