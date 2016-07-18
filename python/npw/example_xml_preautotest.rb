#!/usr/bin/ruby 
# -*- coding : utf-8 -*-
# 

require "Find"
require "fileutils"
require 'optparse'

class ExampleXmlPreautotest
    def initialize()
        @sdk2_repo_path = "E:/git_sdk_2.0_rel/mcu-sdk-2.0"
        @release_package_path = ""
        @sdk_board = ""
        @option = ""
    end

    def all_example_xml_action()
        process_cmdargs()
        if @option == "copyxml"
            copy_example_xml()
        elsif @option == "deletexml"
            delete_example_xml()
        elsif @option == "checkxml"
            check_example_xml_in_relpackage()
        end
    end

    def delete_example_xml()
        projects_file_path = @release_package_path + "/boards/" + @sdk_board
        Find.find(projects_file_path).each do |each_path|
            if each_path.include?("example.xml")
                File.delete(each_path)
            end
        end
    end

    def copy_example_xml()
        sdk_repo_board_path = @sdk2_repo_path + '/boards/' + @sdk_board
       
        unless File.exist?(sdk_repo_board_path)
             raise "#{sdk_repo_board_path} doesn't exists. "
        end
       
        Find.find(sdk_repo_board_path).each do |each_path|
            if each_path.include?("example.xml")
                target_relpackage_project_example_xml_path = each_path.gsub(/#{@sdk2_repo_path}\/boards/, @release_package_path + "/boards")
                target_relpackage_project_example_xml_dir_path = File.dirname(target_relpackage_project_example_xml_path)
                if File.exist?(target_relpackage_project_example_xml_dir_path)
                    FileUtils.cp(each_path, target_relpackage_project_example_xml_path)
                else
                    puts "#{target_relpackage_project_example_xml_dir_path} doesn't exists. "
                end
            end
        end
    end

    def check_example_xml_in_relpackage()
        projects_file_path = @release_package_path + "/boards/" + @sdk_board
        unless File.exist?(projects_file_path)
             raise "#{projects_file_path} doesn't exists. "
        end

        Find.find(projects_file_path).each do |each_path|
            # If there is a "readme.txt", there should be a example.xml
            if each_path.include?("readme.txt")
                # Get the example.xml path
                example_xml_path  = each_path.split('/')[0 ... -1].push('example.xml').join('/')
                unless File.exists?(example_xml_path)
                    puts "#{example_xml_path} doesn't exists."
                end
            end
        end
    end

    def process_cmdargs()
        opt_parser = OptionParser.new do | opts |
            opts.on("-b", "--board", "The sdk board name, like twrkv58f220m") do | value |
                @option = "copyxml"
            end  
            opts.on("-c", "--copy", "Copy the example.xml file") do | value |
                @option = "copyxml"
            end            
            opts.on("-d", "--delete", String, "Delete all the example.xml files") do | value |
                @option = "deletexml"
            end
            opts.on("-v", "--check", String, "Check if every folder has an example.xml") do | value |
                @option = "checkxml"
            end
            opts.on("-r", "--release package path", String, "Release package path") do | value |
                @release_package_path = value.gsub(/\\/,"/")
            end
            opts.on("-s", "--sdk repo path",String, "Sdk2.0 git repo path") do | value |
                @sdk2_repo_path = value.gsub(/\\/,"/")
            end            
            opts.on("-h", "--help", "print this help") do
                puts(opts)
                exit(0)
            end
        end
        opt_parser.parse!
    end

end

if __FILE__ == $0
    obj = ExampleXmlPreautotest.new()
    obj.all_example_xml_action()
end

