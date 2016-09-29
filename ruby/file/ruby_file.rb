#!/usr/bin/ruby 
# -*- coding : utf-8 -*-
# 
require 'tempfile'

tmpfile = Tempfile.new('my_tmp')
tmpfile.puts "helloworldswdsfasdfasdfasdfasdfasdfasdfasdf"
tmpfile.close
tmpfile.open
tmpfile.each_line do |each|
    puts each
end
tmpfile.close


# f_write = File.open("tmp.txt", "w")
# File.open("tmp1.c", "r") do |file|
#     while var = file.gets
#         puts var
#         f_write.write(var)
#     end 
# end
# puts "end"
# f_write.close


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
# 
# 输出文件完整绝对路径
# puts Pathname.new(file_path).realpath

# 输出文件
# File.open("tmp1.c", "r") do |file|
#     arr = file.readlines()
#     # Notes the last line, should be a blank one
#     arr.each { |chr| puts chr  }
# end
# 

# 此种方法遍历文件会漏掉一个最后一个空行
# begin
#     File.open("tmp1.txt", "r") do |file|
#         file.each_line do |v|
#             puts v
#         end
#     end
#     puts "end"
# rescue
#     puts "There is an exception"
# end
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