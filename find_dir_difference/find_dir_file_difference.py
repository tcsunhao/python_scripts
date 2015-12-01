# !/ usr / bin / python
# Filename : find_dir_difference.py
# command line example:
#   python find_dir_difference.py 

import re,os,sys,time,subprocess,filecmp

dir_a = 'E:\\sun_project\\python_test\\test0'
dir_b = 'E:\\sun_project\\python_test\\test1'

is_same = True

both_have = []
differnt_files = []
only_a_have = []
only_b_have = []

dir_a_list = dir_a.split('\\')
dir_b_list = dir_b.split('\\')

for parent,dirnames,filenames in os.walk(dir_a):
    for filename in filenames:
        filename_path = os.path.join(parent,filename)
        dir_b_copy_list = dir_b_list[:]
        
        # Get the corresponding file path in dir b 
        dir_a_file_path_list = filename_path.split('\\')
        dir_a_file_path_alone_list = [i for i in dir_a_file_path_list if i not in dir_a_list]
        dir_b_copy_list.extend(dir_a_file_path_alone_list)
        dir_b_possible_path = "\\".join(dir_b_copy_list)
        dir_file_path_alone_list = dir_a_file_path_alone_list[:]
        dir_file_path_alone = "\\".join(dir_file_path_alone_list)
        
        # Whether the file exits
        if os.path.exists(dir_b_possible_path) == True:
            both_have.append(dir_file_path_alone)
            if filecmp.cmp(dir_b_possible_path, filename_path) == False:
                differnt_files.append(dir_file_path_alone)
                is_same = False
        else:
            is_same = False
            only_a_have.append(dir_file_path_alone)

for parent,dirnames,filenames in os.walk(dir_b):
    for filename in filenames:
        filename_path = os.path.join(parent,filename)
        dir_a_copy_list = dir_a_list[:]
        
        # Get the corresponding file path in dir b 
        dir_b_file_path_list = filename_path.split('\\')
        dir_b_file_path_alone_list = [i for i in dir_b_file_path_list if i not in dir_b_list]
        dir_a_copy_list.extend(dir_b_file_path_alone_list)
        dir_a_possible_path = "\\".join(dir_a_copy_list)
        dir_file_path_alone_list = dir_b_file_path_alone_list[:]
        dir_file_path_alone = "\\".join(dir_file_path_alone_list)
        
        # Whether the file exits
        if os.path.exists(dir_a_possible_path) == True:
            both_have.append(dir_file_path_alone)
        else:
            is_same = False
            only_b_have.append(dir_file_path_alone)

if is_same == True:
    print 'The two directors are the same.'
else:
    if len(differnt_files):
        print 78*'*'
        print 'The following files are differnt between two dirs :'
        for mem in differnt_files:
            print mem

    if len(only_a_have):
        print 78*'*'
        print 'The following files only exit in dir a: '
        for mem in only_a_have:
            print mem
    
    if len(only_b_have):
        print 78*'*'
        print 'The following files only exit in dir b: '
        for mem in only_b_have:
            print mem

