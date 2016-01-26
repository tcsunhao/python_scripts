#!/usr/bin/python
#Filename : autobuild_iar_release_package.py
#command line example:
#   python autobuild_iar_release_package.py -n build1 -m debug 
#   python autobuild_iar_release_package.py -n build1 -m release 
#   python autobuild_iar_release_package.py -n build1 -m all

import re,os,sys,time,subprocess, yaml, shutil
from aux_tool import ProgressBar, __warning_log_filter, __error_log_filter, __read_options,__output_log

# rootdir = r"E:\tmp\rc1\SDK_2.0_FRDM-K66F_all2\boards\frdmk66f"
rootdir = r"E:\tmp\SDK_2.0_MAPS-KS22_all_bdb4773\boards\mapsks22"

iar_extension_name = '\\*.ewp'

projectbuild_pass_number = 0
projectbuild_warning_number = 0
projectbuild_fail_number = 0

iar_log_dic = {}

proj_num = 0
proj_built_num = 0
build_mode = 'Debug'
progressbar_counter = 0
identify_string = ''

file_proj_num_statistics = 'proj_num_statistics.yml'
file_pass_withoutwarning = 'proj_pass_without_warning.txt'
file_pass_withwarning = 'proj_pass_with_warning.txt'
file_fail = 'proj_fail.txt'

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

def __get_projects_num(rootdir):
    proj_num = 0
    
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            filename_path = os.path.join(parent,filename)
            if re.search(r'\.ewp',filename_path):
                proj_num = proj_num + 1

    return proj_num

def _run_command(cmd, filename_path, build_mode):
    global projectbuild_pass_number
    global projectbuild_fail_number
    global projectbuild_warning_number
    has_warning = 0
    first_warning = 0

    if build_mode == 'Debug':
        proj_name = filename_path.split('\\')[-1] + ' ' + build_mode
        
        print '%s %s make %s' % (cmd, filename_path, build_mode)
        sys.stdout.flush()

        iar_debug_tmp_log_path = 'iar_debug_tmp_log.txt' 
        f_debug_log = open(iar_debug_tmp_log_path, 'w')
        debug_task = subprocess.Popen([cmd, filename_path, '-make', build_mode, '-log', 'info', '-parallel', '4'], 0, stdin=f_debug_log, stdout=f_debug_log, stderr=f_debug_log, shell=True)
        debug_ret = debug_task.wait()
        f_debug_log.close()
        
        # If the project build failed
        if debug_ret != 0 :
            projectbuild_fail_number += 1
            iar_log_dic['projectbuild_fail_number'] = projectbuild_fail_number
            __error_log_filter(iar_debug_tmp_log_path, file_fail, proj_name)
            print 78*'X'
            print proj_name + ' ' + 'build failed' + '\n'
        # If the project build passed, find the warnings
        else : 
            has_warning = __warning_log_filter(iar_debug_tmp_log_path, file_pass_withwarning, proj_name)
            if has_warning == 1:
                projectbuild_warning_number += 1
                iar_log_dic['projectbuild_warning_number'] = projectbuild_warning_number
                print 78*'W'
                print proj_name + ' ' + 'build pass with warnings' + '\n'
            else:
                projectbuild_pass_number += 1
                iar_log_dic['projectbuild_pass_number'] = projectbuild_pass_number
                print proj_name + ' ' + 'build pass without warnings' + '\n'
                f_file_pass_withoutwarning = open(file_pass_withoutwarning, 'a')
                f_file_pass_withoutwarning.write(proj_name + '\n')
                f_file_pass_withoutwarning.close()

        os.remove(iar_debug_tmp_log_path)
    
    elif build_mode == 'Release':
        proj_name = filename_path.split('\\')[-1] + ' ' + build_mode
        
        print '%s %s make %s' % (cmd, filename_path, build_mode)
        sys.stdout.flush()

        iar_release_tmp_log_path = 'iar_release_tmp_log.txt' 
        f_release_log = open(iar_release_tmp_log_path, 'w')
        release_task = subprocess.Popen([cmd, filename_path, '-make', build_mode, '-log', 'info', '-parallel', '4'], 0, stdin=f_release_log, stdout=f_release_log, stderr=f_release_log, shell=True)
        release_ret = release_task.wait()
        f_release_log.close()
        
        # If the project build failed
        if release_ret != 0 :
            projectbuild_fail_number += 1
            iar_log_dic['projectbuild_fail_number'] = projectbuild_fail_number
            __error_log_filter(iar_release_tmp_log_path, file_fail, proj_name)
            print 78*'X'
            print proj_name + ' ' + 'build failed' + '\n'
        # If the project build passed, find the warnings
        else : 
            has_warning = __warning_log_filter(iar_release_tmp_log_path, file_pass_withwarning, proj_name)
            if has_warning == 1:
                projectbuild_warning_number += 1
                iar_log_dic['projectbuild_warning_number'] = projectbuild_warning_number
                print 78*'W'
                print proj_name + ' ' + 'build pass with warnings' + '\n'
            else:
                projectbuild_pass_number += 1
                iar_log_dic['projectbuild_pass_number'] = projectbuild_pass_number
                print proj_name + ' ' + 'build pass without warnings' + '\n'
                f_file_pass_withoutwarning = open(file_pass_withoutwarning, 'a')
                f_file_pass_withoutwarning.write(proj_name + '\n')
                f_file_pass_withoutwarning.close()
        
        os.remove(iar_release_tmp_log_path)
    
    elif build_mode == 'All':
        
        print '%s %s make %s' % (cmd, filename_path, build_mode)
        sys.stdout.flush()

        iar_release_tmp_log_path = 'iar_release_tmp_log.txt' 
        iar_debug_tmp_log_path = 'iar_debug_tmp_log.txt' 
        
        f_release_log = open(iar_release_tmp_log_path, 'w')
        f_debug_log = open(iar_debug_tmp_log_path, 'w')
        
        release_task = subprocess.Popen([cmd, filename_path, '-make', 'Debug', '-log', 'info', '-parallel', '4'], 0, stdin=f_release_log, stdout=f_release_log, stderr=f_release_log, shell=True)
        debug_task = subprocess.Popen([cmd, filename_path, '-make', 'Release', '-log', 'info', '-parallel', '4'], 0, stdin=f_debug_log, stdout=f_debug_log, stderr=f_debug_log, shell=True)
        
        release_ret = release_task.wait()
        debug_ret = debug_task.wait()
        
        f_release_log.close()
        f_debug_log.close()
        
        # If the debug project build failed
        if debug_ret != 0 :
            proj_name = filename_path.split('\\')[-1] + ' ' + 'debug'
            projectbuild_fail_number += 1
            iar_log_dic['projectbuild_fail_number'] = projectbuild_fail_number
            __error_log_filter(iar_debug_tmp_log_path, file_fail, proj_name)
            print 78*'X'
            print proj_name + ' ' + 'build failed' + '\n'
        # If the project build passed, find the warnings
        else : 
            proj_name = filename_path.split('\\')[-1] + ' ' + 'debug'
            has_warning = __warning_log_filter(iar_debug_tmp_log_path, file_pass_withwarning, proj_name)
            if has_warning == 1:
                projectbuild_warning_number += 1
                iar_log_dic['projectbuild_warning_number'] = projectbuild_warning_number
                print 78*'W'
                print proj_name + ' ' + 'build pass with warnings' + '\n'
            else:
                projectbuild_pass_number += 1
                iar_log_dic['projectbuild_pass_number'] = projectbuild_pass_number
                print proj_name + ' ' + 'build pass without warnings' + '\n'
                f_file_pass_withoutwarning = open(file_pass_withoutwarning, 'a')
                f_file_pass_withoutwarning.write(proj_name + '\n')
                f_file_pass_withoutwarning.close()        
        
        # If the project build failed
        if release_ret != 0 :
            proj_name = filename_path.split('\\')[-1] + ' ' + 'release'
            projectbuild_fail_number += 1
            iar_log_dic['projectbuild_fail_number'] = projectbuild_fail_number
            __error_log_filter(iar_release_tmp_log_path, file_fail, proj_name)
            print 78*'X'
            print proj_name + ' ' + 'build failed' + '\n'
        # If the project build passed, find the warnings
        else : 
            proj_name = filename_path.split('\\')[-1] + ' ' + 'release'
            has_warning = __warning_log_filter(iar_release_tmp_log_path, file_pass_withwarning, proj_name)
            if has_warning == 1:
                projectbuild_warning_number += 1
                iar_log_dic['projectbuild_warning_number'] = projectbuild_warning_number
                print 78*'W'
                print proj_name + ' ' + 'build pass with warnings' + '\n'
            else:
                projectbuild_pass_number += 1
                iar_log_dic['projectbuild_pass_number'] = projectbuild_pass_number
                print proj_name + ' ' + 'build pass without warnings' + '\n'
                f_file_pass_withoutwarning = open(file_pass_withoutwarning, 'a')
                f_file_pass_withoutwarning.write(proj_name + '\n')
                f_file_pass_withoutwarning.close()
            
        os.remove(iar_release_tmp_log_path)
        os.remove(iar_debug_tmp_log_path)        
    
    # Update the file_proj_num_statistics
    f = open(file_proj_num_statistics,'w')
    yaml.dump(iar_log_dic, f)
    f.close()


if __name__ == '__main__':
    has_build = 0

    # Gets IAR bin path
    iar_bin_path = __search_iar()
    
    # Gets the command line args
    the_args = __read_options()
    
    # Reads the build name for this time
    if the_args.buildname == None:
        print 'You need give a name for this build, the name can distinguish itself from next time build, such as python autobuild_iar_release_package -n frdmkxx -m debug'
        sys.exit()
    else:
        pass

    log_file_path_record = os.getcwd()
    log_file_path = os.getcwd() + '\\%s\\%s'% (the_args.buildname, 'iar') 
    # Checks wether the log_file_path already exists
    if os.path.exists(log_file_path):
        os.chdir(log_file_path)
        if os.path.exists(log_file_path + '\\%s' % file_proj_num_statistics):
            f = open(file_proj_num_statistics, 'r')
            iar_log_dic_tmp = yaml.load(f)
            if iar_log_dic_tmp:
                iar_log_dic = iar_log_dic_tmp.copy()
                if iar_log_dic.has_key('projectbuild_pass_number'):
                    projectbuild_pass_number = projectbuild_pass_number + iar_log_dic['projectbuild_pass_number']
                if iar_log_dic.has_key('projectbuild_warning_number'):
                    projectbuild_warning_number = projectbuild_warning_number + iar_log_dic['projectbuild_warning_number']
                if iar_log_dic.has_key('projectbuild_fail_number'):
                    projectbuild_fail_number = projectbuild_fail_number + iar_log_dic['projectbuild_fail_number']
                if iar_log_dic.has_key('progressbar_counter'):
                    progressbar_counter = progressbar_counter + iar_log_dic['progressbar_counter']
            f.close()          
    else:
        os.makedirs(log_file_path)
        os.chdir(log_file_path)

    # Uniforms the mode case
    if re.search(r'debug',the_args.mode,re.I):
        build_mode = 'Debug'
    elif re.search(r'release',the_args.mode,re.I):
        build_mode = 'Release'
    elif re.search(r'all',the_args.mode,re.I):
        build_mode = 'All'

    proj_num = __get_projects_num(rootdir)
    identify_string = the_args.buildname + the_args.mode

    pb = ProgressBar(proj_num)
    # Starts the program
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            filename_path = os.path.join(parent,filename)
            if re.search(r'\.ewp',filename_path):
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
                    
                    _run_command(iar_bin_path, filename_path, build_mode)
                    
                    progressbar_counter = progressbar_counter + 1
                    print pb(progressbar_counter)
                    sys.stdout.flush()
                    iar_log_dic['progressbar_counter'] = progressbar_counter
                    # Update the file_proj_num_statistics
                    f = open(file_proj_num_statistics,'w')
                    yaml.dump(iar_log_dic, f)
                    f.close()
                    
                    f = open(path_whetherbuild, 'w')
                    f.write(identify_string)
                    f.close()
                else:
                    has_build = 0

    # Output the log
    path_log_file = log_file_path_record + '\\%s\\iar_%s_build_log.txt' % (the_args.buildname, build_mode)
    __output_log(iar_log_dic, file_pass_withoutwarning, file_pass_withwarning, file_fail, path_log_file)
    # Returns to the up dir 
    os.chdir(log_file_path_record)
    shutil.rmtree(log_file_path)  

    print 78*'*'
    print 78*'*'
    print "Please refer the %s for the build log " % path_log_file
 