#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "yaml"

file_path = "E:\\git_sdk_2.0_feature_common_generator\\mcu-sdk-2.0\\bin\\generator\\records\\ksdk\\sdk_example\\common\\driver_example.yml"
# file_path = "E:\\git_sdk_2.0_feature_common_generator\\mcu-sdk-2.0\\bin\\generator\\records\\lsdk\\sdk_example\\common\\demo_app_lpc.yml"
new_file_path = "test_yml.yml"

exception_array = Array.new
rootdir = "E:/git_sdk_2.0_feature_common_generator/mcu-sdk-2.0/"
begin
    content = File::read(file_path.gsub("\\","/"))
    content = YAML::load(content.gsub("\\", "/"))
    content.each do |k, v|
        next if k == "__hierarchy__"
        has_example_readme = false
        has_board_readme = false

        example_readme_path = nil
        board_readme_path = nil

        v['modules'].each do |demo, k_demo|
            if k_demo.has_key?('files')
                k_demo['files'].each do |each_source|
                    src_path = each_source["source"]
                    if src_path.include?('boards/src/driver_examples') or src_path.include?('boards/src/rtos_examples') or src_path.include?('boards/src/mmcau_examples')
                        has_board_src = true
                        src_dir = File.dirname(src_path)
                        Dir.foreach(rootdir + src_dir) do |file|
                            if file.index(/\.readme/)
                                example_readme_path =  src_dir + '/' + file
                                has_example_readme = true
                                break
                            end
                        end
                        break
                    end
                end
            end
        end

        if has_example_readme == false
            unless exception_array.include?(k)
                exception_array.push(k)
            end
        end

        v['modules'].each do |demo, k_demo|
            if demo == "pinset"
                k_demo['files'].each do |each_source|
                    src_path = each_source['source']
                    if src_path.include?('hardware_init')
                        board_readme_path = File.dirname(src_path) + '/board.readme'
                        has_board_readme = true
                        break
                    end
                end
            end
        end

        if has_board_readme == false
            unless exception_array.include?(k)
                exception_array.push(k)
            end            
        end

        if board_readme_path!=nil or example_readme_path!=nil
            v['document']['readme'] = Array.new()
            if board_readme_path!=nil
                v['document']['readme'].push(board_readme_path)
            end
            if example_readme_path!=nil
                v['document']['readme'].push(example_readme_path)
            end
        end
    end

    YAML::dump(content, File.open(file_path.gsub("\\","/"),'w'))

    exception_array.each do |each|
        puts each
    end
end
