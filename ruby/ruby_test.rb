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
istring2 = ["IAR", "GCC", "ARM", "keil"]
istring3 = ["IAR", "GCC", "ARM", "keil"]
file_path = "ruby_xml.rb"


path0 = "boards/twrkl82z72m/demo_apps/hello_world_qspi/startup/iar/startup_MKL82Z7.s"
path1 = "boards/twrkl82z72m/demo_apps/hello_world_qspi/startup/system_MKL82Z7.h"
path2 = "boards/twrkl82z72m/demo_apps/hello_world_qspi/startup/system_MKL82Z7.c"

line = " -g  -O0  -mcpu=cortex-m4  -Wall  -mfloat-abi=hard  -mfpu=fpv4-sp-d16  -fno-common  -ffunction-sections  -fdata-sections  -ffreestanding  -fno-builtin  -std=gnu99 "
board = "twrkl82z72m"

if __FILE__ == $0
    pattern = /\s-(O0|O1|O2|O3|Os|Og)\s/
    result  = line.match(pattern)
    puts result.class
end
