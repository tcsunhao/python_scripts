#!/ usr / bin / python
#Filename : autobuild_armgcc_release_package.py
#command line example:
# python autobuild_armgcc_release_package.py -n frdmk82f -m debug
# python autobuild_armgcc_release_package.py -n frdmk82f -m release
# python autobuild_armgcc_release_package.py -n frdmk82f -m all

import re,os,sys,time,subprocess, yaml, shutil
from aux_tool import ProgressBar, __warning_log_filter, __error_log_filter, __read_options,__output_log

rootdir = r"E:\tmp\SDK_2.0_MAPS-KS22_all_bdb4773\boards\mapsks22"

projectbuild_pass_number = 0
projectbuild_warning_number = 0
projectbuild_fail_number = 0

armgcc_log_dic = {}

proj_num = 0
proj_built_num = 0
build_mode = 'Debug'
progressbar_counter = 0
identify_string = ''

file_proj_num_statistics = 'proj_num_statistics.yml'
file_pass_withoutwarning = 'proj_pass_without_warning.txt'
file_pass_withwarning = 'proj_pass_with_warning.txt'
file_fail = 'proj_fail.txt'

def __get_projects_num(rootdir):
    proj_num = 0
    
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            filename_path = os.path.join(parent,filename)
            if re.search(r'CMakeLists',filename_path):
                    proj_num = proj_num + 1

    return proj_num

if __name__ == '__main__':
    has_build = 0

    # Gets the command line args
    the_args = __read_options()
    
    # Reads the build name for this time
    if the_args.buildname == None:
        print 'You need give a name for this build, the name can distinguish itself from next time build, such as python autobuild_armgcc_release_package -n frdmkxx -m debug'
        sys.exit()
    else:
        pass

    if the_args.rootdir == None:
        pass
    else:
        rootdir = the_args.rootdir        

    log_file_path_record = os.getcwd()
    log_file_path = os.getcwd() + '\\%s\\%s'% (the_args.buildname, 'armgcc') 
    
    # Changes the pass, warning and fail log file path, because the script will change the PWD to the armgcc proj path
    file_proj_num_statistics = log_file_path + '\\proj_num_statistics.yml'
    file_pass_withoutwarning = log_file_path + '\\proj_pass_without_warning.txt'
    file_pass_withwarning = log_file_path + '\\proj_pass_with_warning.txt'
    file_fail = log_file_path + '\\proj_fail.txt'

    # Checks wether the log_file_path already exists
    if os.path.exists(log_file_path):
        os.chdir(log_file_path)
        if os.path.exists(log_file_path + '\\%s' % file_proj_num_statistics):
            f = open(file_proj_num_statistics, 'r')
            armgcc_log_dic_tmp = yaml.load(f)
            if armgcc_log_dic_tmp:
                armgcc_log_dic = armgcc_log_dic_tmp.copy()
                if armgcc_log_dic.has_key('projectbuild_pass_number'):
                    projectbuild_pass_number = projectbuild_pass_number + armgcc_log_dic['projectbuild_pass_number']
                if armgcc_log_dic.has_key('projectbuild_warning_number'):
                    projectbuild_warning_number = projectbuild_warning_number + armgcc_log_dic['projectbuild_warning_number']
                if armgcc_log_dic.has_key('projectbuild_fail_number'):
                    projectbuild_fail_number = projectbuild_fail_number + armgcc_log_dic['projectbuild_fail_number']
                if armgcc_log_dic.has_key('progressbar_counter'):
                    progressbar_counter = progressbar_counter + armgcc_log_dic['progressbar_counter']
            f.close()          
    else:
        os.makedirs(log_file_path)
        os.chdir(log_file_path)

    # Uniforms the mode case
    if re.search(r'debug',the_args.mode,re.I):
        build_mode = 'debug'
    elif re.search(r'release',the_args.mode,re.I):
        build_mode = 'release'
    elif re.search(r'all',the_args.mode,re.I):
        build_mode = 'All'

    proj_num = __get_projects_num(rootdir)
    identify_string = the_args.buildname + the_args.mode

    pb = ProgressBar(proj_num)    
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            filename_path = os.path.join(parent,filename)
            if re.search(r'CMakeLists',filename_path):
                path_whetherbuild = ('\\').join(filename_path.split('\\')[0:-1]) + '\\' + 'whetherbuild_%s' % the_args.mode
                if os.path.exists(path_whetherbuild) == True:
                    f = open(path_whetherbuild, 'r')
                    if f.read().find(identify_string) != -1:
                        has_build = 1
                        proj_built_num = proj_built_num + 1
                    f.close()
                    if (proj_built_num == proj_num) : 
                        print 'All projects in the build %s_%s have been built before.' % (the_args.buildname, the_args.mode)
                        sys.exit()
                else:
                    has_build = 0

                if has_build == 0:
                    f = open(path_whetherbuild, 'w')
                    f.close()

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
                    
                    dirname_path = ('\\').join(filename_path.split('\\')[0:-1])
                    os.chdir(dirname_path)

                    # For 'debug' and 'release'
                    if build_mode == 'debug' or build_mode == 'release':
                        proj_name_withmode = proj_name + ' ' + build_mode

                        bat_file_path = dirname_path + '\\build_%s.bat' % (build_mode)
                        # Remove the 'pause' in the bat file
                        newbat_file_path = dirname_path + '\\newbuild_%s.bat' % (build_mode)
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
                        if build_mode == 'release':
                            f_newbat = open(newbat_file_path,'r')
                            file_content = f_newbat.read()
                            if file_content.find('build_log.txt') == -1:
                                file_content = file_content.strip('\n') + ' ' + '2> build_%s_log.txt' % build_mode
                            f_newbat.close()
                            f_newbat = open(newbat_file_path,'w')
                            f_newbat.write(file_content)
                            f_newbat.close()
                            armgcc_tmp_log_path = 'build_%s_log.txt' % build_mode
                        else:
                            armgcc_tmp_log_path = 'build_log.txt'
                            
                        print proj_name_withmode + ' ' + 'build start: ' 
                        sys.stdout.flush()
                        
                        p = subprocess.Popen('newbuild_%s.bat' % build_mode, stdin=None, stdout=None, stderr=None)
                        returncode = p.wait()

                        if returncode != 0:
                            projectbuild_fail_number += 1
                            armgcc_log_dic['projectbuild_fail_number'] = projectbuild_fail_number
                            __error_log_filter(armgcc_tmp_log_path, file_fail, proj_name_withmode)
                            print 78*'X'
                            print proj_name_withmode + ' ' + 'build failed' + '\n'
                        else : 
                            has_warning = __warning_log_filter(armgcc_tmp_log_path, file_pass_withwarning, proj_name_withmode)
                            if has_warning == 1:
                                projectbuild_warning_number += 1
                                armgcc_log_dic['projectbuild_warning_number'] = projectbuild_warning_number
                                print 78*'W'
                                print proj_name_withmode + ' ' + 'build pass with warnings' + '\n'
                            else:
                                projectbuild_pass_number += 1
                                armgcc_log_dic['projectbuild_pass_number'] = projectbuild_pass_number
                                print proj_name_withmode + ' ' + 'build pass without warnings' + '\n'
                                f_file_pass_withoutwarning = open(file_pass_withoutwarning, 'a')
                                f_file_pass_withoutwarning.write(proj_name_withmode + '\n')
                                f_file_pass_withoutwarning.close()

                        os.remove(newbat_file_path)
                    
                    # For 'All'
                    elif build_mode == 'All':

                        debug_bat_file_path = dirname_path + '\\build_debug.bat'
                        release_bat_file_path = dirname_path + '\\build_release.bat'
                        # Remove the 'pause' in the bat file
                        debug_newbat_file_path = dirname_path + '\\newbuild_debug.bat'
                        release_newbat_file_path = dirname_path + '\\newbuild_release.bat'
                        f_debug_bat = open(debug_bat_file_path,'r')
                        f_release_bat = open(release_bat_file_path,'r')
                        f_debug_newbat = open(debug_newbat_file_path,'w')
                        f_release_newbat = open(release_newbat_file_path,'w')
                        
                        f_debug_bat_data = f_debug_bat.readlines()
                        for line in f_debug_bat_data:
                            if 'pause' in line:
                                continue
                            f_debug_newbat.write(line)
                        f_debug_bat.close()
                        f_debug_newbat.close()
                        
                        f_release_bat_data = f_release_bat.readlines()
                        for line in f_release_bat_data:
                            if 'pause' in line:
                                continue
                            f_release_newbat.write(line)
                        f_release_bat.close()
                        f_release_newbat.close()
                        
                        # the release bat file need to add "build_log.txt"
                        f_release_newbat = open(release_newbat_file_path,'r')
                        file_content = f_release_newbat.read()
                        if file_content.find('build_log.txt') == -1:
                            file_content = file_content.strip('\n') + ' ' + '2> build_release_log.txt'
                        f_release_newbat.close()
                        f_release_newbat = open(release_newbat_file_path,'w')
                        f_release_newbat.write(file_content)
                        f_release_newbat.close()
                        armgcc_release_tmp_log_path = 'build_release_log.txt'
                        armgcc_debug_tmp_log_path = 'build_log.txt'
                        
                        print proj_name + ' ' + 'build start: '

                        debug_task = subprocess.Popen('newbuild_debug.bat', stdin=None, stdout=None, stderr=None)
                        debug_ret = debug_task.wait()
                        release_task = subprocess.Popen('newbuild_release.bat', stdin=None, stdout=None, stderr=None)
                        release_ret = release_task.wait()

                        if debug_ret != 0:
                            proj_name_withmode = proj_name + ' ' + 'debug'
                            projectbuild_fail_number += 1
                            armgcc_log_dic['projectbuild_fail_number'] = projectbuild_fail_number
                            __error_log_filter(armgcc_debug_tmp_log_path, file_fail, proj_name_withmode)
                            print 78*'X'
                            print proj_name_withmode + ' ' + 'build failed' + '\n'
                        else : 
                            proj_name_withmode = proj_name + ' ' + 'debug'
                            has_warning = __warning_log_filter(armgcc_debug_tmp_log_path, file_pass_withwarning, proj_name_withmode)
                            if has_warning == 1:
                                projectbuild_warning_number += 1
                                armgcc_log_dic['projectbuild_warning_number'] = projectbuild_warning_number
                                print 78*'W'
                                print proj_name_withmode + ' ' + 'build pass with warnings' + '\n'
                            else:
                                projectbuild_pass_number += 1
                                armgcc_log_dic['projectbuild_pass_number'] = projectbuild_pass_number
                                print proj_name_withmode + ' ' + 'build pass without warnings' + '\n'
                                f_file_pass_withoutwarning = open(file_pass_withoutwarning, 'a')
                                f_file_pass_withoutwarning.write(proj_name_withmode + '\n')
                                f_file_pass_withoutwarning.close()
                        
                        if release_ret != 0:
                            proj_name_withmode = proj_name + ' ' + 'release'
                            projectbuild_fail_number += 1
                            armgcc_log_dic['projectbuild_fail_number'] = projectbuild_fail_number
                            __error_log_filter(armgcc_release_tmp_log_path, file_fail, proj_name_withmode)
                            print 78*'X'
                            print proj_name_withmode + ' ' + 'build failed' + '\n'
                        else : 
                            proj_name_withmode = proj_name + ' ' + 'release'
                            has_warning = __warning_log_filter(armgcc_release_tmp_log_path, file_pass_withwarning, proj_name_withmode)
                            if has_warning == 1:
                                projectbuild_warning_number += 1
                                armgcc_log_dic['projectbuild_warning_number'] = projectbuild_warning_number
                                print 78*'W'
                                print proj_name_withmode + ' ' + 'build pass with warnings' + '\n'
                            else:
                                projectbuild_pass_number += 1
                                armgcc_log_dic['projectbuild_pass_number'] = projectbuild_pass_number
                                print proj_name_withmode + ' ' + 'build pass without warnings' + '\n'
                                f_file_pass_withoutwarning = open(file_pass_withoutwarning, 'a')
                                f_file_pass_withoutwarning.write(proj_name_withmode + '\n')
                                f_file_pass_withoutwarning.close()
                        
                        os.remove(debug_newbat_file_path)
                        os.remove(release_newbat_file_path)

                    progressbar_counter = progressbar_counter + 1
                    print pb(progressbar_counter)
                    sys.stdout.flush()
                    armgcc_log_dic['progressbar_counter'] = progressbar_counter
                    # Update the file_proj_num_statistics
                    f = open(file_proj_num_statistics,'w')
                    yaml.dump(armgcc_log_dic, f)
                    f.close()

                    # Means this project just finish build
                    f = open(path_whetherbuild, 'w')
                    f.write(identify_string)
                    f.close()
                else:
                    has_build = 0


    # Output the log
    path_log_file = log_file_path_record + '\\%s\\armgcc_%s_build_log.txt' % (the_args.buildname, build_mode)
    __output_log(armgcc_log_dic, file_pass_withoutwarning, file_pass_withwarning, file_fail, path_log_file)
    # Returns to the up dir 
    os.chdir(log_file_path_record)
    shutil.rmtree(log_file_path)  

    print 78*'*'
    print 78*'*'
    print "Please refer the %s for the build log " % path_log_file