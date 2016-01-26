#!/ usr / bin / python
#Filename : autobuild_atl_release_package.py
#command line example:
# python autobuild_atl_release_package.py -n frdmk82f -m debug
# python autobuild_atl_release_package.py -n frdmk82f -m release
# python autobuild_atl_release_package.py -n frdmk82f -m all

import re,os,sys,time,subprocess,shutil,yaml
import xml.dom.minidom
from aux_tool import ProgressBar, __warning_log_filter, __error_log_filter, __read_options,__output_log

rootdir = r"E:\tmp\SDK_2.0_FRDM-K82F_all_nda_3f09dc9\boards\frdmk82f"

projectbuild_pass_number = 0
projectbuild_warning_number = 0
projectbuild_fail_number = 0

atl_log_dic = {}

proj_num = 0
proj_built_num = 0
build_mode = 'Debug'
progressbar_counter = 0
identify_string = ''

file_proj_num_statistics = 'proj_num_statistics.yml'
file_pass_withoutwarning = 'proj_pass_without_warning.txt'
file_pass_withwarning = 'proj_pass_with_warning.txt'
file_fail = 'proj_fail.txt'

def __search_atl():
    try:
        workbenchPath = os.environ['ATL_WORKBENCH']
    except KeyError:
        raise RuntimeError("ATL_WORKBENCH environment variable is not set.")

    return workbenchPath
   
def __get_projects_num(rootdir):
    proj_num = 0
    
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            filename_path = os.path.join(parent,filename)
            if re.search(r'\.project', filename_path):
                if filename_path.find('kds') != -1:
                    pass
                else:
                    proj_num = proj_num + 1

    return proj_num   

def _run_command(atl_path, filename_path, proj_name, build_mode):
    global projectbuild_pass_number
    global projectbuild_fail_number
    global projectbuild_warning_number
    has_warning = 0
    first_warning = 0

    import_path = ('/').join(filename_path.split('\\')[0:-1])
    import_path = import_path.replace('/','\\',2)

    if build_mode == 'debug':
        
        print '%s %s make %s' % (atl_path, filename_path, build_mode)
        sys.stdout.flush()

        atl_debug_tmp_log_path = os.getcwd() + '\\atl_debug_tmp_log.txt'
        atl_build_cmd = 'set path=%s;%s;%s && \
        "%s" --launcher.suppressErrors -nosplash -application "org.eclipse.cdt.managedbuilder.core.headlessbuild" -build "%s" -import "%s" -data "%s" >> %s 2>&1 ' % (
                atl_path + '/ide',
                atl_path + '/ARMTools/bin',
                '%SystemRoot%\system32;%SystemRoot%',
                atl_path + '/ide/TrueSTUDIO',
                proj_name + '/' + 'debug',
                import_path + '/',
                './',
                atl_debug_tmp_log_path
                ) 
        proj_name_withmode = proj_name + ' ' + build_mode
        debug_task = subprocess.Popen(atl_build_cmd, 0, stdin=None, stdout=None, stderr=None, shell = True)
        debug_ret = debug_task.wait()
        
        # If the project build failed
        if debug_ret != 0 :
            projectbuild_fail_number += 1
            atl_log_dic['projectbuild_fail_number'] = projectbuild_fail_number
            __error_log_filter(atl_debug_tmp_log_path, file_fail, proj_name_withmode)
            print 78*'X'
            print proj_name_withmode + ' ' + 'build failed' + '\n'
        # If the project build passed, find the warnings
        else : 
            has_warning = __warning_log_filter(atl_debug_tmp_log_path, file_pass_withwarning, proj_name_withmode)
            if has_warning == 1:
                projectbuild_warning_number += 1
                atl_log_dic['projectbuild_warning_number'] = projectbuild_warning_number
                print 78*'W'
                print proj_name_withmode + ' ' + 'build pass with warnings' + '\n'
            else:
                projectbuild_pass_number += 1
                atl_log_dic['projectbuild_pass_number'] = projectbuild_pass_number
                print proj_name_withmode + ' ' + 'build pass without warnings' + '\n'
                f_file_pass_withoutwarning = open(file_pass_withoutwarning, 'a')
                f_file_pass_withoutwarning.write(proj_name_withmode + '\n')
                f_file_pass_withoutwarning.close()

        os.remove(atl_debug_tmp_log_path)
    elif build_mode == 'release':
        
        print '%s %s make %s' % (atl_path, filename_path, build_mode)
        sys.stdout.flush()

        atl_release_tmp_log_path = os.getcwd() + '\\atl_release_tmp_log.txt'

        atl_build_cmd = 'set path=%s;%s;%s && \
        "%s" --launcher.suppressErrors -nosplash -application "org.eclipse.cdt.managedbuilder.core.headlessbuild" -build "%s" -import "%s" -data "%s" >> %s 2>&1 ' % (
                atl_path + '/ide',
                atl_path + '/ARMTools/bin',
                '%SystemRoot%\system32;%SystemRoot%',
                atl_path + '/ide/TrueSTUDIO',
                proj_name + '/' + 'release',
                import_path + '/',
                './',
                atl_release_tmp_log_path
                )

        proj_name_withmode = proj_name + ' ' + build_mode
        release_task = subprocess.Popen(atl_build_cmd, 0, stdin=None, stdout=None, stderr=None, shell = True)
        release_ret = release_task.wait()
        
        # If the project build failed
        if release_ret != 0 :
            projectbuild_fail_number += 1
            atl_log_dic['projectbuild_fail_number'] = projectbuild_fail_number
            __error_log_filter(atl_release_tmp_log_path, file_fail, proj_name_withmode)
            print 78*'X'
            print proj_name_withmode + ' ' + 'build failed' + '\n'
        # If the project build passed, find the warnings
        else : 
            has_warning = __warning_log_filter(atl_release_tmp_log_path, file_pass_withwarning, proj_name_withmode)
            if has_warning == 1:
                projectbuild_warning_number += 1
                atl_log_dic['projectbuild_warning_number'] = projectbuild_warning_number
                print 78*'W'
                print proj_name_withmode + ' ' + 'build pass with warnings' + '\n'
            else:
                projectbuild_pass_number += 1
                atl_log_dic['projectbuild_pass_number'] = projectbuild_pass_number
                print proj_name_withmode + ' ' + 'build pass without warnings' + '\n'
                f_file_pass_withoutwarning = open(file_pass_withoutwarning, 'a')
                f_file_pass_withoutwarning.write(proj_name_withmode + '\n')
                f_file_pass_withoutwarning.close()

        os.remove(atl_release_tmp_log_path) 
    
    elif build_mode == 'All':
        print '%s %s make %s' % (atl_path, filename_path, build_mode)
        sys.stdout.flush()

        atl_release_tmp_log_path = os.getcwd() + '\\atl_release_tmp_log.txt' 
        atl_debug_tmp_log_path = os.getcwd() + '\\atl_debug_tmp_log.txt' 

        atl_cmd_debug = 'set path=%s;%s;%s && \
        "%s" --launcher.suppressErrors -nosplash -application "org.eclipse.cdt.managedbuilder.core.headlessbuild" -build "%s" -import "%s" -data "%s" >> %s 2>&1 ' % (
                atl_path + '/ide',
                atl_path + '/ARMTools/bin',
                '%SystemRoot%\system32;%SystemRoot%',
                atl_path + '/ide/TrueSTUDIO',
                proj_name + '/' + 'debug',
                import_path + '/',
                './',
                atl_debug_tmp_log_path
                ) 

        atl_cmd_release = 'set path=%s;%s;%s && \
        "%s" --launcher.suppressErrors -nosplash -application "org.eclipse.cdt.managedbuilder.core.headlessbuild" -build "%s" -import "%s" -data "%s" >> %s 2>&1 ' % (
                atl_path + '/ide',
                atl_path + '/ARMTools/bin',
                '%SystemRoot%\system32;%SystemRoot%',
                atl_path + '/ide/TrueSTUDIO',
                proj_name + '/' + 'release',
                import_path + '/',
                './',
                atl_release_tmp_log_path
                )               
       
        debug_task = subprocess.Popen(atl_cmd_debug, 0, stdin=None, stdout=None, stderr=None, shell=True)
        debug_ret = debug_task.wait()
        release_task = subprocess.Popen(atl_cmd_release, 0, stdin=None, stdout=None, stderr=None, shell=True)
        release_ret = release_task.wait()
                
        # If the debug project build failed
        if debug_ret != 0 :
            proj_name_withmode = proj_name + ' ' + 'debug'
            projectbuild_fail_number += 1
            atl_log_dic['projectbuild_fail_number'] = projectbuild_fail_number
            __error_log_filter(atl_debug_tmp_log_path, file_fail, proj_name_withmode)
            print 78*'X'
            print proj_name_withmode + ' ' + 'build failed' + '\n'
        # If the project build passed, find the warnings
        else : 
            proj_name_withmode = proj_name + ' ' + 'debug'
            has_warning = __warning_log_filter(atl_debug_tmp_log_path, file_pass_withwarning, proj_name_withmode)
            if has_warning == 1:
                projectbuild_warning_number += 1
                atl_log_dic['projectbuild_warning_number'] = projectbuild_warning_number
                print 78*'W'
                print proj_name_withmode + ' ' + 'build pass with warnings' + '\n'
            else:
                projectbuild_pass_number += 1
                atl_log_dic['projectbuild_pass_number'] = projectbuild_pass_number
                print proj_name_withmode + ' ' + 'build pass without warnings' + '\n'
                f_file_pass_withoutwarning = open(file_pass_withoutwarning, 'a')
                f_file_pass_withoutwarning.write(proj_name_withmode + '\n')
                f_file_pass_withoutwarning.close()        
        
        # If the project build failed
        if release_ret != 0 :
            proj_name_withmode = proj_name + ' ' + 'release'
            projectbuild_fail_number += 1
            atl_log_dic['projectbuild_fail_number'] = projectbuild_fail_number
            __error_log_filter(atl_release_tmp_log_path, file_fail, proj_name_withmode)
            print 78*'X'
            print proj_name_withmode + ' ' + 'build failed' + '\n'
        # If the project build passed, find the warnings
        else : 
            proj_name_withmode = proj_name + ' ' + 'release'
            has_warning = __warning_log_filter(atl_release_tmp_log_path, file_pass_withwarning, proj_name_withmode)
            if has_warning == 1:
                projectbuild_warning_number += 1
                atl_log_dic['projectbuild_warning_number'] = projectbuild_warning_number
                print 78*'W'
                print proj_name_withmode + ' ' + 'build pass with warnings' + '\n'
            else:
                projectbuild_pass_number += 1
                atl_log_dic['projectbuild_pass_number'] = projectbuild_pass_number
                print proj_name_withmode + ' ' + 'build pass without warnings' + '\n'
                f_file_pass_withoutwarning = open(file_pass_withoutwarning, 'a')
                f_file_pass_withoutwarning.write(proj_name_withmode + '\n')
                f_file_pass_withoutwarning.close()
            
        os.remove(atl_release_tmp_log_path)
        os.remove(atl_debug_tmp_log_path)   

    # Update the file_proj_num_statistics
    f = open(file_proj_num_statistics,'w')
    yaml.dump(atl_log_dic, f)
    f.close()

if __name__ == '__main__':
    has_build = 0
    
    # Gets atl bin path
    atl_bin_path = __search_atl()
    
    # Gets the command line args
    the_args = __read_options()
    
    # Reads the build name for this time
    if the_args.buildname == None:
        print 'You need give a name for this build, the name can distinguish itself from next time build, such as python autobuild_atl_release_package -n frdmkxx -m debug'
        sys.exit()
    else:
        pass

    if the_args.rootdir == None:
        pass
    else:
        rootdir = the_args.rootdir        

    log_file_path_record = os.getcwd()
    log_file_path = os.getcwd() + '\\%s\\%s'% (the_args.buildname, 'atl') 
    # Checks wether the log_file_path already exists
    if os.path.exists(log_file_path):
        os.chdir(log_file_path)
        if os.path.exists(log_file_path + '\\%s' % file_proj_num_statistics):
            f = open(file_proj_num_statistics, 'r')
            atl_log_dic_tmp = yaml.load(f)
            if atl_log_dic_tmp:
                atl_log_dic = atl_log_dic_tmp.copy()
                if atl_log_dic.has_key('projectbuild_pass_number'):
                    projectbuild_pass_number = projectbuild_pass_number + atl_log_dic['projectbuild_pass_number']
                if atl_log_dic.has_key('projectbuild_warning_number'):
                    projectbuild_warning_number = projectbuild_warning_number + atl_log_dic['projectbuild_warning_number']
                if atl_log_dic.has_key('projectbuild_fail_number'):
                    projectbuild_fail_number = projectbuild_fail_number + atl_log_dic['projectbuild_fail_number']
                if atl_log_dic.has_key('progressbar_counter'):
                    progressbar_counter = progressbar_counter + atl_log_dic['progressbar_counter']
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
            # atl_project_path = dirname_path + atl_extension_name
            if re.search(r'\.project', filename_path):
                if filename_path.find('kds') != -1:
                    pass
                else:
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
                        # Get project name from the .project
                        file_project_path = ('\\').join(filename_path.split('\\')[0:-1]) + '\\.project'
                        dom = xml.dom.minidom.parse(filename_path)
                        cproject_root = dom.documentElement
                        tag_name = cproject_root.getElementsByTagName('name')
                        tag0_name = tag_name[0]
                        proj_name = tag0_name.firstChild.data
                        _run_command(atl_bin_path, filename_path , proj_name, build_mode)
                        
                        progressbar_counter = progressbar_counter + 1
                        print pb(progressbar_counter)
                        sys.stdout.flush()
                        atl_log_dic['progressbar_counter'] = progressbar_counter
                        # Update the file_proj_num_statistics
                        f = open(file_proj_num_statistics,'w')
                        yaml.dump(atl_log_dic, f)
                        f.close()
                        
                        f = open(path_whetherbuild, 'w')
                        f.write(identify_string)
                        f.close()
                        
                    else:
                        has_build = 0

    if os.path.isdir('./.metadata'):
        shutil.rmtree('./.metadata')

    # Output the log
    path_log_file = log_file_path_record + '\\%s\\atl_%s_build_log.txt' % (the_args.buildname, build_mode)
    __output_log(atl_log_dic, file_pass_withoutwarning, file_pass_withwarning, file_fail, path_log_file)
    # Returns to the up dir 
    os.chdir(log_file_path_record)
    shutil.rmtree(log_file_path)  

    print 78*'*'
    print 78*'*'
    print "Please refer the %s for the build log " % path_log_file