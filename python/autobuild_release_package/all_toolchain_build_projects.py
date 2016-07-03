#! /usr/bin/env python

# Copyright (c) 2013 Freescale Semiconductor, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# o Redistributions of source code must retain the above copyright notice, this list
#   of conditions and the following disclaimer.
#
# o Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
#
# o Neither the name of Freescale Semiconductor, Inc. nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Options
#
# -i, "--incremental", Incremental build (default).
# -a, "--arch", Specify the which type of projects to build.
# -b, "--board", Board list seperated by comma. e.g. -b twrk64f120m,frdmk64f120m
# -p, "--project_list", Takes a comma separated list of projects to build.
# -f, "--project_list_file", A file of projects list, take /project_list/<tool>_<platform>.txt for example.
# -t, "--target", build targets. parameters options: DEBUG, RELEASE, ALL

# Usage demo:
# 1. for single soc:
#    > python all_build_projects -d K60D10
# 2. parse project from a project list file:
#    > python all_build_projects -f "project_list/iar_twrk64f120m.txt"

import os, sys

class SdkProjectBuilder():
    ## Constructor.
    def __init__(self):
        pass

    def run(self):
        status = 0
        status += os.system('python autobuild_iar_release_package.py -n frdmk82f -m debug' )
        status += os.system('python autobuild_keil_release_package.py -n frdmk82f -m debug' )
        status += os.system('python autobuild_kds_release_package.py -n frdmk82f -m debug' )
        status += os.system('python autobuild_atl_release_package.py -n frdmk82f -m debug' )
        return status

if __name__ == "__main__":
    exit(SdkProjectBuilder().run())
