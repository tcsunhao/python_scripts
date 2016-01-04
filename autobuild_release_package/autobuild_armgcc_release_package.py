#!/ usr / bin / python
#Filename : autobuild_armgcc.py
#command line example:
# python autobuild_armgcc.py debug
# python autobuild_armgcc.py release

import re,os,sys,time,subprocess

error_log_list = []
pass_project_list = []
warning_log_list = []

# rootdir = r"E:\git_sdk_2.0_feature_common\mcu-sdk-2.0\boards\frdmk64f\usb_examples\usb_device_audio_generator"
rootdir = r"E:\tmp\rc1\SDK_2.0_FRDM-K66F_all2\boards\frdmk66f"

armgcc_pass_number = 0
armgcc_warning_number = 0
armgcc_fail_number = 0

has_warning = 0;
first_warning = 1;

if os.path.exists("C:\\armgcc_build_log_file"):
    pass
else :
    os.mkdir("C:\\armgcc_build_log_file") 

for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        filename_path = os.path.join(parent,filename)
        if re.search(r'CMakeLists',filename_path):
            # print filename_path
            proj_name = filename_path.split('\\')[-4] + '_' + filename_path.split('\\')[-3]           
            dirname_path = ('\\').join(filename_path.split('\\')[0:-1])
            os.chdir(dirname_path)
            # print dirname_path
            bat_file_path = dirname_path + '\\build_%s.bat' % (sys.argv[1])
            newbat_file_path = dirname_path + '\\newbuild_%s.bat' % (sys.argv[1])
            sh_file_path = dirname_path + '\\build_%s.sh' % (sys.argv[1])
            f_bat = open(bat_file_path,'r')
            f_newbat = open(newbat_file_path,'w')
            
            f_bat_data = f_bat.readlines()
            for line in f_bat_data:
                if 'pause' in line:
                    continue
                f_newbat.write(line)

            f_bat.close()
            f_newbat.close()

            print proj_name + ' ' + 'build start: ' 
            sys.stdout.flush()
            p = subprocess.Popen('newbuild_%s.bat' % sys.argv[1], stdin=None, stdout=None, stderr=None)
            returncode = p.wait()
            log_file_path = dirname_path + '\\build_log.txt'
            f_log = open(log_file_path,'r')
            if returncode != 0:
                armgcc_fail_number += 1
                print proj_name + ' ' + 'build failed\n'
                print '\n'
                sys.stdout.flush()
                error_log_list.append(proj_name + ' build failed\n')
                for line in f_log:
                    if line.find('error:') != -1:
                        error_log_list.append('    >> ' + line)
                        # error_log_list.append('\n')
                f_log.close()
            else : 
                first_warning = 1;
                for line in f_log:
                    if line.find('warning:') != -1:
                        has_warning = 1;
                        if first_warning :
                            warning_log_list.append(proj_name + ' build passed with warnings\n')
                            first_warning = 0;
                        warning_log_list.append('    >> ' + line)

                if has_warning == 1:
                    armgcc_warning_number += 1
                    has_warning = 0;        
                    print proj_name + ' ' + 'build pass with warnings'
                else:
                    armgcc_pass_number += 1
                    print proj_name + ' ' + 'build pass without warnings'
                f_log.close()
                

            os.remove(newbat_file_path)

f_final_log = open('C:\\armgcc_build_log_file\\final_log.txt','w')

print 30*'*' + 'BUILD RESULT' + 30*'*'
print >> f_final_log, 30*'*' + 'BUILD RESULT' + 30*'*'
print '%s' %(armgcc_pass_number) + ' projects build passed without warning:\n'
print >> f_final_log, '%s' %(armgcc_pass_number) + ' projects build passed without warning:\n'
print '%s' %(armgcc_warning_number) + ' projects build passed with warning:\n'
print >> f_final_log,'%s' %(armgcc_warning_number) + ' projects build passed with warning:\n'
print '%s' %(armgcc_fail_number) + ' projects build failed\n'
print >> f_final_log, '%s' %(armgcc_fail_number) + ' projects build failed\n'

if armgcc_pass_number != 0:
    print 'The passed projects without warning are :'
    print >> f_final_log, 'The passed projects without warning are :'
    for mem in pass_project_list:
        print '  ' + mem,
        print >> f_final_log, '  ' + mem

print >> f_final_log, '\n'
print >> f_final_log, 68*'*'

if armgcc_warning_number != 0 :
    print '\n'
    print 'The warning log is :' 
    print >> f_final_log, 'The warning log is :' 
    for mem in warning_log_list:
        print '  ' + mem,
        print >> f_final_log, '  ' + mem,

print >> f_final_log, '\n'
print >> f_final_log, 68*'*'

if armgcc_fail_number != 0 :
    print '\n'
    print 'The error log is :' 
    print >> f_final_log, 'The error log is :' 
    for mem in error_log_list:
        print '  ' + mem,
        print >> f_final_log, '  ' + mem,
 
f_final_log.close()
print 78*'*'
print 78*'*'
print "Please refer the C:\\armgcc_build_log_file\\final_log.txt for the build log"