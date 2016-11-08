#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "nokogiri"
require "rubygems"

root = "E:/git_sdk_2.0_feature_common/mcu-sdk-2.0/boards/frdmk64f/demo_apps/hello_world/example.xml"
# root = "example.xml"

macro_array = ['DEBUG', 'CPU_MK64FN1M0VMD12', 'FSL_RTOS_FREE_RTOS','PRINTF_FLOAT_ENABLE=1']

begin

    xmlpath = './tmp.xml'

    project_definition_xml = Nokogiri::XML(File.open("./hello_world.xml")) {|f| f.noblanks}
    # puts project_definition_xml
    project_node = project_definition_xml.at_xpath("/examples/example/projects/project[@nature=\"org.eclipse.cdt.core.cnature\"]")
    
    unless project_node == nil
        project_node['nature'] = "org.eclipse.cdt.core.ccnature"
    end
    # puts project_node['nature']
    # option_node.each do |each|
    #     if each.content.empty?
    #         each.remove
    #     end
    # end
    # option_node.children().each do |each|
    # option_node.each do |each|
    #     puts "**"
    #     puts each
    # end
    # toolchainSetting_node.children().each do |child|
    #     puts "***"
    #     puts child
    # end
    # if cc_defsymbols_node_debug == nil
    #     puts 'nil'
    # else
    #     macro_array.each do |each|
    #         macro_node = Nokogiri::XML::Node.new("value", cc_defsymbols_node_debug)
    #         macro_node.content = each 
    #         cc_defsymbols_node_debug << macro_node
    #     end

    File.open(xmlpath, "w") do |f|
        f.write(project_definition_xml.to_xml(:encoding => "UTF-8"))
    end    
    # end
end