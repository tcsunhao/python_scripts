#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "yaml"
require "find"
require "optparse"
require "pathname"
require 'set'

def log(msg, level="ERROR", time:Time.now)
    puts "#{ time.ctime } [#{ level }] #{msg}"
end

def method_test(*arg1, **rest)
    puts arg1.class
    puts arg1
    puts rest.class  #should be an array
    puts rest
end

if __FILE__ == $0
    method_test("one", "two", "three",Country:"China")
    log("hello", "INFO")
end


# def log(msg, level="ERROR", time:Time.now)
#     puts "#{ time.ctime } [#{ level }] #{msg}"
# end
# log("hello", "INFO")
