#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "yaml"
require "find"
require 'fileutils'

class MoveDriversUnderDevice
    
    def initialize(sdk_rootdir)
        # sdk_rootdir
        @sdk_rootdir = sdk_rootdir
        @devices_relpath = "devices/"
        # Files needs to be moved to the devices/xxxx
        @driver_files_names = ["fsl_clock.h",
                               "fsl_clock.c"]
        @driver_clock_dir_relpath = "platform/drivers/clock"
    end

    def move_clockandother_drivers()
        devices_path = @sdk_rootdir + @devices_relpath
        Dir.entries(devices_path).each do |each_device|
            next if ['.','..'].include?(each_device)
            # All files has a '.' in the file name
            next if each_device.include?('.')
            # Gets the full path of device/xxxxx
            devices_path = (@sdk_rootdir + @devices_relpath + each_device).gsub(/\\/,'/')
            devices_drivers_path = devices_path + '/drivers'
            FileUtils.mkdir_p(devices_drivers_path) unless Dir.exists?(devices_drivers_path)
            
            if Dir.exists?(devices_path)
                @driver_files_names.each do |each_file|
                    drivers_file_path = devices_path + '/' + each_file
                    if File.exists?(drivers_file_path)
                        FileUtils.mv(drivers_file_path, "#{devices_drivers_path}/#{each_file}")
                    end
                end
            else
                raise "Dir not exists : #{devices_path}"
            end

            # Moves all the files and dirs under drivers/clock into devices/xxxx/drivers
            driver_clock_dir_path = @sdk_rootdir + @driver_clock_dir_relpath
            Dir.entries(driver_clock_dir_path).each do |each_clock_related|
                next if ['.','..'].include?(each_clock_related)
                dest_path = devices_drivers_path + '/' + each_clock_related
                src_path =  @sdk_rootdir + @driver_clock_dir_relpath + '/' + each_clock_related
                FileUtils.cp_r(src_path,dest_path)
            end
        end
    end

end


if __FILE__ == $0
    sdk_root_dir = "E:/git_sdk_2.0_mainline/mcu-sdk-2.0/"
    obj = MoveDriversUnderDevice.new(sdk_root_dir)
    obj.move_clockandother_drivers()
end




