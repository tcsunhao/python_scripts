#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "nokogiri"
require "rubygems"

xml_path = ""

begin
    meta_doc = Nokogiri::XML(File.open("./hello_world.meta")) {|f| f.noblanks}
    example_node = meta_doc.at_xpath('//examples')
    puts meta_doc
    puts example_node
end