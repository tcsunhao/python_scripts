#!/ usr / bin / python
#Filename : autobuild_kds.py
#command line example:
#   python autobuild_kds.py debug 
#   python autobuild_kds.py release

import re,os,sys,time,subprocess,shutil
from log_filter import __warning_log_filter, __error_log_filter, __output_log

rootdir = r"E:\tmp\rc1\SDK_2.0_FRDM-K66F_all\boards\frdmk66f"

pass_project_list = []
warning_log_list = []
error_log_list = []

kds_pass_number = 0
kds_warning_number = 0
kds_fail_number = 0

def __search_kds():
    try:
        workbenchPath = os.environ['KDS_WORKBENCH']
    except KeyError:
        raise RuntimeError("KDS_WORKBENCH environment variable is not set.")
    return workbenchPath

def _run_command(cmd, proj_name):
    global kds_pass_number
    global kds_fail_number
    global kds_warning_number

    task = subprocess.Popen(cmd, 0, stdin=None, stdout=None, stderr=None, shell=True)
    returncode = task.wait()

    if returncode != 0: 
        kds_fail_number += 1
        error_log_list.append(proj_name + ' build failed\n')
        __error_log_filter('tmp_log.txt', error_log_list)
        print 78*'X'
        print filename + ' ' + 'build failed' + '\n'
    else:
        has_warning = __warning_log_filter('tmp_log.txt', warning_log_list, proj_name)
        if has_warning == 1:
            kds_warning_number += 1
            print 78*'W'
            print filename + ' ' + 'build pass with warnings' + '\n'
        else:
            kds_pass_number += 1
            print filename + ' ' + 'build pass without warnings' + '\n'
            pass_project_list.append(proj_name + '\n')
        
    os.remove('tmp_log.txt')

for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        filename_path = os.path.join(parent,filename)
        # kds_project_path = dirname_path + kds_extension_name
        if re.search(r'wsd',filename_path):
            # print filename_path
            proj_name = filename_path.split('\\')[-1].split('.')[0]
            import_path = ('/').join(filename_path.split('\\')[0:-1])
            import_path = import_path.replace('/','\\',2)
            # print import_path
            kds_path = __search_kds()
            # print kds_path
            kds_build_cmd = 'set path=%s;%s;%s && \
            "%s" --launcher.suppressErrors -nosplash -application "org.eclipse.cdt.managedbuilder.core.headlessbuild" -build "%s" -import "%s" -data "%s" >> %s 2>&1 ' % (
                    kds_path + '/bin',
                    kds_path + '/toolchain/bin',
                    '%SystemRoot%\system32;%SystemRoot%',
                    kds_path + '/eclipse/kinetis-design-studio',
                    proj_name + '/' + sys.argv[1],
                    import_path + '/',
                    './',
                    './tmp_log.txt'
                    )
            # print kds_build_cmd
            print 'Building ' + proj_name + ' ' + sys.argv[1]
            sys.stdout.flush()
            _run_command(kds_build_cmd, proj_name)

if os.path.isdir('./.metadata'):
    shutil.rmtree('./.metadata')
# set path=C:\Freescale\KDS_3.0.0/bin;C:\Freescale\KDS_3.0.0/toolchain/bin;%SystemRoot%\system32;%SystemRoot% && 
            # "C:\Freescale\KDS_3.0.0/eclipse/kinetis-design-studio" --launcher.suppressErrors -nosplash -application 
            # "org.eclipse.cdt.managedbuilder.core.headlessbuild" 
            # -build "host_audio_speaker_bm_mapsks22/debug" 
            # -import "E:\git_sdk_2.0_mainline\mcu-sdk-2.0/examples/mapsks22/usb/usb_host_audio_speaker/bm/kds/" -data "./" >> ./log.txt 2>&1
log_member = (kds_pass_number, kds_warning_number, kds_fail_number, pass_project_list, warning_log_list, error_log_list, )

# Create log file
path_log_file = rootdir + '\\kds_build_log.txt'
f_final_log = open(path_log_file,'w')

__output_log(log_member, f_final_log)

f_final_log.close()

print 78*'*'
print 78*'*'
print "Please refer the %s for the build log " % path_log_file