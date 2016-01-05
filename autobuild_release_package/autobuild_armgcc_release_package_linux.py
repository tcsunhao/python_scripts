#!/ usr / bin / python
#Filename : autobuild_armgcc_release_package.py
#command line example:
# python autobuild_armgcc_release_package.py debug
# python autobuild_armgcc_release_package.py release

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
            # Get the project name from the cmakelist
            f_cmakelist = open(filename_path,'r')
            for line in f_cmakelist:
                if re.search(r'TARGET_LINK_LIBRARIES',line):
                    search_obj = re.search(r'.*elf', line)
                    if search_obj:
                        proj_name = search_obj.group().split('(')[-1].split('.')[0]
                        print proj_name
                    break
            f_cmakelist.close()    
            
            dirname_path = ('/').join(filename_path.split('/')[0:-1])
            os.chdir(dirname_path)

            sh_file_path = dirname_path + '/build_%s.sh' % (sys.argv[1])
            # the release bat file need to add "build_log.txt"
            if sys.argv[1] == 'release':
                f_sh = open(sh_file_path,'r')
                file_content = f_sh.read()
                if file_content.find('build_log.txt') == -1:
                    file_content = file_content.strip('\n') + ' ' + '2> build_log.txt'
                f_sh.close()
                f_sh = open(sh_file_path,'w')
                f_sh.write(file_content)
                f_sh.close()
                
            print proj_name + ' ' + 'build start: ' 
            sys.stdout.flush()
            
            p = subprocess.Popen(['bash', sh_file_path], stdin=None, stdout=None, stderr=None)
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

log_member = (armgcc_pass_number, armgcc_warning_number, armgcc_fail_number, pass_project_list, warning_log_list, error_log_list, )

# Create log file
path_log_file = rootdir + '/armgcc_build_log.txt'
f_final_log = open(path_log_file,'w')

__output_log(log_member, f_final_log)

f_final_log.close()

print 78*'*'
print 78*'*'
print "Please refer the %s for the build log " % path_log_file