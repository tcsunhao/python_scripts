#!/ usr / bin / python
#Filename : autobuild_iar.py
#command line example:
#   python autobuild_iar.py make Debug 

import re,os,sys,time,subprocess


iar_extension_name = '\\*.ewp'

# rootdir = "C:\\Users\\b55235\\Desktop\\SDK_2.0_MAPS-KS22_all_preRC2\\examples\\mapsks22\\usb"
rootdir = "C:\\Users\\b55235\\Desktop\\SDK_2.0_MAPS-KS22_all_preRC2\\examples\\mapsks22\\usb"
# rootdir = "E:\\git_sdk_2.0_ks22_rel\\mcu-sdk-2.0\\boards\\mapsks22\\driver_examples"

iar_pass_number = 0
iar_fail_number = 0
iar_warning_number = 0

pass_project_list = []
error_log_list = []
warning_log_list = []

has_warning = 0;
first_warning = 1;

def _run_command(cmd, filename):
    global iar_pass_number
    global iar_fail_number
    global iar_warning_number
    global has_warning
    global first_warning
    f_log = open('C:\\iar_build_log_file\\tmp_log.txt', 'w')
    task = subprocess.Popen(cmd, 0, stdin=f_log, stdout=f_log, stderr=f_log, shell=True)
    ret = task.wait()
    f_log.close()

    f_log = open('C:\\iar_build_log_file\\tmp_log.txt', 'r')
    
    if ret != 0 :
        # print 'Fail to build the project..'
        # print cmd.split('\\')[-1]
        iar_fail_number += 1
        error_log_list.append(filename + ' build failed\n')
        print '\n'
        for line in f_log:
            if line.find('Error') != -1:
                error_log_list.append('    >> ' + line)
        f_log.close()
    else :
        first_warning = 1;
        for line in f_log:
            if line.find('warning:') != -1:
                has_warning = 1;
                if first_warning :
                    warning_log_list.append(filename + ' build passed with warnings\n')
                    print '\n'
                    first_warning = 0;
                warning_log_list.append('    >> ' + line)
        if has_warning == 1:
            iar_warning_number += 1
            has_warning = 0;        
            print filename + ' ' + 'build pass with warnings'
            print '\n'
        else:
            iar_pass_number += 1
            print filename + ' ' + 'build pass without warnings'
            print '\n'
        f_log.close()



if os.path.exists("C:\\iar_build_log_file"):
    pass
else :
    os.mkdir("C:\\iar_build_log_file") 

for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        filename_path = os.path.join(parent,filename)
        # iar_project_path = dirname_path + iar_extension_name
        if re.search(r'ewp',filename_path):
            iar_cmd = 'IarBuild.exe %s -%s %s -log info' %(filename_path, sys.argv[1], sys.argv[2])
            print iar_cmd
            sys.stdout.flush()
            _run_command(iar_cmd, filename)

f_final_log = open('C:\\iar_build_log_file\\final_log.txt','w')

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
        print >> f_final_log, '  ' + mem

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
 