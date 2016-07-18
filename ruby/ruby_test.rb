#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "yaml"
require "find"

file = "E:\\sun_project\\python_scripts\\ruby\\xml"
tool = "iar"
istring1 = ["IAR", "GCC", "ARM"]

begin
    istring1.each do |each|
       each.downcase!
    end

    puts istring1.inspect
    # if tool == ("iar" or "gcc" or "arm")
    #     puts tool
    # end
    # Find.find(file) do |filename|
    #     if File.file?(filename) && File.extname(filename) == ".meta"
    #         puts filename
    #     end
    # end

end

