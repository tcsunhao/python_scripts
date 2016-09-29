#!/usr/bin/ruby 
# coding : utf-8

require "yaml"
require "find"
require "optparse"
require "pathname"
require 'set'

module ModuleTop

    def self.who_am_i?()
        puts "#{self.class.name}"
    end

    # self is for this module self function
    def self.introduce_himself()    
        puts "I am from ModuleTop."
    end

    def say_hello()
        puts "hello brother, I am #{self.to_s}."
    end

end

module Music
    
    class Song    
        
        include ModuleTop

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

        def self.introduce_class
            puts "My name is Song."
        end
    end

end

if __FILE__ == $0
    # include ModuleTop
    # say_hello

    # 能这样直接调用的都必须是模块自身的方法（self）， 否则，就需要include
    ModuleTop::introduce_himself()

    song = Music::Song.new("Holt", "Strong","100")
    puts song.to_s
    song.say_hello

    # class can call not self function
    puts Music::Song.to_s

    # below is wrong, class self funtion cannot be called by object
    # song.introduce_class
    
    # below is not correct, the self funtion in module cannot be used as a self function in class which includes it 
    # Music::Song.who_am_i?
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
