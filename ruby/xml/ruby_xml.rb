#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "nokogiri"
require "rubygems"

root = "E:/git_sdk_2.0_feature_common_generator/mcu-sdk-2.0/boards/frdmk64f/demo_apps/hello_world/example.xml"
# root = "example.xml"
begin
    meta_doc = Nokogiri::XML(File.open("./hello_world.meta")) {|f| f.noblanks}
    example_node = meta_doc.xpath('//metadata/components[@name="abc"]/component')
    # puts meta_doc
    example_node.each do |n|
        n['name'] = "xxxxxx"
    end

    File.open("tmp.meta", "w") { |file| file.puts(meta_doc.to_xml())}

    File.open(root, "w") do |f|
        f.write("hhhh")
    end 
end