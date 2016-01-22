#!/usr/bin/python
#Filename : autobuild_iar_release_package.py
#command line example:
#   python autobuild_iar_release_package.py debug 
#   python autobuild_iar_release_package.py release 
#   python autobuild_iar_release_package.py all

import re,os,sys,time,subprocess
from aux_tool import ProgressBar, __get_projects_num, __warning_log_filter, __error_log_filter, __read_options,__output_log

# rootdir = r"E:\tmp\rc1\SDK_2.0_FRDM-K66F_all2\boards\frdmk66f"
rootdir = r"E:\tmp\SDK_2.0_FRDM-K82F_all_nda_3f09dc9\boards\frdmk82f\demo_apps"

iar_extension_name = '\\*.ewp'

iar_pass_number = 0
iar_warning_number = 0
iar_fail_number = 0

pass_project_list = []
warning_log_list = []
error_log_list = []

proj_num = 0
build_mode = 'Debug'
i = 0
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

def _run_command(cmd, filename_path, build_mode):
    global iar_pass_number
    global iar_fail_number
    global iar_warning_number
    global has_warning
    global first_warning
    
    # Get project name from file path

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
            iar_fail_number += 1
            error_log_list.append(proj_name + ' build failed\n')
            __error_log_filter(iar_debug_tmp_log_path, error_log_list)
            print 78*'X'
            print proj_name + ' ' + 'build failed' + '\n'
        # If the project build passed, find the warnings
        else : 
            has_warning = __warning_log_filter(iar_debug_tmp_log_path, warning_log_list, proj_name)
            if has_warning == 1:
                iar_warning_number += 1
                print 78*'W'
                print proj_name + ' ' + 'build pass with warnings' + '\n'
            else:
                iar_pass_number += 1
                print proj_name + ' ' + 'build pass without warnings' + '\n'
                pass_project_list.append(proj_name + '\n')
            
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
            iar_fail_number += 1
            error_log_list.append(proj_name + ' build failed\n')
            __error_log_filter(iar_release_tmp_log_path, error_log_list)
            print 78*'X'
            print proj_name + ' ' + 'build failed' + '\n'
        # If the project build passed, find the warnings
        else : 
            has_warning = __warning_log_filter(iar_release_tmp_log_path, warning_log_list, proj_name)
            if has_warning == 1:
                iar_warning_number += 1
                print 78*'W'
                print proj_name + ' ' + 'build pass with warnings' + '\n'
            else:
                iar_pass_number += 1
                print proj_name + ' ' + 'build pass without warnings' + '\n'
                pass_project_list.append(proj_name + '\n')
            
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
        
        # If the project build failed
        if debug_ret != 0 :
            proj_name = filename_path.split('\\')[-1] + ' ' + 'debug'
            iar_fail_number += 1
            error_log_list.append(proj_name + ' ' + 'build failed\n')
            __error_log_filter(iar_debug_tmp_log_path, error_log_list)
            print 78*'X'
            print proj_name + ' ' + 'build failed' + '\n'
        # If the project build passed, find the warnings
        else : 
            proj_name = filename_path.split('\\')[-1] + ' ' + 'debug'
            has_warning = __warning_log_filter(iar_debug_tmp_log_path, warning_log_list, proj_name)
            if has_warning == 1:
                iar_warning_number += 1
                print 78*'W'
                print proj_name + ' ' + 'build pass with warnings' + '\n'
            else:
                iar_pass_number += 1
                print proj_name + ' ' + 'build pass without warnings' + '\n'
                pass_project_list.append(proj_name + '\n')        
        
        # If the project build failed
        if release_ret != 0 :
            proj_name = filename_path.split('\\')[-1] + ' ' + 'release'
            iar_fail_number += 1
            error_log_list.append(proj_name + ' build failed\n')
            __error_log_filter(iar_release_tmp_log_path, error_log_list)
            print 78*'X'
            print proj_name + ' ' + 'build failed' + '\n'
        # If the project build passed, find the warnings
        else : 
            proj_name = filename_path.split('\\')[-1] + ' ' + 'release'
            has_warning = __warning_log_filter(iar_release_tmp_log_path, warning_log_list, proj_name)
            if has_warning == 1:
                iar_warning_number += 1
                print 78*'W'
                print proj_name + ' ' + 'build pass with warnings' + '\n'
            else:
                iar_pass_number += 1
                print proj_name + ' ' + 'build pass without warnings' + '\n'
                pass_project_list.append(proj_name + '\n')
            
        os.remove(iar_release_tmp_log_path)
        os.remove(iar_debug_tmp_log_path)

if __name__ == '__main__':

    # Gets IAR bin path
    iar_bin_path = __search_iar()
    
    # Gets the command line args
    the_args = __read_options()
    
    # Uniform the mode case
    if re.search(r'debug',the_args.mode,re.I):
        build_mode = 'Debug'
    elif re.search(r'release',the_args.mode,re.I):
        build_mode = 'Release'
    elif re.search(r'all',the_args.mode,re.I):
        build_mode = 'All'

    proj_num = __get_projects_num(rootdir)
    
    pb = ProgressBar(proj_num)
    # Starts the program
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            filename_path = os.path.join(parent,filename)
            if re.search(r'\.ewp',filename_path):
                _run_command(iar_bin_path, filename_path, build_mode)
                i = i + 1
                print pb(i)
                sys.stdout.flush()


    log_member = (iar_pass_number, iar_warning_number, iar_fail_number, pass_project_list, warning_log_list, error_log_list, )

    # Creates log file
    path_log_file = rootdir + '\\iar_%s_build_log.txt' % build_mode
    f_final_log = open(path_log_file,'w')

    __output_log(log_member, f_final_log)

    f_final_log.close()

    print 78*'*'
    print 78*'*'
    print "Please refer the %s for the build log " % path_log_file
 