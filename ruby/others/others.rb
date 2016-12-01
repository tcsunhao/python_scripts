#!/usr/bin/ruby 
# -*- coding : utf-8 -*-

require "yaml"
require "find"
require "optparse"
require "pathname"
require 'set'

class GeneratorUp

    attr_reader :logger
    attr_reader :script_dir
    attr_reader :ustruct
    attr_reader :generated_hook

    def initialize(
        ustruct:    nil,
        script_dir: nil,
        logger:     nil,
        **kwarg
    )
        @logger         = logger ? logger : Logger.new(STDOUT)
        @script_dir     = script_dir
        @ustruct        = ustruct
    end
end

class Generator < GeneratorUp

    # attr_accessor :gen_release

    def initialize(*arg1,output_rootdir: nil, refer_paths: nil, generate_options: nil, project_names:nil, **kwargs)
        puts **kwargs
        super(**kwargs)
        @output_rootdir = output_rootdir
        @refer_paths = refer_paths
        @gen_options = generate_options
        @project_names = project_names
    end
end



if __FILE__ == $0
    # method_test("one", "two", "three",Country:"China")
    # log("hello", "INFO")
    generator = Generator.new(
                "p0",
                "p1",
                "p2",
                ustruct:            "p_translated_data",
                project_names:      "p_project_names",
                script_dir:         "p_script_dir",
                output_rootdir:     "p_output_rootdir",
                logger:             "p_logger",
                refer_paths:        "p_refer_paths",
                generate_options:   "p_generate_options"
            )



end


# def log(msg, level="ERROR", time:Time.now)
#     puts "#{ time.ctime } [#{ level }] #{msg}"
# end
# log("hello", "INFO")
def log(msg, level="ERROR", time:Time.now)
    puts "#{ time.ctime } [#{ level }] #{msg}"
end

def method_test(*arg1, **rest)
    puts arg1.class
    puts arg1
    puts rest.class  #should be an array
    puts rest
end
