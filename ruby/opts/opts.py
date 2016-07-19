#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "yaml"
require "find"
require "optparse"


file = "E:\\sun_project\\python_scripts\\ruby\\xml"
tool = "iar"
istring1 = ["IAR", "GCC", "ARM"]


if __FILE__ == $0
    options = {}
    option_parser = OptionParser.new do |opts|
        opts.banner = "Here is the help message for the command line tool."
        options[:switch] = false
        
        opts.on('-s', '--switch', 'Set options as switch') do |value|
            options[:switch] = true
        end

        opts.on('-n', '--name Name', 'Pass-in single name') do |value|
            options[:name] = value
        end

        opts.on('-a', '--array A,B', Array, 'List of arguments') do |value|
            options[:array] = value
        end
    end
    option_parser.parse!
    puts options.inspect   
    puts options[:array][0]
end