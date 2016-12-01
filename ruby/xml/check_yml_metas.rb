#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "nokogiri"
require "rubygems"
require "yaml"
require "find"

class XmlCommonPracticeForSDK

    def initialize()
        @sdk_root_dir = "E:\\git_sdk_2.0_mainline\\mcu-sdk-2.0"
    end

    def check_ymls_metas()
        @lib_path_array = [
            "bin\\generator\\records\\lsdk\\lib\\lib_sdk\\common\\drivers",
            "bin\\generator\\records\\lsdk\\lib\\lib_sdk\\common\\cmsis_drivers",
            "bin\\generator\\records\\ksdk\\lib\\lib_sdk\\common\\drivers",
            "bin\\generator\\records\\ksdk\\lib\\lib_sdk\\common\\cmsis_driver"
        ] 

        @fail_path = Array.new()

        @lib_path_array.each do |each_lib_path|
            Find.find(File.join(@sdk_root_dir, each_lib_path).gsub!('\\','/')) do |filepath|
                begin    
                    next if File::directory?(filepath)
                    content = File::read(filepath)
                    content = YAML::load(content.gsub("\\", "/"))
                    content.each do |k, v|
                        if k == "__hierarchy__"
                            @fail_path.push(filepath)
                            next
                        end
                        v['modules'].each do |driver_name, driver_content|
                            yml_meta_component = driver_content['meta-component']
                            driver_content['files'].each do |each_source|
                                src_path = each_source['source']
                                if '.meta' == File.extname(src_path) 
                                    meta_path = File.join(@sdk_root_dir, src_path).gsub('\\','/')
                                    if File.exist?(meta_path)
                                        meta_root_node = Nokogiri::XML(File.open(meta_path)) {|f| f.noblanks}
                                        component_nodeset = meta_root_node.xpath("//metadata/components/component[@description]")
                                        find = false
                                        component_nodeset.each do |each_node|
                                            if each_node['name'] == yml_meta_component
                                                find = true
                                                next
                                            end
                                        end
                                        unless find
                                            @fail_path.push(filepath)
                                        end
                                    else
                                        @fail_path.push(filepath)
                                    end
                                end
                            end
                        end
                    end
                rescue 
                    @fail_path.push(filepath)
                end
            end
        end

        unless @fail_path.empty?
            puts "********** failed list ************"
            @fail_path.each do |each|
                puts each
            end
        end
    end
end

if __FILE__ == $0
    object = XmlCommonPracticeForSDK.new()
    object.check_ymls_metas
end
