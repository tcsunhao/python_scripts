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
path3 = "middleware/wolfssl/wolfssl/wolfcrypt/arc4.h"
board = "twrkl82z72m"
path4 = "CMSIS/Driver/Include/Driver_USART.h"
line = " -Xlinker --gc-sections -Xlinker -static -Xlinker -z -Xlinker muldefs"

if __FILE__ == $0

    # puts File.dirname(path4)
    # case File.dirname(path4)
    # when /^\/?boards\/#{board}\/(\w*)\/\w*\/startup$/
    #     puts $1
    #     puts 'startup'  
    # when /^\/?boards\/#{board}\/(\w*)\/(\w*)\/startup\/(?<devices_subfolder>iar|arm|gcc)/
    #     puts $~[:devices_subfolder]       
    # when /^\/?(rtos|middleware)\/(?<prefix>\w*)\/(?<relpath>.*)/
    #     puts $~[:prefix]
    #     puts $~[:relpath]
    # when /^\/?CMSIS\/Driver\/Include/
    #     puts 'CMSIS/Driver/Include'        
    # end
    pattern = /\s-Xlinker\s(\S+)/
    result  = line.match(pattern)
    puts result.inspect
    puts result.class    
end




# puts "*******************"
# path3.gsub!(/middleware/, 'rtos')
# puts path3

# path4 = "His height 175.00cm and weight 60.00kg."
# puts path4
# path4.gsub! /(\d+\.\d+)(\w+)/ do |matched|
#     puts $1
#     # puts $2
#     "%g%s" % [$1, $2]
# end
# puts path4
