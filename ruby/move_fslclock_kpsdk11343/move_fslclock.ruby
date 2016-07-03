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
    end

    def move_clockandother_drivers()
        devices_path = @sdk_rootdir + @devices_relpath
        Dir.entries(devices_path).each do |each_device|
            next if ['.','..'].include?(each_device)
            # All files has a '.' in the file name
            next if each_device.include?('.')
            # Gets the full path of device/xxxxx
            devices_path = (@sdk_rootdir + @devices_relpath + each_device).gsub(/\\/,'/')
            
            if Dir.exists?(devices_path)
                devices_drivers_path = devices_path + '/drivers'
                next if Dir.exists?(devices_drivers_path)
                # Makes the "drivers" dir under /devices/xxxx
                FileUtils.mkdir_p(devices_drivers_path)
                @driver_files_names.each do |each_file|
                    drivers_file_path = devices_path + '/' + each_file
                    if File.exists?(drivers_file_path)
                        p drivers_file_path
                    end
                end
            else
                raise "Dir not exists : #{devices_path}"
            end
        end
    end

end


if __FILE__ == $0
    sdk_root_dir = "E:\\git_sdk_2.0_mainline\\mcu-sdk-2.0\\"
    obj = MoveDriversUnderDevice.new(sdk_root_dir)
    obj.move_clockandother_drivers()
end




