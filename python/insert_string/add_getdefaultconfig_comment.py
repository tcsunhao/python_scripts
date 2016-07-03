# !/usr/bin/python
# Filename : add_getdefaultconfig_comment.py
# Note the \boards\src\demo_apps\mbedtls\mbedtls_benchmark\benchmark.c

import re,os,sys,time,subprocess,fnmatch,json

rootdir = r"E:\git_sdk_2.0_feature_common\mcu-sdk-2.0\boards"

comment_jason = file('default_config.json');
comment_dic = json.load(comment_jason)
comment_jason.close()

first_line = '    /*\n'
last_line = '     */\n'

file_content_list = []
line_index = 0
tmp_list = []
find_target = 0

for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        filename_path = os.path.join(parent,filename)
        if fnmatch.fnmatch(filename_path, "*.c"):
            f_handler = open(filename_path, 'r')
            
            for line in f_handler.readlines():
                # line number start from 1, not 0
                line_index = line_index + 1
                file_content_list.append(line)

                # find the 'GetDefaultConfig' line
                if re.search(r'GetDefaultConfig', line) != None :
                    searchobj = re.search(r'\w*GetDefaultConfig', line)
                    
                    if re.search(r'(&)(.*)(\));',line) != None:
                        searchobj_configname = re.search(r'(&)(.*)(\));',line)
                        # print searchobj_configname.group(2)
                        dic_key = searchobj.group(0)
                        # Get the dic key value
                        if comment_dic.has_key(dic_key) == True: 
                            find_target = 1
                            comment_string = comment_dic.get(dic_key, '')
                            # print comment_string
                            comment_list = comment_string.split('\n')
                            # Add the '/*' and '*/' in the front and end
                            comment_list.insert(0, first_line)
                            comment_list.append(last_line)
                            comment_list_len = len(comment_list)
                            list_num = 1
                            for mem in comment_list:
                                if list_num == 1 or list_num == comment_list_len :
                                    pass
                                else:
                                    tmp = mem.split('->')
                                    tmp[0] = searchobj_configname.group(2)
                                    # print tmp
                                    mem = ('.').join(tmp)
                                    mem = '     * ' + mem + '\n'
                                list_num = list_num + 1
                                pos = line_index - 1
                                file_content_list.insert(pos, mem)
                                line_index = line_index + 1
                        else:
                            find_target = 0
                            print 'Not found in the json file : ' + dic_key
                            print filename_path
                            print '\n'
                    else:
                        print 78*'*'
                        print 'Mismatch, cannot update the structurer variable name in the :'
                        print filename_path
                        print 78*'*'


            # Close file
            f_handler.close() 
            
            if find_target == 1:
                # Reopen file to move the file offset to 0
                f_handler = open(filename_path, 'w')
                for mem in file_content_list:
                    f_handler.write(mem)
                f_handler.close()
            else:
                pass

            # Clean for next loop
            file_content_list = []
            line_index = 0
            find_target = 0