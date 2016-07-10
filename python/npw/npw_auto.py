"""
File:  npw_auto.py
=================
Copyright (c) 2016 Freescale Semiconductor

"""
import os
import re
import argparse
import shutil, stat
import datetime
from xml.etree import ElementTree as ET
import yaml


DEBUG = False
KDS_STUDIO_PARENT_PATH = "C:\\Freescale\\KDS_V3"
BACKUP_FOLDER = '_backup'

class KSDKPackageGroup():
    CURRENT_PATH = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')
    SEARCH_FOLDER_MAX_LEVER = 3
    UNZIP_DETAILED_LOG = 'unzip_log.txt'

    def __init__(self, path):
        self.sdk_zip_package_list = []
        self.sdk_package_list = []

    def search_SDK_zip_packages(self, root_folder, level, ws_patch):
        if level > KSDKPackageGroup.SEARCH_FOLDER_MAX_LEVER: return
        for item in os.listdir(root_folder):
            ab_path = os.path.join(root_folder, item)
            if os.path.isfile(ab_path):
                if ws_patch is not None:
                    if ab_path == ws_patch: continue

                if ab_path.endswith('.zip') or ab_path.endswith('.tar.gz'):
                    self.sdk_zip_package_list.append(ab_path)
            elif os.path.isdir(ab_path):
                if BACKUP_FOLDER not in ab_path:
                    self.search_SDK_zip_packages(ab_path, level + 1, ws_patch)


    def unzip_SDK_packages(self, root_folder, force_replace, ws_patch):
        # print how many SDK packages will be unzipped
        print 'The following packages will be unzipped for testing:\n'
        count = 0
        for package_path in self.sdk_zip_package_list:
            count = count + 1
            print str(count) + ' ' + package_path

        # remove the unzip log
        try:
            if os.path.exists(KSDKPackageGroup.UNZIP_DETAILED_LOG):
                os.remove(KSDKPackageGroup.UNZIP_DETAILED_LOG)
        except Exception,e:
            print 'Fail to remove ' + KSDKPackageGroup.UNZIP_DETAILED_LOG
            print e

        # start unzip
        for package_path in self.sdk_zip_package_list:
            parent_folder_path = os.path.split(package_path)[0]
            folder_name = os.path.splitext(package_path)[0]

            target_folder = os.path.join(parent_folder_path, folder_name)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            else:
                if not force_replace:
                    print 'Skip unzip because it has been unzipped: ' + target_folder
                    continue

            if DEBUG: print 'unzipping ' + folder_name + ' in path: ' + parent_folder_path

            cmd = ''
            cmd_ws = ''
            if package_path.endswith('.zip'):
                cmd = 'unzip -o ' + package_path + ' -d ' + target_folder + \
                        ' >> ' + KSDKPackageGroup.UNZIP_DETAILED_LOG

                if ws_patch is not None:
                    cmd_ws = 'unzip -o ' + ws_patch + ' -d ' + target_folder
            elif package_path.endswith('.tar.gz'):
                cmd = 'tar -zxvf ' + package_path + ' -C ' + target_folder + \
                        ' >> ' + KSDKPackageGroup.UNZIP_DETAILED_LOG

                if ws_patch is not None:
                    cmd_ws = 'tar -zxvf ' + ws_patch + ' -C ' + target_folder + \
                            ' >> ' + KSDKPackageGroup.UNZIP_DETAILED_LOG
            try:
                if DEBUG: print 'execute the command: ' + cmd + ', ws: ' + cmd_ws
                print 'Unzipping the package ' + package_path + ' ...... '
                os.system(cmd)

                if ws_patch is not None:
                    os.system(cmd_ws)
            except Exception, e:
                print 'Fatal to call os.system() for command: ' + cmd + ', ws: ' + cmd_ws


    def search_SDK_packages(self, root_folder, level):
        if level > KSDKPackageGroup.SEARCH_FOLDER_MAX_LEVER: return

        for SDK_root in os.listdir(root_folder):
            ab_path = os.path.join(root_folder, SDK_root)
            if os.path.isdir(ab_path):

                is_SDK_package = False
                for SDK_root_file in os.listdir(ab_path):
                    if re.match('.+_manifest.xml', SDK_root_file):
                        self.sdk_package_list.append(ab_path)
                        if DEBUG: print "Found SDK package: " + SDK_root
                        is_SDK_package = True
                        break

                if not is_SDK_package:
                    if BACKUP_FOLDER not in ab_path:
                        self.search_SDK_packages(ab_path, level + 1)

        return self.sdk_package_list


class NPWGenerator():
    METADATA_FOLDER = '.metadata'
    REMOTE_TEMP_FOLDER = 'RemoteSystemsTempFiles'
    PRE_NAME_PRJ = 'prj'
    BUILD_RESULT_FILE = 'build_result.yml'
    FAILURE_CASE_FILE = 'failure_case_log.yml'

    def __init__(self, studio_path, workspace, version):
        self.studio_path = studio_path
        self.workspace = workspace
        self.version = version
        self.packages = []

    def clean_env(self):
        # to keep the history and quicken the backup, just move legacy projects to a backup folder
        time_folder_name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        target_path = os.path.join(os.path.join(self.workspace, BACKUP_FOLDER), time_folder_name)
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        Utility.move_tree(self.workspace, target_path)


    def move_temp_file_to(self, ksdk_path):
        pkg_folder_name = os.path.basename(ksdk_path)
        target_path = os.path.join(self.workspace, pkg_folder_name)

        if not os.path.exists(target_path):
            print target_path + ' does not exist, skip moving!'
            return

        # finally move the tempfolder and metadata to folder
        for item in os.listdir(self.workspace):
            path_item = os.path.join(self.workspace, item)

            # to avoid duplicate case in chips and boards, we need exclude metadata and remote temp files folder
            if os.path.isdir(path_item) and \
                (NPWGenerator.METADATA_FOLDER == item or NPWGenerator.REMOTE_TEMP_FOLDER == item):
                shutil.move(path_item, target_path)


    def move_projects_to(self, package_name):
        target_path = os.path.join(self.workspace, package_name)
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        for item in os.listdir(self.workspace):
            path_item = os.path.join(self.workspace, item)

            # to avoid duplicate case in chips and boards, we need exclude metadata and remote temp files folder
            if os.path.isdir(path_item) and re.match('^'+ NPWGenerator.PRE_NAME_PRJ, item):
                shutil.move(path_item, target_path)
    
    def generate_cloned_projects(self, ksdk_path):
        cmd = os.path.join(self.studio_path, 'kinetis-design-studio.exe') + ' -newSdkPrj:' + \
            NPWGenerator.PRE_NAME_PRJ + '{@utotest:c,' + 'example' + '} -sdkPath4npw:' + ksdk_path

        try:
            has_error = os.system(cmd)

            # just warning but continue
            if has_error: print 'Warning: errors to execute ' + cmd

            # move to a parent folder name to avoid same chip project name for FRDM-XXX and TWR-XXX
            pkg_folder_name = os.path.basename(ksdk_path)
            self.move_projects_to(pkg_folder_name)

        except Exception, e:
                print e

    def scan_packages(self):
        for folder in os.listdir(self.workspace):
            folder_path = os.path.join(self.workspace, folder)
            if not os.path.isdir(folder_path): continue

            if re.match('\..+', folder): continue #skip the hide folder, such as .metadata
            if BACKUP_FOLDER == folder: continue
            if NPWGenerator.REMOTE_TEMP_FOLDER == folder: continue # skip the remote folder

            package = KDSProjectsGroup(self.studio_path, folder_path)
            package.scan_projects()

            self.packages.append(package)


    def build(self):
        for package in self.packages:
            package.build_all()

    def report_summary(self, only_failue_log):
        result = {}

        total_casenum = 0
        pass_casenum = 0
        for package in self.packages:
            total_casenum += package.get_casenum()
            pass_casenum += package.get_passnum()

        pass_rate = 0.0
        if total_casenum != 0: pass_rate = (pass_casenum * 1.0 /total_casenum) * 100.0

        summary = 'NPW version -- ' + self.version
        fail_casenum = total_casenum - pass_casenum
        if only_failue_log:
            summary += ' ,failure case number -- ' + str(fail_casenum)
        else:
            summary += ' ,total -- ' + str(total_casenum) + ', fail or warning -- ' + str(fail_casenum) + \
                    ', pass -- ' + str(pass_casenum) + ', pass rate -- ' + str(pass_rate) + '%'

        result['### Test Report ###'] = summary

        for package in self.packages:
            package.report_result(result, only_failue_log)

        if not only_failue_log: # print summary in console
            print yaml.dump(result, default_flow_style=False)

        log_file = NPWGenerator.FAILURE_CASE_FILE if only_failue_log else NPWGenerator.BUILD_RESULT_FILE
        with open(os.path.join(self.workspace, log_file), 'w') as yaml_file:
            yaml_file.write( yaml.dump(result, default_flow_style=False))


class KDSProjectsGroup():
    def __init__(self, studio_path, root_path):
        self.studio_path = studio_path
        self.root_path = root_path
        self.name = os.path.basename(root_path)
        self.projects_list = []

    def scan_projects(self):
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if '.project' == file:
                    if re.search(NPWGenerator.REMOTE_TEMP_FOLDER, root) or \
                        re.search(NPWGenerator.METADATA_FOLDER, root):
                        continue #skip the KDS temp folder and meta folder

                    kds_project = KDSProject(self.studio_path, root)
                    self.projects_list.append(kds_project)

    def build_all(self):
        for project in self.projects_list:
            project.build()

    def get_casenum(self):
        return len(self.projects_list)

    def get_passnum(self):
        pass_num = 0
        for project in self.projects_list:
            if project.is_pass(): pass_num +=1

        return pass_num

    def get_failnum(self):
        fail_num = 0
        for project in self.projects_list:
            if not project.is_pass(): fail_num +=1

        return fail_num

    def report_result(self, result, only_failue_log):
        failnum = self.get_failnum()
        if only_failue_log and failnum <= 0:
            return  # no need report the details failure log if no failure cases

        key = self.name + '(Fail-' + str(failnum) + ',Total-' + str(self.get_casenum()) + ')'
        if key not in result:
            result[key] = {}

        for project in self.projects_list:
            project_result = {}
            is_case_pass = True

            for config in project.configs:
                ret = project.build_result[config]

                if only_failue_log:
                    if ret != KDSProject.BUILD_RESULT_PASS:
                        is_case_pass = False

                        project_result[config] = ret
                        # attached the detailed log
                        build_log_file = KDSProject.get_build_log_file(project.project_path, config)
                        content = []
                        with open(build_log_file, 'r') as log_file:
                            for line in log_file:
                                content.append(line.strip('\n'))
                        project_result[config + '_' + 'log'] = content
                else:
                    project_result[config] = ret

            # only include the failure cases log if only_failure_log is set
            if not only_failue_log or not is_case_pass:
                result[key][project.project_name] = project_result


class KDSProject():
    BUILD_RESULT_PASS = "PASS"
    BUILD_RESULT_FAIL = "FAIL"
    BUILD_RESULT_WARNING = "WARNING"
    BUILD_RESULT_UNKNOWN = "UNKNOWN"

    DEBUG_CONFIG = 'Debug'
    RELEASE_CONFIG = 'Release'
    BUILD_LOG_FILE_NAME = "build.log"

    TEMP_WORK_SPACE = 'C:\\TEMP\\KDS_Workspace'

    def __init__(self, studio_path, project_path):
        self.studio_path = studio_path
        self.project_path = project_path
        self.project_name = self.parser_name()
        self.build_result = {}
        self.configs = []

    def parser_name(self):
        project_name = ""
        project_file = os.path.join(self.project_path, '.project')
        with open(project_file, 'r') as pfile:
            tree = ET.parse(pfile)
            node = tree.find('name')
            project_name = node.text.strip()

        return project_name


    def check_configs(self):
        cproject_file = os.path.join(self.project_path, '.cproject')
        with open(cproject_file, 'r') as cpfile:
            tree = ET.parse(cpfile)
            nodes = tree.findall('storageModule/cconfiguration/storageModule')
            for node in nodes:
                try:
                    config = node.attrib['name'].strip()
                    if KDSProject.DEBUG_CONFIG.lower() == config.lower()\
                         or KDSProject.RELEASE_CONFIG.lower() == config.lower():
                        self.configs.append(config)
                        self.build_result[config] = KDSProject.BUILD_RESULT_UNKNOWN

                except Exception, e:
                    pass


    def build(self):
        self.check_configs()
        if len(self.configs) <= 0:
            print 'Error: cprojects has not debug and release configuration, cannot execute build task!'
            return

        for config in self.configs:
            self.build_with_config(config)

    def is_pass(self):
        is_pass = True
        for config in self.configs:
            if self.build_result[config] != KDSProject.BUILD_RESULT_PASS:
                is_pass = False

        return is_pass


    @staticmethod
    def get_build_log_file(project_path, config):
        return os.path.join(project_path, config + '_' + KDSProject.BUILD_LOG_FILE_NAME)

    def build_with_config(self, config):
        # try to clean the temp workspace first
        try:
            print 'cleaning ' + KDSProject.TEMP_WORK_SPACE
            shutil.rmtree(KDSProject.TEMP_WORK_SPACE)
        except Exception, e:
            pass

        kds_studio = os.path.join(self.studio_path, 'kinetis-design-studio.exe')
        auto_compile_option = ' --launcher.suppressErrors -nosplash -application "org.eclipse.cdt.managedbuilder.core.headlessbuild" -build '
        case = '"' + self.project_name + '/' + config + '"'
        build_log_file = KDSProject.get_build_log_file(self.project_path, config)

        cmd = kds_studio + auto_compile_option + case + ' -import "' + self.project_path + \
                '" -data "' + KDSProject.TEMP_WORK_SPACE + '" > ' + build_log_file + ' 2>&1'

        try:
            self.build_result[config] = KDSProject.BUILD_RESULT_PASS # initial the build result as PASS

            print 'start building ' + self.project_path
            not_succeed = os.system(cmd)

            if not_succeed: self.build_result[config] = KDSProject.BUILD_RESULT_FAIL
            with open(build_log_file, 'r') as log_file:
                for line in log_file:
                    print line  #print the build log in console
                    if not not_succeed:
                        if re.search('\s+Error\s+', line) or re.search('\s+error\s+', line):
                            self.build_result[config] = KDSProject.BUILD_RESULT_FAIL
                        elif (re.search('\s+Warning\s*', line) or re.search('\s+warning\s+', line))\
                                and KDSProject.BUILD_RESULT_PASS == self.build_result[config]:
                            self.build_result[config] = KDSProject.BUILD_RESULT_WARNING

        except Exception, e:
            print e

class Utility():
    @staticmethod
    def copytree(src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            if re.match('\..+', item): continue #skip the hide folder, such as .metadata

            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

    @staticmethod
    def remove_readonly(func, path, excinfo):
        #removes readonly tag from files/folders so they can be deleted
        if func in (os.rmdir, os.remove):
            os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
            func(path)
        else:
            raise

    @staticmethod
    def move_tree(src, dst):
        for item in os.listdir(src):
            if BACKUP_FOLDER == item: continue #skip the backup folder

            s = os.path.join(src, item)
            d = os.path.join(dst, item)

            try:
                shutil.move(s, d)
            except Exception, e:
                # try again
                shutil.move(s,d)


if __name__ == '__main__':

    # parser the arguments
    parser = argparse.ArgumentParser(description='Process the command for batch test')
    parser.add_argument('-p', action='store', required=True, dest='parent_path', \
                        help='Specify the parent path of whole KEx packages')
    parser.add_argument('-w', action='store', required=True, dest='kds_workspace', \
                        help='Specify the KDS workspace path, which is used to store the NPW projects')
    parser.add_argument('-v', action='store', required=True, dest='npw_version', \
                        help='Specify the NPW version number to be tested.')
    parser.add_argument('-kds', action='store', required=False, dest='kds_root', \
                        help='Specify the KDS install path')
    parser.add_argument('-z', action='store_true', default=False, dest='unzip_packages', \
                        help='Unzip all KEx packages if they have not been unzipped')
    parser.add_argument('-f', action='store_true', default=False, dest='force_replace', \
                        help='Unzip all KEx packages even they have been unzipped')
    parser.add_argument('-ws', action='store', required=False, dest='ws_patch', \
                        help='Specify the patch with WS part number')
    parser.add_argument('-b', action='store_true', default=False, dest='build', \
                        help='auto build the projects that generated by NPW')
    arguments = parser.parse_args()


    # check parent folder first
    if not os.path.isdir(arguments.parent_path):
        print arguments.parent_path + " is not a directory!"
        exit()

    if not os.path.exists(arguments.parent_path):
        print arguments.parent_path + " does not exist!"
        exit()

    if not arguments.kds_root:
        arguments.kds_root = KDS_STUDIO_PARENT_PATH

    if not os.path.exists(arguments.kds_root):
        print arguments.kds_root + " does not exist! Please set the path with command -kds !"
        exit()


    ########################
    # KSDK Package operation
    ########################
    ksdk_pkg_group = KSDKPackageGroup(arguments.parent_path)

    if arguments.unzip_packages:
        ksdk_pkg_group.search_SDK_zip_packages(arguments.parent_path, 1, arguments.ws_patch)
        ksdk_pkg_group.unzip_SDK_packages(arguments.parent_path, arguments.force_replace, arguments.ws_patch)

    # search and get all SDK packages need to be tested
    sdk_package_list = ksdk_pkg_group.search_SDK_packages(arguments.parent_path, 1)


    ########################
    # NPW operation
    ########################
    npw = NPWGenerator(os.path.join(arguments.kds_root, 'eclipse'), arguments.kds_workspace, arguments.npw_version)

    for package_path in sdk_package_list:
        npw.generate_cloned_projects(package_path)

        npw.move_temp_file_to(package_path)





