#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "nokogiri"
require "rubygems"

xml_path = ""

begin
    meta_doc = Nokogiri::XML(File.open("fsl_gpio.meta")) {|f| f.noblanks}
    component_node = meta_doc.xpath('//metadata/components/component')
    puts meta_doc
    puts component_node
end