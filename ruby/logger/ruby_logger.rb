#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require 'logger'

if __FILE__ == $0
    
    @logger = Logger.new(STDOUT)
    @logger.level = Logger::DEBUG

    @logger.info(" I am testing logger class by ruby. ")
end
