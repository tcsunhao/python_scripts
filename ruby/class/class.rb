#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "yaml"
require "find"
require "optparse"
require "pathname"
require 'set'

require './music'

class KaraokeSong < Music::Song

    attr_reader :lyrics

    def initialize(name, artist, duration, lyrics)
        super(name, artist, duration)
        @lyrics = lyrics
    end

    def to_s()
        puts "i am in"
        super + "   #{@lyrics}"
    end
end

class SongList
    MAX_TIME = 30

    def self.is_too_long(song)
        return song.duration > MAX_TIME
    end
end

# end

if __FILE__ == $0
    
    song = KaraokeSong.new("Holt", "Fleck", 260, "xxxxxxxxxxxxxx")
    SongList.is_too_long(song)
    puts song.to_s

end



# def test(itest)
#     i = itest
# end
# def test=(itest)
#     i = itest
# end

# attr_reader
# def abc
# return @abc
# end


# class A  
#   #类的类实例变量在访问前可以赋值也可以不赋值，不赋值就是nil  
#   @alpha='This is @alpha\' value!' 
  
#   def A.look
#    puts "#{@alpha}"  
#   end
#   def look  
#    puts "#{@alpha}"  
#   end
# end 
