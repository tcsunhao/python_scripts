#!/ usr / bin / python
#Filename : autobuild_kds.py
#command line example:
#   python autobuild_kds.py debug 
#   python autobuild_kds.py release

import re,os,sys,time,subprocess,shutil

pass_project_list = []
error_log_list = []
warning_log_list = []

# rootdir = "E:\\tmp\\rc1\\SDK_2.0_FRDM-K66F_all1\\boards\\frdmk66f"
# rootdir = r"E:\tmp\rc1\SDK_2.0_FRDM-K66F_all2\boards\frdmk66f"
# rootdir = r"E:\tmp\rc1\SDK_2.0_FRDM-K66F_all1\boards\frdmk66f\usb"
rootdir = r"E:\git_sdk_2.0_feature_common\mcu-sdk-2.0\boards\frdmk64f\usb_examples\usb_device_audio_generator"
# rootdir = "E:\\git_sdk_2.0_feature_common\\mcu-sdk-2.0\\boards\\mapsks22\\usb_examples"
kds_pass_number = 0
kds_fail_number = 0
kds_warning_number = 0

has_warning = 0
first_warning = 1

def __search_kds():
    try:
        workbenchPath = os.environ['KDS_WORKBENCH']
    except KeyError:
        raise RuntimeError("KDS_WORKBENCH environment variable is not set.")
    return workbenchPath

def _run_command(cmd, filename):
    global kds_pass_number
    global kds_fail_number
    global kds_warning_number
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
                    pass
                else:
                    error_log_list.append('    >> ' + line)
        f.close()
        kds_fail_number += 1
    else:
        first_warning = 1
        for line in f:
            if line.find('warning:') != -1:
                if line.find('ignored') != -1:
                    pass
                else:
                    has_warning = 1;
                    if first_warning :
                        warning_log_list.append(proj_name + ' build passed with warnings\n')
                        first_warning = 0;
                    warning_log_list.append('    >> ' + line)

        if has_warning == 1:
            kds_warning_number += 1
            has_warning = 0;        
            print proj_name + ' ' + 'build pass with warnings'
        else:
            kds_pass_number += 1
            pass_project_list.append(proj_name)
            print proj_name + ' ' + 'build pass without warnings'
    
    f.close()   
    os.remove('.\log.txt')

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
                    './log.txt'
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
if os.path.exists("C:\\kds_build_log_file"):
    pass
else :
    os.mkdir("C:\\kds_build_log_file") 

f_final_log = open('C:\\kds_build_log_file\\final_log.txt','w')

print 30*'*' + 'BUILD RESULT' + 30*'*'
print >> f_final_log, 30*'*' + 'BUILD RESULT' + 30*'*'
print '%s' %(kds_pass_number) + ' projects build passed:\n'
print >> f_final_log, '%s' %(kds_pass_number) + ' projects build passed:\n'
print '%s' %(kds_warning_number) + ' projects build passed with warning:\n'
print >> f_final_log,'%s' %(kds_warning_number) + ' projects build passed with warning:\n'
print '%s' %(kds_fail_number) + ' projects build failed\n'
print >> f_final_log, '%s' %(kds_fail_number) + ' projects build failed:\n'

if kds_pass_number != 0:
    print 'The passed projects without warning are :'
    print >> f_final_log, 'The passed projects without warning are :'
    for mem in pass_project_list:
        print '  ' + mem + '\n',
        print >> f_final_log, '  ' + mem

print >> f_final_log, '\n'
print >> f_final_log, 68*'*'

if kds_warning_number != 0 :
    print '\n'
    print 'The warning log is :' 
    print >> f_final_log, 'The warning log is :' 
    for mem in warning_log_list:
        print '  ' + mem + '\n',
        print >> f_final_log, '  ' + mem

print >> f_final_log, '\n'
print >> f_final_log, 68*'*'

if kds_fail_number != 0 :
    print 'The error log is :' 
    print >> f_final_log, 'The error log is :' 
    for mem in error_log_list:
        print '  ' + mem + '\n',
        print >> f_final_log, '  ' + mem
 
 
f_final_log.close()

print 78*'*'
print 78*'*'
print "Please refer the C:\\kds_build_log_file\\final_log.txt for the build log"