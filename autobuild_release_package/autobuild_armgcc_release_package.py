#!/ usr / bin / python
#Filename : autobuild_armgcc.py
#command line example:
# python autobuild_armgcc.py debug
# python autobuild_armgcc.py release

import re,os,sys,time,subprocess
from log_filter import __warning_log_filter, __error_log_filter, __output_log

rootdir = r"E:\tmp\rc1\SDK_2.0_FRDM-K66F_all\boards\frdmk66f"

error_log_list = []
pass_project_list = []
warning_log_list = []

armgcc_pass_number = 0
armgcc_warning_number = 0
armgcc_fail_number = 0

for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        filename_path = os.path.join(parent,filename)
        if re.search(r'CMakeLists',filename_path):
            proj_name = filename_path.split('\\')[-3]           
            # print proj_name
            dirname_path = ('\\').join(filename_path.split('\\')[0:-1])
            os.chdir(dirname_path)

            bat_file_path = dirname_path + '\\build_%s.bat' % (sys.argv[1])
            # Remove the 'pause' in the bat file
            newbat_file_path = dirname_path + '\\newbuild_%s.bat' % (sys.argv[1])
            f_bat = open(bat_file_path,'r')
            f_newbat = open(newbat_file_path,'w')
            f_bat_data = f_bat.readlines()
            for line in f_bat_data:
                if 'pause' in line:
                    continue
                f_newbat.write(line)
            f_bat.close()
            f_newbat.close()

            # the release bat file need to add "build_log.txt"
            if sys.argv[1] == 'release':
                f_newbat = open(newbat_file_path,'r')
                file_content = f_newbat.read()
                if file_content.find('build_log.txt') == -1:
                    file_content = file_content.strip('\n') + ' ' + '2> build_log.txt'
                f_newbat.close()
                f_newbat = open(newbat_file_path,'w')
                f_newbat.write(file_content)
                f_newbat.close()
            
            print proj_name + ' ' + 'build start: ' 
            sys.stdout.flush()
            
            p = subprocess.Popen('newbuild_%s.bat' % sys.argv[1], stdin=None, stdout=None, stderr=None)
            returncode = p.wait()

            if returncode != 0:
                armgcc_fail_number += 1
                error_log_list.append(proj_name + ' build failed\n')
                __error_log_filter('build_log.txt', error_log_list)
                print 78*'X'
                print proj_name + ' ' + 'build failed\n'
                sys.stdout.flush()
            else : 
                has_warning = __warning_log_filter('build_log.txt', warning_log_list, proj_name)
                if has_warning == 1:
                    armgcc_warning_number += 1
                    print 78*'W'
                    print proj_name + ' ' + 'build pass with warnings' + '\n'
                else:
                    armgcc_pass_number += 1
                    print proj_name + ' ' + 'build pass without warnings' + '\n'
                    pass_project_list.append(proj_name + '\n')
                
            # os.remove('build_log.txt')
            os.remove(newbat_file_path)

log_member = (armgcc_pass_number, armgcc_warning_number, armgcc_fail_number, pass_project_list, warning_log_list, error_log_list, )

# Create log file
path_log_file = rootdir + '\\armgcc_build_log.txt'
f_final_log = open(path_log_file,'w')

__output_log(log_member, f_final_log)

f_final_log.close()

print 78*'*'
print 78*'*'
print "Please refer the %s for the build log " % path_log_file