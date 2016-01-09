#!/usr/bin/python
#Filename:project_name_parser.py
#command line example:

import  xml.dom.minidom

if __name__ == "__main__":
    print 'I am in the test'
else:
    dom = xml.dom.minidom.parse(r'E:\tmp\rc1\SDK_2.0_FRDM-K66F_all\boards\frdmk66f\demo_apps\rtc_func\atl\.project')
    root = dom.documentElement
    tag_name = root.getElementsByTagName('name')
    tag0_name = tag_name[0]
    
    print tag0_name.firstChild.data
    print 20 * '*'

