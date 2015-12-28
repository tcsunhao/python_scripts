#!/usr/bin/python
#Filename:project_name_parser.py
#command line example:

import  xml.dom.minidom

dom = xml.dom.minidom.parse('E:\\tmp\\rc1\\SDK_2.0_FRDM-K66F_all1\\boards\\frdmk66f\\usb_host_audio_speaker\\bm\\atl\\.project')

root = dom.documentElement

tag_name = root.getElementsByTagName('name')

tag0_name = tag_name[0]
print tag0_name.firstChild.data
# for mem in tag_name:
    # print mem.nodeValue

# print root.nodeName
# print root.nodeValue
# print root.nodeType
# print root.ELEMENT_NODE
print 20 * '*'