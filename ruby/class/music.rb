#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "yaml"
require "find"
require "optparse"
require "pathname"
require 'set'


module Music
    
    class Song    
        attr_reader :name 
        attr_writer :name 

        attr_reader :artist 
        attr_reader :duration 

        def initialize(name, artist, duration)
            @name = name
            @artist = artist
            @duration = duration
        end

        # private
        def to_s()
            "Song: #{@name} -- #{@artist} (#{@duration})"
        end
    end

end
