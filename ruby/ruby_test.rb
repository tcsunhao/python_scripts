#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "yaml"
require "find"

file = "E:\\sun_project\\python_scripts\\ruby\\xml"
istring0 = "HoltSun"
istring1 = "Holt"

begin
    istring = istring1 - istring0
    puts istring
    # Find.find(file) do |filename|
    #     if File.file?(filename) && File.extname(filename) == ".meta"
    #         puts filename
    #     end
    # end

end

