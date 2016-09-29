#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "yaml"
require "find"
require "optparse"
require "pathname"
require 'set'

dir = "E:\\sun_project\\python_scripts\\ruby"
tool = "iar"
istring1 = ["IAR", "GCC", "ARM"]
file_path = "ruby_xml.rb"


path0 = "boards/twrkl82z72m/demo_apps/hello_world_qspi/startup/iar/startup_MKL82Z7.s"
path1 = "boards/twrkl82z72m/demo_apps/hello_world_qspi/startup/system_MKL82Z7.h"
path2 = "boards/twrkl82z72m/demo_apps/hello_world_qspi/startup/system_MKL82Z7.c"

board = "twrkl82z72m"

if __FILE__ == $0
    # puts File.dirname(path0)
    # case File.dirname(path0)
    # when /^\/?boards\/#{board}\/(\w*)\/\w*\/startup$/
    #     puts $1
    #     puts 'startup'  
    # when /^\/?boards\/#{board}\/(\w*)\/(\w*)\/startup\/(?<devices_subfolder>iar|arm|gcc)/
    #     # puts $1
    #     # puts $2
    #     puts $~[:devices_subfolder]       
    # when /^\/?(rtos|middleware)\/(?<prefix>\w*)_(\w|\.)*(\/(?<relpath>.*))?/
    # end
    # # 
    # # array_a = ["example"]
    # # array_b = ["readme"]
    # # array_c = array_a + array_b
    # # puts array_c.inspect   
    # 
    str = "I am Holt."
    p str.is_a?(String) 
    p str.is_a?(Object) 
    p str.instance_of?(String) 
end
