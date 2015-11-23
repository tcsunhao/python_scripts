#!/ usr / bin / python
#Filename : test0.py

import re,os,sys,time,subprocess,fnmatch
find_string = 0
main_content = []
relate_file = []
exception_list = []
exception_num = 0
# rootdir = "E:\\git_sdk_2.0_flexio_camera\\mcu-sdk-2.0\examples\\frdmk64f\\driver_examples\\enet\\txrx"
rootdir = "E:\\git_sdk_2.0_mainline\\mcu-sdk-2.0\\boards"
# rootdir = "E:\\git_dev_ksdk_1.2_ga_lite\\mcu-sdk-lite\\examples\\"
for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        filename_path = os.path.join(parent,filename)

        if fnmatch.fnmatch(filename_path, "*.c") or fnmatch.fnmatch(filename_path, '*.h') or fnmatch.fnmatch(filename_path, "*.dox"):
            # print filename_path
            f_handler = open(filename_path, 'r')
            for line in f_handler.readlines():
                if re.search(r'.*kPORT_PullDisable.*', line) != None :
                    find_string = 1
                    if (re.search(r'.*port_pin_config_t.*', line) != None) or \
                       (re.search(r'.*kPORT_PassiveFilterDisable.*', line) != None) or \
                       (re.search(r'.*kPORT_OpenDrainEnable.*', line) != None) or \
                       (re.search(r'.*kPORT_HighDriveStrength.*', line) != None) or \
                       (re.search(r'.*SlewRate.*', line) != None) :
                        exception_num += 1
                        exception_list.append(filename_path)
                        find_string = 0
                else :
                    main_content.append(line)
            f_handler.close()

            if(find_string == 1):
                f_handler = open(filename_path,'w')
                for line in main_content:
                    # print line,
                    f_handler.write(line)
                f_handler.close()
            find_string = 0            
            main_content = []

print "The exception number is " ,(exception_num)
for mem in exception_list :
    print mem