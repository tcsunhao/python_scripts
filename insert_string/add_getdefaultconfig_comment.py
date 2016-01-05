# !/usr/bin/python
# Filename : add_getdefaultconfig_comment.py

import re,os,sys,time,subprocess,fnmatch

rootdir = r"E:\git_sdk_2.0_release\mcu-sdk-2.0\boards\frdmk66f"

tmp_comment_list = []
tmp_comment_dic = {
                   'FTM_GetDefaultConfig': ['/*',' I am for the test FTM_GetDefaultConfig','*/'],
                   'I2C_MasterGetDefaultConfig': ['/*',' I am for the test I2C_MasterGetDefaultConfig','*/'],
                   'LPTMR_GetDefaultConfig': ['/*',' I am for the test LPTMR_GetDefaultConfig','*/']
                   }

file_content_list = []
line_index = 0
tmp_list = []

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
                    dic_key = searchobj.group(0)
                    # Get the dic key value 
                    tmp_comment_list = tmp_comment_dic.get(dic_key, '')
                    for mem in tmp_comment_list:
                        # add 4 space and 1 '\n', the 4 is from clang config file. 
                        mem = '    ' + mem + '\n'
                        pos = line_index - 1
                        file_content_list.insert(pos, mem)
                        line_index = line_index + 1
            
            # Close file
            f_handler.close() 
            # Reopen file to move the file offset to 0
            f_handler = open(filename_path, 'w')
            for mem in file_content_list:
                f_handler.write(mem)
            f_handler.close()

            # Clean for next loop
            file_content_list = []
            line_index = 0