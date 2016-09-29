#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "yaml"
require "find"

# file_path = "E:\\git_sdk_2.0_feature_common_generator\\mcu-sdk-2.0\\bin\\generator\\records\\lsdk\\sdk_example\\common\\demo_app_lpc.yml"
# new_file_path = "test_yml.yml"

exception_array = Array.new
rootdir = "E:\\git_sdk_2.0_mainline\\mcu-sdk-2.0\\"
demo_app_yml_path = "bin\\generator\\records\\ksdk\\sdk_example\\common\\demo_app.yml"
driver_yml_path = "bin\\generator\\records\\ksdk\\lib\\lib_sdk\\common\\drivers\\drv_gpio.yml"
driver_yml_dir_path = "bin\\generator\\records\\ksdk\\lib\\lib_sdk\\common\\cmsis_driver\\"
ksdk_yml_dir_path = "bin\\generator\\records\\ksdk\\usb_example\\common"
ksdk_yml_dir_path = "bin\\generator\\records\\ksdk\\sdk_unittest/common/unit_test"
lsdk_lib_yml_dir_path = "bin\\generator\\records\\lsdk\\lib\\lib_sdk\\common\\"
ksdk_lib_yml_dir_path = "bin\\generator\\records\\ksdk\\lib\\lib_sdk\\common\\"

class RubyYml
    def initialize(ksdk_rootdir, yml_path)
        @ksdk_rootdir = ksdk_rootdir
        @yml_path = yml_path
        @exception_release_dir = Array.new()
        @reg_app_h = /\/app/
        @reg_hardware = /\/hardware_init/
    end
    
    def add_sub_tag_usb(dir_path)

        Find.find(@ksdk_rootdir + dir_path) do |filename|
            next if File.directory?(filename)
            next if ".yml" != File.extname(File.basename(filename))
            arr = Array.new()

            # app.h
            File.open(filename, "r") do |file|
                index_array = Array.new()
                arr = file.readlines()
                # Notes the last line, should be a blank one
                line_num = -1
                arr.each do |each|
                    line_num += 1
                    if each.include?("app.h")
                        index_array.push(line_num + 2)
                    end                                       
                end

                index_array.each do |each|
                    arr.insert(each + index_array.index(each), "          merge-to-main : sub\n")                        
                end               
            end            

            File.open(filename, "w") do |file|
                arr.each do |each|
                    file.write(each)
                end
            end

            # appclock.h
            File.open(filename, "r") do |file|
                index_array = Array.new()
                arr = file.readlines()
                # Notes the last line, should be a blank one
                line_num = -1
                arr.each do |each|
                    line_num += 1
                    if each.include?("appclock.h")
                        index_array.push(line_num + 2)
                    end                                       
                end

                index_array.each do |each|
                    arr.insert(each + index_array.index(each), "            merge-to-main : sub\n")                        
                end               
            end            

            File.open(filename, "w") do |file|
                arr.each do |each|
                    file.write(each)
                end
            end     

            # hardware_init.c
            File.open(filename, "r") do |file|
                index_array = Array.new()
                arr = file.readlines()
                # Notes the last line, should be a blank one
                line_num = -1
                arr.each do |each|
                    line_num += 1
                    if each.include?("hardware_init.c")
                        index_array.push(line_num + 2)
                    end                                       
                end

                index_array.each do |each|
                    arr.insert(each + index_array.index(each), "            merge-to-main : sub\n")                        
                end               
            end            

            File.open(filename, "w") do |file|
                arr.each do |each|
                    file.write(each)
                end
            end                   
        end
    end

    def add_sub_tag_sdk(yml_path)
        arr = Array.new()
        filename = @ksdk_rootdir + yml_path
        puts filename
        # app.h
        
        File.open(filename, "r") do |file|
            index_array = Array.new()
            arr = file.readlines()
            # Notes the last line, should be a blank one
            line_num = -1
            arr.each do |each|
                line_num += 1
                if each.match(@reg_app_h) and (not each.include?("/apps/"))
                    index_array.push(line_num + 1)
                end                                       
            end

            index_array.each do |each|
                arr.insert(each + index_array.index(each), "        merge-to-main : sub\n")                        
            end               
        end            

        File.open(filename, "w") do |file|
            arr.each do |each|
                file.write(each)
            end
        end

        # hardware_init.c
        File.open(filename, "r") do |file|
            index_array = Array.new()
            arr = file.readlines()
            # Notes the last line, should be a blank one
            line_num = -1
            arr.each do |each|
                line_num += 1
                if each.match(@reg_hardware)
                    index_array.push(line_num + 1)
                end                                       
            end

            index_array.each do |each|
                arr.insert(each + index_array.index(each), "        merge-to-main : sub\n")                        
            end               
        end            

        File.open(filename, "w") do |file|
            arr.each do |each|
                file.write(each)
            end
        end                   
    end    
    
    def add_main_sub_tag()
        begin
            @exception_main = Array.new()
            @exception_app_h = Array.new()
            @exception_hardware = Array.new()

            content = File::read((@ksdk_rootdir + @yml_path).gsub("\\","/"))
            content = YAML::load(content.gsub("\\", "/"))
            content.each do |k, v|
                next if k == "__hierarchy__"
                find_main = false
                # find_hardware = false
                # find_app = false
                v['modules'].each do |demo, k_demo|
                    if k_demo.has_key?('files')
                        k_demo['files'].each do |each_source|
                            src_path = @ksdk_rootdir + each_source["source"]
                            # Find the main.c
                            if ".c" == File.extname(src_path)
                                if true == is_main_file(src_path) 
                                    find_main = true
                                    each_source["merge-to-main"] = "main"
                                end
                            end

                            # if File.basename(src_path) =~ reg_hardware
                            #     find_hardware = true
                            #     each_source["merge-to-main"] = "sub"
                            # end

                            # if File.basename(src_path) =~ reg_app_h
                            #     find_app = true
                            #     each_source["merge-to-main"] = "sub"
                            # end
                        end
                    end
                end

                if false == find_main
                    @exception_main.push(k)
                end
                # if false == find_app
                #     @exception_app_h.push(k)
                # end
                # if false == find_hardware
                #     @exception_hardware.push(k)
                # end
            end

            puts "The following examples don't have 'main.c' : " 
            puts @exception_main.inspect

            # puts "The following examples don't have 'app.h' : " 
            # puts @exception_app_h.inspect

            # puts "The following examples don't have 'hardware_init' : " 
            # puts @exception_hardware.inspect

            YAML::dump(content, File.open((@ksdk_rootdir + @yml_path).gsub("\\","/"),'w'))
        end

    end 

    def add_releasedir_tag(dir)
        @exception_release_dir = Array.new()
        dir = (@ksdk_rootdir + dir).gsub("\\","/")
        Dir.glob("#{dir}**/*").each do |filename|
            next if !File.file?(filename)
            if filename =~ /drv_.+yml/
                puts filename
                # add_releasedir_tag_meta_single_yml(filename)
                add_releasedir_tag_single_yml(filename)
            end 
        end

        @exception_release_dir.each do |each|
            puts each
        end
    end

    def add_releasedir_tag_meta_single_yml(yml_path)
        begin 
            content = File::read(yml_path.gsub("\\","/"))
            content = YAML::load(content.gsub("\\", "/"))
            drivername = nil
            content.each do |k, v|
                v['modules'].each do |driver, driver_content|
                    drivername = driver
                    if driver_content.has_key?("virtual-dir")
                        virtualdir = driver_content["virtual-dir"]
                        driver_content.delete("virtual-dir")
                    end

                    driver_content['files'].each do |each_source|
                        unless each_source.has_key?("virtual-dir") 
                            each_source["virtual-dir"] = virtualdir
                        end 
                    end

                    key = driver_content['files'][0]["source"].split('.')[0] + ".meta"
                    driver_meta_path = @ksdk_rootdir + key
                    if File::exists?(driver_meta_path)
                        driver_content['files'].push({"source" => key})
                    else
                        driver_content['files'].push({"source" => key})
                        unless @exception_release_dir.include?({yml_path=>"add meta"})  
                            @exception_release_dir.push({yml_path=>"add meta"})  
                        end
                    end
                end
                # Add attribute : hidden for meta file
                v['modules'].each do |driver, driver_content|
                    driver_content['files'].each do |each_source|
                        if File::extname(File::basename(each_source["source"])) == ".meta"
                            each_source["attribute"] = "hidden"
                        end 
                    end
                end
            end
        rescue
            unless @exception_release_dir.include?({yml_path=>"add meta"})  
                @exception_release_dir.push({yml_path=>"add meta"})  
            end
        end
        YAML::dump(content, File.open((yml_path).gsub("\\","/"),'w'))
    end

    def add_releasedir_tag_single_yml(yml_path)
        begin
            content = File::read(yml_path.gsub("\\","/"))
            content = YAML::load(content.gsub("\\", "/"))
            drivername = nil
            content.each do |k, v|
                v['modules'].each do |driver, driver_content|
                    drivername = driver
                    # include path
                    driver_content["cc-include"].each do |each_include|
                        unless each_include.has_key?("release-dir")
                            each_include["release-dir"] = "devices/${platform_devices_soc_name}/drivers"
                        end
                    end
                    
                    if driver_content.has_key?('files')
                        driver_content['files'].each do |each_source|
                            if each_source["source"].include?("platform/drivers")
                                unless each_source.has_key?("release-dir")
                                    each_source["release-dir"] = "devices/${platform_devices_soc_name}/drivers"
                                end
                            else
                                unless @exception_release_dir.include?({yml_path=>"add tag"}) 
                                    @exception_release_dir.push({yml_path=>"add tag"})  
                                end
                            end
                        end
                    end
                end
            end
        rescue
            unless @exception_release_dir.include?({yml_path=>"add tag"}) 
                @exception_release_dir.push({yml_path=>"add tag"})  
            end
        end
        YAML::dump(content, File.open(yml_path.gsub("\\","/"),'w'))
    end   

    def add_content_afterfind(dir, target)
        dir = (@ksdk_rootdir + dir).gsub("\\","/")
        Dir.glob("#{dir}/**/*").each do |filename|
            next if !File.file?(filename)
            if File.extname(filename) == ".yml"
                content = ""
                File.open(filename,"r") {|f| content = f.readlines}
                file = File.open(filename,"w")
                content.each do |line|
                    file.puts line                 
                    if line.include?("add_free")
                        file.puts("  - ksdk/shared/add_misc_utilities.yml")
                    end
                end
            end 
        end

    end

    def check_whether_meta_exist(dir)
        @array_wrong_meta_path = Array.new() 
        @array_meta_exception = Array.new()
        dir = (@ksdk_rootdir + dir).gsub("\\","/")
        Dir.glob("#{dir}**/*").each do |filename|
            next if !File.file?(filename)
            if File.extname(filename) == ".yml"
                begin
                    content = File::read(filename.gsub("\\","/"))
                    content = YAML::load(content.gsub("\\", "/"))
                    content.each do |k, v|
                        v['modules'].each do |driver, driver_content|
                            
                            if driver_content.has_key?('files')
                                driver_content['files'].each do |each_source|
                                    if File.extname(each_source["source"]) == ".meta"
                                        meta_path = (@ksdk_rootdir + each_source["source"]).gsub('\\','/')
                                        unless File.exists?(meta_path)
                                            unless @array_wrong_meta_path.include?(filename + ' ' + meta_path) 
                                                @array_wrong_meta_path.push(filename + ' ' + meta_path)  
                                            end                       
                                        end 
                                    end
                                end
                            end
                        end
                    end
                rescue
                    @array_meta_exception.push(filename)
                end

            end 
        end
        puts "*****************"
        @array_wrong_meta_path.each do |each|
            puts each
        end

        puts "*****************"
        @array_meta_exception.each do |each|
            puts each
        end
    end

    private
    def is_main_file(path)
        return true if path.include?("main.c")
        if File.exist?(path)
            IO.foreach(path) do |line|
                return true if line.match(/^.*\smain(\s)?\(.*\)$/)
            end
        end
        return false
    end
end


if __FILE__ == $0

    obj_releasedir_tag = RubyYml.new(rootdir,"")
    # obj_releasedir_tag.add_releasedir_tag(lsdk_lib_yml_dir_path)
    obj_releasedir_tag.check_whether_meta_exist(lsdk_lib_yml_dir_path)
    # obj_releasedir_tag.add_releasedir_tag_single_yml(rootdir + driver_yml_path)
    # obj_releasedir_tag.add_releasedir_tag_meta_single_yml(rootdir + driver_yml_path)
end