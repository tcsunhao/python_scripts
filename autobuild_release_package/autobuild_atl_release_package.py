#!/ usr / bin / python
#Filename : autobuild_atl_release_package.py
#command line example:
#   python autobuild_atl_release_package.py debug 
#   python autobuild_atl_release_package.py release

import re,os,sys,time,subprocess,stat,shutil
import xml.dom.minidom
from log_filter import __warning_log_filter, __error_log_filter, __output_log

rootdir = r"E:\tmp\rc1\SDK_2.0_FRDM-K66F_all\boards\frdmk66f"

pass_project_list = []
warning_log_list = []
error_log_list = []

atl_pass_number = 0
atl_warning_number = 0
atl_fail_number = 0

def __search_atl():
    try:
        workbenchPath = os.environ['ATL_WORKBENCH']
    except KeyError:
        raise RuntimeError("ATL_WORKBENCH environment variable is not set.")

    return workbenchPath

def _run_command(cmd, proj_name):
    global atl_pass_number
    global atl_fail_number
    global atl_warning_number

    task = subprocess.Popen(cmd, 0, stdin=None, stdout=None, stderr=None, shell=True)
    returncode = task.wait()

    if returncode != 0: 
        atl_fail_number += 1
        error_log_list.append(proj_name + ' build failed\n')
        __error_log_filter('atl_tmp_log.txt', error_log_list)
        print 78*'X'
        print proj_name + ' ' + 'build failed' + '\n'
    else:
        has_warning = __warning_log_filter('atl_tmp_log.txt', warning_log_list, proj_name)
        if has_warning == 1:
            atl_warning_number += 1
            print 78*'W'
            print proj_name + ' ' + 'build pass with warnings' + '\n'
        else:
            atl_pass_number += 1
            print proj_name + ' ' + 'build pass without warnings' + '\n'
            pass_project_list.append(proj_name + '\n')
    
    os.remove('atl_tmp_log.txt')

for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        filename_path = os.path.join(parent,filename)
        # atl_project_path = dirname_path + atl_extension_name
        if re.search(r'\.project', filename_path):
            if filename_path.find('kds') != -1:
                pass
            else:
                # Get project name from the .project
                dom = xml.dom.minidom.parse(filename_path)
                cproject_root = dom.documentElement
                tag_name = cproject_root.getElementsByTagName('name')
                tag0_name = tag_name[0]
                proj_name = tag0_name.firstChild.data
                import_path = ('/').join(filename_path.split('\\')[0:-1])
                import_path = import_path.replace('/','\\',2)
                # print import_path
                atl_path = __search_atl()
                atl_build_cmd = 'set path=%s;%s;%s && \
                    "%s" --launcher.suppressErrors -nosplash -application "org.eclipse.cdt.managedbuilder.core.headlessbuild" -build "%s" -import "%s" -data "%s" >> %s 2>&1 ' % (
                            atl_path + '/ide',
                            atl_path + '/ARMTools/bin',
                            '%SystemRoot%\system32;%SystemRoot%',
                            atl_path + '/ide/TrueSTUDIO',
                            proj_name + '/' + sys.argv[1],
                            import_path + '/',
                            './',
                            './atl_tmp_log.txt'
                            )
                # print atl_build_cmd
                print 'Building ' + proj_name + ' ' + sys.argv[1]
                sys.stdout.flush()
                _run_command(atl_build_cmd, proj_name)
                
if os.path.isdir('./.metadata'):
    shutil.rmtree('./.metadata')
log_member = (atl_pass_number, atl_warning_number, atl_fail_number, pass_project_list, warning_log_list, error_log_list, )

# Create log file
path_log_file = rootdir + '\\atl_build_log.txt'
f_final_log = open(path_log_file,'w')

__output_log(log_member, f_final_log)

f_final_log.close()

print 78*'*'
print 78*'*'
print "Please refer the %s for the build log " % path_log_file