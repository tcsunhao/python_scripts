#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "yaml"

file = "E:\\sun_project\\python_scripts\\ruby\\yaml\\drivers.yml"

begin
    content = File::read(file.gsub("\\","/"))
    content = YAML::load(content.gsub("\\", "/"))
    content['__load__'].each do |loadfile|
        puts loadfile
    end
rescue 
    puts "Please check whether the file exists."
end
