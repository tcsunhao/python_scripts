#!/ usr / bin / python
#Filename : autobuild_kds.py
#command line example:
#   python autobuild_kds.py debug 
#   python autobuild_kds.py release

import re,os,sys,time,subprocess

pass_project_list = []
error_log_list = []

# rootdir = "E:\\tmp\\rc1\\SDK_2.0_FRDM-K66F_all\\boards\\frdmk66f"
rootdir = "E:\\tmp\\rc1\\SDK_2.0_FRDM-K66F_all1\\boards\\frdmk66f"
kds_pass_number = 0
kds_fail_number = 0

def _run_command(cmd, filename):
    global kds_pass_number
    global kds_fail_number
    # print cmd
    task = subprocess.Popen(cmd, 0, stdin=None, stdout=None, stderr=None, shell=True)
    returncode = task.wait()
    if returncode != 0: 
        print filename + " build failed",
        print "*"*76
        error_log_list.append(proj_name)
        f = open('./log.txt','r')   
        for line in f:
            if line.find('error:') != -1:
                error_log_list.append('    >> ' + line)
        f.close()
        kds_fail_number += 1
    else:
        print filename + " build passed",
        print '\n'
        kds_pass_number += 1
        pass_project_list.append(proj_name)    


for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        filename_path = os.path.join(parent,filename)
        # kds_project_path = dirname_path + kds_extension_name
        if re.search(r'wsd',filename_path):
            # print filename_path
            proj_name = filename_path.split('\\')[-1].split('.')[0]
            import_path = ('/').join(filename_path.split('\\')[0:-1])
            import_path = import_path.replace('/','\\',2)
            print import_path
            kds_build_cmd = 'set path=%s;%s;%s && \
            "%s" --launcher.suppressErrors -nosplash -application "org.eclipse.cdt.managedbuilder.core.headlessbuild" -build "%s" -import "%s" -data "%s" >> %s 2>&1 ' % (
                    'C:\Freescale\KDS_3.0.0/bin',
                    'C:\Freescale\KDS_3.0.0/toolchain/bin',
                    '%SystemRoot%\system32;%SystemRoot%',
                    'C:\Freescale\KDS_3.0.0/eclipse/kinetis-design-studio',
                    proj_name + '/' + sys.argv[1],
                    import_path + '/',
                    './',
                    './log.txt'
                    )
            print kds_build_cmd
            print 'Building ' + proj_name + ' ' + sys.argv[1]
            sys.stdout.flush()
            _run_command(kds_build_cmd, proj_name)


# set path=C:\Freescale\KDS_3.0.0/bin;C:\Freescale\KDS_3.0.0/toolchain/bin;%SystemRoot%\system32;%SystemRoot% && 
            # "C:\Freescale\KDS_3.0.0/eclipse/kinetis-design-studio" --launcher.suppressErrors -nosplash -application 
            # "org.eclipse.cdt.managedbuilder.core.headlessbuild" 
            # -build "host_audio_speaker_bm_mapsks22/debug" 
            # -import "E:\git_sdk_2.0_mainline\mcu-sdk-2.0/examples/mapsks22/usb/usb_host_audio_speaker/bm/kds/" -data "./" >> ./log.txt 2>&1

print 30*'*' + 'BUILD RESULT' + 30*'*'
print '%s' %(kds_pass_number) + ' projects build passed:\n'
for mem in pass_project_list:
    print mem
print '\n'
print '%s' %(kds_fail_number) + ' projects build failed\n'
if kds_fail_number != 0 :
    print 'The error log is :\n' 
    for mem in error_log_list:
        print mem,
 