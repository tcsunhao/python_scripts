#!/usr/bin/python
#Filename : autobuild_armgcc.py
#command line example:
# python autobuild_armgcc.py debug
# python autobuild_armgcc.py release

import re,os,sys,time,subprocess

error_log_list = []
pass_project_list = []
warning_log_list = []

rootdir = r"/home/mcu-sw/Downloads/"

armgcc_pass_number = 0
armgcc_warning_number = 0
armgcc_fail_number = 0

has_warning = 0;
first_warning = 1;

current_dir = os.getcwd()
if os.path.exists(current_dir+r'/armgcc_build_log_file'):
    pass
else :
    os.mkdir(current_dir+r'/armgcc_build_log_file')

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
                        # print proj_name
                    break
            f_cmakelist.close() 
          
            dirname_path = ('/').join(filename_path.split('/')[0:-1])
            os.chdir(dirname_path)
            #print dirname_path
            sh_file_path = dirname_path + '/build_%s.sh' % (sys.argv[1])
            newsh_file_path = dirname_path + '/newbuild_%s.sh' % (sys.argv[1])
            # the release sh file need to add "build_log.txt"
            if sys.argv[1] == 'release':
                f_sh = open(sh_file_path,'r')
                file_content = f_sh.read()
                if file_content.find('build_log.txt') == -1:
                    file_content = file_content.strip('\n') + ' ' + '2> build_log.txt'
                f_sh.close()
                f_sh = open(newsh_file_path,'w')
                f_sh.write(file_content)
                f_sh.close()
            print proj_name + ' ' + 'build start: ' 
            sys.stdout.flush()
            log_file_path = dirname_path + '/build_log.txt'
            f_log = open(log_file_path,'w')
            p = subprocess.Popen(['bash',sh_file_path],stdin=f_log, stdout=f_log, stderr=f_log)
            returncode = p.wait()
            f_log.close()
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
                    pass_project_list.append('    >> ' + line)
                f_log.close()
            
            os.remove(newsh_file_path)

f_final_log = open(current_dir+'/armgcc_build_log_file/final_log.txt','w')

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
print r"Please refer the "+current_dir+"/armgcc_build_log_file/final_log.txt for the build log"
