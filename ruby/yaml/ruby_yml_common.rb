#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "yaml"

# file_path = "E:\\git_sdk_2.0_feature_common_generator\\mcu-sdk-2.0\\bin\\generator\\records\\ksdk\\sdk_example\\common\\demo_app.yml"
file_path = "meta_component_exception.yml"

exception_array = Array.new

begin
    content = File::read(file_path.gsub("\\","/"))
    content = YAML::load(content.gsub("\\", "/"))
    puts content.class
    content.each do |k, v|
        puts k
        puts v.class    
    end
end
