#!/usr/bin/ruby 
# -*- coding : utf-8 -*-
# 

file_path = "test.txt"
content_string0 = "I am Holt Sun from NXP, I love ruby.(fuck it!)"
content_string1 = "Python is much easier than Ruby."
file_tmp_path = "tmp1.c"


begin
    File.open("tmp1.c", "r") do |file|
        puts file.class
        file.each do |v|
            puts v
        end
    end
rescue
    puts "There is an exception"
end


# 常用文件操作
# File.open("file.rb") if File::exists?( "file.rb" )
# File::directory?( "/usr/local/bin" )
# File.file?( "text.txt" )
# File.readable?( "test.txt" )  # => true
# File.writable?( "test.txt" )  # => true
# File.executable?( "test.txt" ) # => false
# File.extname(f)
# Dir.chdir("/usr/bin")
# 

# 输出文件
# File.open("tmp1.c", "r") do |file|
#     arr = file.readlines()
#     # Notes the last line, should be a blank one
#     arr.each { |chr| puts chr  }
# end
# 
# 
# 读写文件
# f_write = File.open("tmp.txt", "w")
# File.open("tmp1.c", "r") do |file|
#     arr = file.readlines()
#     arr.each do |var|
#         f_write.write(var)
#     end 
# end
# f_write.close
# 
# 
# puts
# putc
# 
# #### putc ?.
# File.open("tmp1.c", "r") do |file|
#     file.each_byte do |v|
#         putc v
#         putc ?.            
#     end
# end
# 
# 
# File.open("tmp1.c", "r") do |file|
#     file.each do |v|
#         puts v
#     end
# end
# 
# 
# 遍历文件夹
# Find.find(dir) do |filename|
#     p filename
# end