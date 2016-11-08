#!/ usr / bin / python
#Filename : autobuild_mcux_release_package.py
#command line example:
# python autobuild_mcux_release_package.py -n mcux 


import re,os,sys,time,subprocess,shutil,yaml
import xml.dom.minidom
from aux_tool import ProgressBar, __warning_log_filter, __error_log_filter, __read_options,__output_log

build_properties_path = r'E:\\sun_project\\python_scripts\\python\\autobuild_release_package\\build_properties'

projectbuild_pass_number = 0
projectbuild_warning_number = 0
projectbuild_fail_number = 0

mcux_log_dic = {}
mcux_xml_dic = []

passed_project_record_list = []
failed_project_record_list = []

proj_num = 0
proj_built_num = 0
build_mode = 'Debug'
progressbar_counter = 0
identify_string = ''

def __search_mcux():
    try:
        workbenchPath = os.environ['MCUX_WORKBENCH']
    except KeyError:
        raise RuntimeError("MCUX_WORKBENCH environment variable is not set.")
    return workbenchPath

if __name__ == '__main__':
    has_build = 0
    
    # Gets mcux bin path
    mcux_bin_path = __search_mcux()
    
    # Gets the command line args
    the_args = __read_options()
    
    project_list_file_path = the_args.proj_listfile
    with open(project_list_file_path,'r') as f:
        for line in f:
            mcux_xml_dic.append(line.strip())

    for example_xml_path in mcux_xml_dic:
        example_xml_path = ('\\\\').join(example_xml_path.split('/')) + '\n'
        project_name = ('_').join(example_xml_path.split('\\\\')[-3:-1])
        if os.path.exists(build_properties_path) == True:
            config_path = 'build.properties'
            tmp_log_path = 'mcux_tmp.txt'
            f = open(build_properties_path,'r')
            with open(config_path, 'w+') as f_tmp:
                for line in f:
                    if 'example.xml' in line:
                        f_tmp.write('example.xml = ' + example_xml_path)
                    elif 'standalone' in line:
                        if the_args.standalone:
                            f_tmp.write('standalone = true\n')
                        else:
                            f_tmp.write('standalone = false\n')
                    else:
                        f_tmp.write(line)
            f.close()

            f_tmp_log = open(tmp_log_path,'w+')
            mcux_cmd = "mcuxpressoide -application com.nxp.mcuxpresso.headless.application -noSplash -data C:\\MCUXpressoIDE_0.0.0_166_alpha\\workspace -run example.build %s" % (config_path)
            mcux_task = subprocess.Popen(mcux_cmd, 0, stdin=None, stdout=f_tmp_log, stderr=f_tmp_log, shell=True)
            mcux_ret = mcux_task.wait()
            f_tmp_log.close()

            with open(tmp_log_path, 'r') as f_tmp_log:
                for line in f_tmp_log:
                    if 'Successfully built' in line:
                        projectbuild_pass_number = projectbuild_pass_number + 1
                        passed_project_record_list.append(project_name)
                        print 'Build %s successfully....' % (project_name)     
                        sys.stdout.flush()
                        break       
                    elif 'Unable to build' in line:
                        projectbuild_fail_number = projectbuild_fail_number + 1
                        failed_project_record_list.append(project_name)
                        print 'Build %s failed...' % (project_name)
                        sys.stdout.flush()
                        break       
                    
    file_log = the_args.buildname + '_buildlog.txt'
    f_log = open(file_log,'w')

    print 30*'*' + 'BUILD RESULT' + 30*'*'
    print >> f_log, 30*'*' + 'BUILD RESULT' + 30*'*'
    print '%s' %(projectbuild_pass_number) + ' projects build passed\n'
    print >> f_log, '%s' %(projectbuild_pass_number) + ' projects build passed\n'
    print '%s' %(projectbuild_fail_number) + ' projects build failed\n'
    print >> f_log, '%s' %(projectbuild_fail_number) + ' projects build failed\n'
    
    sys.stdout.flush()

    print >> f_log, '\n'
    print >> f_log, 68*'*'

    if projectbuild_pass_number != 0:
        print 'The passed projects are :'
        print >> f_log, 'The passed projects are :'
        for each in passed_project_record_list:
            print each
            print >> f_log, each

    print >> f_log, '\n'
    print >> f_log, 68*'*'

    sys.stdout.flush()
    
    if projectbuild_fail_number != 0:
        print 'The failed projects are :'
        print >> f_log, 'The failed projects are :'
        for each in failed_project_record_list:
            print each
            print >> f_log, each

    print >> f_log, '\n'
    print >> f_log, 68*'*'

    f_log.close()