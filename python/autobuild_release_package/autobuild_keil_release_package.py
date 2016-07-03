#!/ usr / bin / python
#Filename : autobuild_keil_release_package.py
#command line example:
# python autobuild_keil_release_package.py -n frdmk82f -m debug
# python autobuild_keil_release_package.py -n frdmk82f -m release
# python autobuild_keil_release_package.py -n frdmk82f -m all

import re,os,sys,time,subprocess, yaml, shutil
from aux_tool import ProgressBar, __warning_log_filter, __error_log_filter, __read_options,__output_log

rootdir = r"E:\tmp\SDK_2.0_FRDM-KL28Z_all_nda_75cb2bf\boards\frdmkl28z"

keil_extension_name = '\\*.uvprojx'

projectbuild_pass_number = 0
projectbuild_warning_number = 0
projectbuild_fail_number = 0

keil_log_dic = {}

proj_num = 0
proj_built_num = 0
build_mode = 'Debug'
progressbar_counter = 0
identify_string = ''

file_proj_num_statistics = 'proj_num_statistics.yml'
file_pass_withoutwarning = 'proj_pass_without_warning.txt'
file_pass_withwarning = 'proj_pass_with_warning.txt'
file_fail = 'proj_fail.txt'

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
def __get_projects_num(rootdir):
    proj_num = 0
    
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            filename_path = os.path.join(parent,filename)
            if re.search(r'uvprojx',filename_path):
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

        keil_debug_tmp_log_path = os.getcwd() + '\\keil_debug_tmp_log.txt'
        proj_name_ = proj_name.split('.')[0]
        keil_cmd = '''%s -b %s -o %s -j0 -t "%s %s"''' %(cmd, filename_path, keil_debug_tmp_log_path, proj_name_, build_mode)
        # debug_task = subprocess.Popen([cmd,'-b',filename_path,'-o',keil_debug_tmp_log_path,'-j0','-t',"%s %s" % (proj_name, build_mode)], 0, stdin=None, stdout=None, stderr=None, shell = True)
        debug_task = subprocess.Popen(keil_cmd, 0, stdin=None, stdout=None, stderr=None, shell = True)
        debug_ret = debug_task.wait()
        
        # If the project build failed
        if debug_ret != 0 :
            projectbuild_fail_number += 1
            keil_log_dic['projectbuild_fail_number'] = projectbuild_fail_number
            __error_log_filter(keil_debug_tmp_log_path, file_fail, proj_name)
            print 78*'X'
            print proj_name + ' ' + 'build failed' + '\n'
        # If the project build passed, find the warnings
        else : 
            has_warning = __warning_log_filter(keil_debug_tmp_log_path, file_pass_withwarning, proj_name)
            if has_warning == 1:
                projectbuild_warning_number += 1
                keil_log_dic['projectbuild_warning_number'] = projectbuild_warning_number
                print 78*'W'
                print proj_name + ' ' + 'build pass with warnings' + '\n'
            else:
                projectbuild_pass_number += 1
                keil_log_dic['projectbuild_pass_number'] = projectbuild_pass_number
                print proj_name + ' ' + 'build pass without warnings' + '\n'
                f_file_pass_withoutwarning = open(file_pass_withoutwarning, 'a')
                f_file_pass_withoutwarning.write(proj_name + '\n')
                f_file_pass_withoutwarning.close()

        os.remove(keil_debug_tmp_log_path)
    
    elif build_mode == 'Release':
        proj_name = filename_path.split('\\')[-1] + ' ' + build_mode
        
        print '%s %s make %s' % (cmd, filename_path, build_mode)
        sys.stdout.flush()

        keil_release_tmp_log_path = os.getcwd() + '\\keil_release_tmp_log.txt'
        proj_name_ = proj_name.split('.')[0]
        keil_cmd = '''%s -b %s -o %s -j0 -t "%s %s"''' %(cmd, filename_path, keil_release_tmp_log_path, proj_name_, build_mode)
        # release_task = subprocess.Popen([cmd,'-b',filename_path,'-o',keil_release_tmp_log_path,'-j0','-t',"%s %s" % (proj_name, build_mode)], 0, stdin=None, stdout=None, stderr=None, shell = True)
        release_task = subprocess.Popen(keil_cmd, 0, stdin=None, stdout=None, stderr=None, shell = True)
        release_ret = release_task.wait()
        
        # If the project build failed
        if release_ret != 0 :
            projectbuild_fail_number += 1
            keil_log_dic['projectbuild_fail_number'] = projectbuild_fail_number
            __error_log_filter(keil_release_tmp_log_path, file_fail, proj_name)
            print 78*'X'
            print proj_name + ' ' + 'build failed' + '\n'
        # If the project build passed, find the warnings
        else : 
            has_warning = __warning_log_filter(keil_release_tmp_log_path, file_pass_withwarning, proj_name)
            if has_warning == 1:
                projectbuild_warning_number += 1
                keil_log_dic['projectbuild_warning_number'] = projectbuild_warning_number
                print 78*'W'
                print proj_name + ' ' + 'build pass with warnings' + '\n'
            else:
                projectbuild_pass_number += 1
                keil_log_dic['projectbuild_pass_number'] = projectbuild_pass_number
                print proj_name + ' ' + 'build pass without warnings' + '\n'
                f_file_pass_withoutwarning = open(file_pass_withoutwarning, 'a')
                f_file_pass_withoutwarning.write(proj_name + '\n')
                f_file_pass_withoutwarning.close()

        os.remove(keil_release_tmp_log_path)  

    elif build_mode == 'All':
        print '%s %s make %s' % (cmd, filename_path, build_mode)
        sys.stdout.flush()

        keil_release_tmp_log_path = os.getcwd() + '\\keil_release_tmp_log.txt' 
        keil_debug_tmp_log_path = os.getcwd() + '\\keil_debug_tmp_log.txt' 

        proj_name_ = filename_path.split('\\')[-1].split('.')[0]

        keil_cmd_debug = '''%s -b %s -o %s -j0 -t "%s %s"''' %(cmd, filename_path, keil_debug_tmp_log_path, proj_name_, 'Debug')        
        keil_cmd_release = '''%s -b %s -o %s -j0 -t "%s %s"''' %(cmd, filename_path, keil_release_tmp_log_path, proj_name_, 'Release')
      
        debug_task = subprocess.Popen(keil_cmd_debug, 0, stdin=None, stdout=None, stderr=None, shell=True)
        release_task = subprocess.Popen(keil_cmd_release, 0, stdin=None, stdout=None, stderr=None, shell=True)
        
        release_ret = release_task.wait()
        debug_ret = debug_task.wait()
                
        # If the debug project build failed
        if debug_ret != 0 :
            proj_name = filename_path.split('\\')[-1] + ' ' + 'debug'
            projectbuild_fail_number += 1
            keil_log_dic['projectbuild_fail_number'] = projectbuild_fail_number
            __error_log_filter(keil_debug_tmp_log_path, file_fail, proj_name)
            print 78*'X'
            print proj_name + ' ' + 'build failed' + '\n'
        # If the project build passed, find the warnings
        else : 
            proj_name = filename_path.split('\\')[-1] + ' ' + 'debug'
            has_warning = __warning_log_filter(keil_debug_tmp_log_path, file_pass_withwarning, proj_name)
            if has_warning == 1:
                projectbuild_warning_number += 1
                keil_log_dic['projectbuild_warning_number'] = projectbuild_warning_number
                print 78*'W'
                print proj_name + ' ' + 'build pass with warnings' + '\n'
            else:
                projectbuild_pass_number += 1
                keil_log_dic['projectbuild_pass_number'] = projectbuild_pass_number
                print proj_name + ' ' + 'build pass without warnings' + '\n'
                f_file_pass_withoutwarning = open(file_pass_withoutwarning, 'a')
                f_file_pass_withoutwarning.write(proj_name + '\n')
                f_file_pass_withoutwarning.close()        
        
        # If the project build failed
        if release_ret != 0 :
            proj_name = filename_path.split('\\')[-1] + ' ' + 'release'
            projectbuild_fail_number += 1
            keil_log_dic['projectbuild_fail_number'] = projectbuild_fail_number
            __error_log_filter(keil_release_tmp_log_path, file_fail, proj_name)
            print 78*'X'
            print proj_name + ' ' + 'build failed' + '\n'
        # If the project build passed, find the warnings
        else : 
            proj_name = filename_path.split('\\')[-1] + ' ' + 'release'
            has_warning = __warning_log_filter(keil_release_tmp_log_path, file_pass_withwarning, proj_name)
            if has_warning == 1:
                projectbuild_warning_number += 1
                keil_log_dic['projectbuild_warning_number'] = projectbuild_warning_number
                print 78*'W'
                print proj_name + ' ' + 'build pass with warnings' + '\n'
            else:
                projectbuild_pass_number += 1
                keil_log_dic['projectbuild_pass_number'] = projectbuild_pass_number
                print proj_name + ' ' + 'build pass without warnings' + '\n'
                f_file_pass_withoutwarning = open(file_pass_withoutwarning, 'a')
                f_file_pass_withoutwarning.write(proj_name + '\n')
                f_file_pass_withoutwarning.close()
            
        os.remove(keil_release_tmp_log_path)
        os.remove(keil_debug_tmp_log_path)   
        
    # Update the file_proj_num_statistics
    f = open(file_proj_num_statistics,'w')
    yaml.dump(keil_log_dic, f)
    f.close()

if __name__ == '__main__':
    has_build = 0
    
    # Gets keil bin path
    keil_bin_path = __search_keil()
    
    # Gets the command line args
    the_args = __read_options()
    
    # Reads the build name for this time
    if the_args.buildname == None:
        print 'You need give a name for this build, the name can distinguish itself from next time build, such as python autobuild_keil_release_package -n frdmkxx -m debug'
        sys.exit()
    else:
        pass

    if the_args.rootdir == None:
        pass
    else:
        rootdir = the_args.rootdir
        
    log_file_path_record = os.getcwd()
    log_file_path = os.getcwd() + '\\%s\\%s'% (the_args.buildname, 'keil') 
    # Checks wether the log_file_path already exists
    if os.path.exists(log_file_path):
        os.chdir(log_file_path)
        if os.path.exists(log_file_path + '\\%s' % file_proj_num_statistics):
            f = open(file_proj_num_statistics, 'r')
            keil_log_dic_tmp = yaml.load(f)
            if keil_log_dic_tmp:
                keil_log_dic = keil_log_dic_tmp.copy()
                if keil_log_dic.has_key('projectbuild_pass_number'):
                    projectbuild_pass_number = projectbuild_pass_number + keil_log_dic['projectbuild_pass_number']
                if keil_log_dic.has_key('projectbuild_warning_number'):
                    projectbuild_warning_number = projectbuild_warning_number + keil_log_dic['projectbuild_warning_number']
                if keil_log_dic.has_key('projectbuild_fail_number'):
                    projectbuild_fail_number = projectbuild_fail_number + keil_log_dic['projectbuild_fail_number']
                if keil_log_dic.has_key('progressbar_counter'):
                    progressbar_counter = progressbar_counter + keil_log_dic['progressbar_counter']
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
            if re.search(r'uvprojx',filename_path):
                path_whetherbuild = ('\\').join(filename_path.split('\\')[0:-1]) + '\\' + 'whetherbuild_%s' % the_args.mode
                if os.path.exists(path_whetherbuild) == True:
                    f = open(path_whetherbuild, 'r')
                    if f.read().find(identify_string) != -1:
                        has_build = 1
                        proj_built_num = proj_built_num + 1
                    f.close()
                    if (proj_built_num == proj_num):
                        print 'All projects in the build %s_%s have been built before.' % (the_args.buildname, the_args.mode)
                        sys.exit()
                else:
                    has_build = 0

                if has_build == 0:
                    f = open(path_whetherbuild, 'w')
                    f.close()
                    
                    _run_command(keil_bin_path, filename_path, build_mode)
                    
                    
                    progressbar_counter = progressbar_counter + 1
                    print pb(progressbar_counter)
                    sys.stdout.flush()
                    keil_log_dic['progressbar_counter'] = progressbar_counter
                    # Update the file_proj_num_statistics
                    f = open(file_proj_num_statistics,'w')
                    yaml.dump(keil_log_dic, f)
                    f.close()

                    f = open(path_whetherbuild, 'w')
                    f.write(identify_string)
                    f.close()
                else:
                    has_build = 0

    # Output the log
    path_log_file = log_file_path_record + '\\%s\\keil_%s_build_log.txt' % (the_args.buildname, build_mode)
    __output_log(keil_log_dic, file_pass_withoutwarning, file_pass_withwarning, file_fail, path_log_file)
    # Returns to the up dir 
    os.chdir(log_file_path_record)
    shutil.rmtree(log_file_path)  

    print 78*'*'
    print 78*'*'
    print "Please refer the %s for the build log " % path_log_file