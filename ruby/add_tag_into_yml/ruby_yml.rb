#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "yaml"
require "find"

# file_path = "E:\\git_sdk_2.0_feature_common_generator\\mcu-sdk-2.0\\bin\\generator\\records\\lsdk\\sdk_example\\common\\demo_app_lpc.yml"
# new_file_path = "test_yml.yml"

exception_array = Array.new
rootdir = "E:\\git_sdk_2.0_feature_common_main_tag\\mcu-sdk-2.0\\"
demo_app_yml_path = "bin\\generator\\records\\ksdk\\sdk_example\\common\\demo_app.yml"

class RubyYml
    def initialize(ksdk_rootdir, yml_path)
        @ksdk_rootdir = ksdk_rootdir
        @yml_path = yml_path
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

    obj_main_tag = RubyYml.new(rootdir,demo_app_yml_path)
    # obj_main_tag.add_main_sub_tag()
    # obj_main_tag.add_sub_tag_usb("bin\\generator\\records\\ksdk\\usb_example\\twrk64f120m")
    obj_main_tag.add_sub_tag_sdk(demo_app_yml_path)

end

