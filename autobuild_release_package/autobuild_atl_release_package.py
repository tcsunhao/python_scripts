#!/ usr / bin / python
#Filename : autobuild_atl.py
#command line example:
#   python autobuild_atl.py debug 
#   python autobuild_atl.py release

import re,os,sys,time,subprocess,stat,shutil
import  xml.dom.minidom

pass_project_list = []
error_log_list = []
warning_log_list = []

# rootdir = r"E:\tmp\rc1\SDK_2.0_FRDM-K66F_all1\boards\frdmk66f\usb_host_audio_speaker\bm\atl"
rootdir = r"E:\tmp\rc1\SDK_2.0_FRDM-K66F_all2\boards\frdmk66f"
# rootdir = "E:\\tmp\\rc1\\SDK_2.0_FRDM-K66F_all1\\boards\\frdmk66f"
# rootdir = "E:\\git_sdk_2.0_feature_common\\mcu-sdk-2.0\\boards\\mapsks22\\usb_examples"
atl_pass_number = 0
atl_fail_number = 0
atl_warning_number = 0

has_warning = 0
first_warning = 1

def __search_atl():
    try:
        workbenchPath = os.environ['ATL_WORKBENCH']
    except KeyError:
        raise RuntimeError("ATL_WORKBENCH environment variable is not set.")

    return workbenchPath

def _run_command(cmd, filename):
    global atl_pass_number
    global atl_fail_number
    global atl_warning_number
    global has_warning
    global first_warning
    # print cmd
    task = subprocess.Popen(cmd, 0, stdin=None, stdout=None, stderr=None, shell=True)
    returncode = task.wait()
    f = open('./log.txt','r')   
    if returncode != 0: 
        print filename + " build failed",
        print "*"*76
        error_log_list.append(proj_name)
        for line in f:
            if line.find('error:') != -1:
                if line.find('ignored') != -1:
                    continue
                else:
                    error_log_list.append('    >> ' + line)
        f.close()
        atl_fail_number += 1
    else:
        first_warning = 1
        for line in f:
            if line.find('warning:') != -1:
                if line.find('ignored') != -1:
                    continue
                else:
                    has_warning = 1;
                    if first_warning :
                        warning_log_list.append(proj_name + ' build passed with warnings\n')
                        first_warning = 0;
                    warning_log_list.append('    >> ' + line)

        if has_warning == 1:
            atl_warning_number += 1
            has_warning = 0;        
            print proj_name + ' ' + 'build pass with warnings'
        else:
            atl_pass_number += 1
            pass_project_list.append(proj_name)
            print proj_name + ' ' + 'build pass without warnings'
    
    f.close()   
    os.remove('.\log.txt')

for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        filename_path = os.path.join(parent,filename)
        # atl_project_path = dirname_path + atl_extension_name
        if re.search(r'\.project', filename_path):
            if filename_path.find('kds') != -1:
                pass
            else:
                # print filename_path
                dom = xml.dom.minidom.parse(filename_path)
                cproject_root = dom.documentElement
                tag_name = cproject_root.getElementsByTagName('name')
                tag0_name = tag_name[0]
                proj_name = tag0_name.firstChild.data
                # print proj_name
                import_path = ('/').join(filename_path.split('\\')[0:-1])
                import_path = import_path.replace('/','\\',2)
                # print import_path
                atl_path = __search_atl()
                # print atl_path
                # atl_build_cmd = 'set path=%s;%s;%s && \
                # "%s" --launcher.suppressErrors -nosplash -application "org.eclipse.cdt.managedbuilder.core.headlessbuild" -build "%s" -import "%s" -data "%s" >> %s 2>&1 ' % (
                #         'C:\Program Files (x86)\Atollic\TrueSTUDIO for ARM 5.4.0/ide',
                #         'C:\Program Files (x86)\Atollic\TrueSTUDIO for ARM 5.4.0/ARMTools/bin',
                #         '%SystemRoot%\system32;%SystemRoot%',
                #         'C:\Program Files (x86)\Atollic\TrueSTUDIO for ARM 5.4.0/ide/TrueSTUDIO',
                #         proj_name + '/' + sys.argv[1],
                #         import_path + '/',
                #         './',
                #         './log.txt'
                #         )
                atl_build_cmd = 'set path=%s;%s;%s && \
                    "%s" --launcher.suppressErrors -nosplash -application "org.eclipse.cdt.managedbuilder.core.headlessbuild" -build "%s" -import "%s" -data "%s" >> %s 2>&1 ' % (
                            atl_path + '/ide',
                            atl_path + '/ARMTools/bin',
                            '%SystemRoot%\system32;%SystemRoot%',
                            atl_path + '/ide/TrueSTUDIO',
                            proj_name + '/' + sys.argv[1],
                            import_path + '/',
                            './',
                            './log.txt'
                            )
                # print atl_build_cmd
                print 'Building ' + proj_name + ' ' + sys.argv[1]
                sys.stdout.flush()
                _run_command(atl_build_cmd, proj_name)
                
if os.path.isdir('./.metadata'):
    shutil.rmtree('./.metadata')
# set path=C:\Freescale\atl_3.0.0/bin;C:\Freescale\atl_3.0.0/toolchain/bin;%SystemRoot%\system32;%SystemRoot% && 
            # "C:\Freescale\atl_3.0.0/eclipse/kinetis-design-studio" --launcher.suppressErrors -nosplash -application 
            # "org.eclipse.cdt.managedbuilder.core.headlessbuild" 
            # -build "host_audio_speaker_bm_mapsks22/debug" 
            # -import "E:\git_sdk_2.0_mainline\mcu-sdk-2.0/examples/mapsks22/usb/usb_host_audio_speaker/bm/atl/" -data "./" >> ./log.txt 2>&1
if os.path.exists("C:\\atl_build_log_file"):
    pass
else :
    os.mkdir("C:\\atl_build_log_file") 

f_final_log = open('C:\\atl_build_log_file\\final_log.txt','w')

print 30*'*' + 'BUILD RESULT' + 30*'*'
print >> f_final_log, 30*'*' + 'BUILD RESULT' + 30*'*'
print '%s' %(atl_pass_number) + ' projects build passed without warnings:\n'
print >> f_final_log, '%s' %(atl_pass_number) + ' projects build passed without warnings:\n'
print '%s' %(atl_warning_number) + ' projects build passed with warning:\n'
print >> f_final_log,'%s' %(atl_warning_number) + ' projects build passed with warning:\n'
print '%s' %(atl_fail_number) + ' projects build failed\n'
print >> f_final_log, '%s' %(atl_fail_number) + ' projects build failed:\n'

if atl_pass_number != 0:
    print 'The passed projects without warning are :'
    print >> f_final_log, 'The passed projects without warning are :'
    for mem in pass_project_list:
        print '  ' + mem + '\n',
        print >> f_final_log, '  ' + mem

print >> f_final_log, '\n'
print >> f_final_log, 68*'*'

if atl_warning_number != 0 :
    print '\n'
    print 'The warning log is :' 
    print >> f_final_log, 'The warning log is :' 
    for mem in warning_log_list:
        print '  ' + mem + '\n',
        print >> f_final_log, '  ' + mem

print >> f_final_log, '\n'
print >> f_final_log, 68*'*'

if atl_fail_number != 0 :
    print 'The error log is :' 
    print >> f_final_log, 'The error log is :' 
    for mem in error_log_list:
        print '  ' + mem + '\n',
        print >> f_final_log, '  ' + mem
 
 
f_final_log.close()

print 78*'*'
print 78*'*'
print "Please refer the C:\\atl_build_log_file\\final_log.txt for the build log"