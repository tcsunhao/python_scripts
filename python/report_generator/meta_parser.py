#!/usr/bin/python
#Filename : meta_parser.py
# command line example:
#   python meta_parser.py

import os, re, sys
import xml.dom.minidom
from feature_parser import FeatureParser

class MetaParser:
    """docstring for MetaParser"""

    DEVICE_DIR = './../../../devices'
    PLATFORM_DIRVERS_DIR = './../../../platform/drivers'
    MMCAU_DIR = './../../../middleware/mmcau'

    EXCETIONLIST_FOR_DRIVER_TYPE = \
    [
        "ADC",
        "AIPS",
        "ANT",
        "AXBS",
        "BLE_RF_REGS",
        "BP",
        "BTLE_RF",
        "CAU",
        "COREDEBUG",
        "DDR",
        "DRY",
        "DWT",
        "EMVSIM",
        "ETB",
        "ETF",
        "ETM",
        "FGPIO",
        "FMC",
        "FTFA",
        "FTFE",
        "FTFL",
        "FPB",
        "GENFSK",
        "INTERRUPT",
        "ITM",
        "I2S",
        "IRQ",
        "LCDC",
        "MCM",
        "MSCM",
        "MTB",
        "MTBDWT",
        "MTB_DWT",
        "MTB_ROM",
        "NV",
        "NFC",
        "OPAMP",
        "OSC",
        "OSC32",
        "OTFAD",
        "PCC",
        "PWT",
        "RFSYS",
        "RFVBAT",
        "ROM",
        "RSIM",
        "SCB",
        "SDRAM",
        "SYSTICK",
        "TMR",
        "TPIU",
        "TRIAMP",
        "TRNG0",
        "USB",
        "USBDCD",
        "USBHS",
        "USBHSDCD",
        "USBPHY",
        "XCVR",
        "XCVR_ANALOG",
        "XCVR_CTRL",
        "XCVR_PHY",
        "XCVR_PKT_RAM",
        "XCVR_PLL_DIG",
        "XCVR_RX_DIG",
        "XCVR_TSM",
        "XCVR_TX_DIG",
        "XCVR_ZBDEM",
        "ZLL",

        "MCG",
        "MCGLITE",
        "SCG",
        "OSC",
        "OSC32"
    ]

    def __init__(self):
        # Self use
        self.exception_driver_type_list = []
        self.platform_drivertype_list = []
        
        # For sdk_reportor.py
        self.part_num_list = []
        self.ipdriver_dic = {}
        self.alldriver_dic = {}
        self.boardtype_list = []

    def meta_get_device_part_num(self, device):

        '''
        This function is used to get all the partnumbers of given device from
        xxx_device.meta. The partnumbers are stored in self.part_num_list.


        device: SoC name which is used in <repo>/device/ folder.

        return: self.part_num_list
        '''

        # The device meta path
        device_mata_path = MetaParser.DEVICE_DIR + '/%s/%s_device.meta' % (device, device)
        device_meta_dom = xml.dom.minidom.parse(device_mata_path)
        root = device_meta_dom.documentElement
        tag_device = root.getElementsByTagName('devices')[0].getElementsByTagName('device')
        for each_tag_device in tag_device:
            tag_part = each_tag_device.getElementsByTagName('part')
            for each_tag_part in tag_part:
                self.part_num_list.append(each_tag_part.getAttribute('name'))

        return self.part_num_list

    def meta_compare_to_get_drivers_dic(self, device, part_num):
        '''
            Compares the device meta with the driver meta to get the ip driver information and all 
            drivers'information.

            The function returns 2 dictionaries and 1 list. They are stored in self.ipdriver_dic, 
            self.alldriver_dic and self.boardtype_list

            self.ipdriver_dic contains the ip drivers the device should support.
            It looks like :
                { 
                    'adc16': 'certain D_IP_ADC_16bSAR_SYN_047',
                    'cmp'  : 'certain D_IP_ANL_1C1D8C_SYN_030',
                    'crc'  : 'certain D_IP_CRC_16_32_PROG_SYN_011',
                    ......
                    'i2s'  : 'uncertain unsupport',
                    ......
                }

            self.alldriver_dic contains all the drivers the device should support
            It looks like :
                {
                    'adc16': '2.0.0',
                    'cmp'  : '2.0.0',
                    'crc'  : '2.0.1', 
                    ......
                    'uart' : '2.0.1'
                    'uart_dma': '2.0.1', 
                    'uart_freertos': '2.0.1', 
                    'uart_ucosii': '2.0.1',
                    'uart_ucosiii': '2.0.1'
                    ......
                }

            The board list of dedicated device:
            self.boardtype_list = [
                FRDM-K64F,
                TWR-K64F120M
            ]
        '''
        # component_name to find all driver
        component_name = {}
        # list to store ip_block version and ip_block information
        device_meta_ip_list = []
        # dictionary to store the ip driver information
        ipdriver_dic = {}
        # dictionary to store all driver information
        alldriver_dic = {}
        # board type list
        boardtype_list = []
        # Determines whether the device part number is included in the meta file
        this_device = 0
        # driver directors list 1 from the feature file
        driver_dir_list1 = []
        # driver directors list 2 from the possible new meta file.
        driver_dir_list2 = []
        # The final driver list
        driver_dir_list = []
        # For emvsim use
        find_emvsim = 0

        # Needs the driver directors list from the feature_parser.py
        featureParser =  FeatureParser()
        featureParser.get_featurelist(device, part_num)
        driver_dir_list1 = featureParser.transfer_features2drivers()[:]

        # The device meta path
        device_mata_path = MetaParser.DEVICE_DIR + '/%s/%s_device.meta' % (device, device)
        device_meta_dom = xml.dom.minidom.parse(device_mata_path)
        root = device_meta_dom.documentElement

        # Get the platform list
        for board in root.getElementsByTagName('board'):
            if board.hasAttribute('name'):
                self.boardtype_list.append(board.getAttribute('name'))

        tag_device = root.getElementsByTagName('device')
        for device in tag_device:
            if device.getElementsByTagName('part') != None:
                tag_part = device.getElementsByTagName('part')
                for part in tag_part:
                    # Check whether the part number matches
                    if part.getAttribute('name') == part_num:
                        this_device = 1
                        break
            if this_device == 1:
                tag_ip_block = device.getElementsByTagName('modules')[0].getElementsByTagName('ip_block')
                # Adds the ip_block version into the device_meta_ip_list
                for ip_block in tag_ip_block:
                    device_meta_ip_list.append(ip_block.getAttribute('version'))
                break

        # If the part number is not included in the device meta file
        if this_device == 0:
            print 'Please check your part num. It cann\'t be found in the device meta file.'
            sys.exit()

        # Get the ip driver list 2 from the new meta file.
        for each_item in device_meta_ip_list:
            if re.search(r"DriverType_",each_item):
                tmp_ipdriver_name = ('_').join(each_item.split('_')[1:])
                # "RNG" is for rnga
                if tmp_ipdriver_name == "RNG":
                    driver_dir_list2.append("rnga")
                # "EMVSIM" is for smartcard
                elif tmp_ipdriver_name == "EMVSIM":
                    driver_dir_list2.append("smartcard")
                # "FB" is for flexbus
                elif tmp_ipdriver_name == "FB":
                    driver_dir_list2.append("flexbus")
                # "QuadSPI" is for qspi
                elif tmp_ipdriver_name == "QuadSPI":
                    driver_dir_list2.append("qspi")
                elif self.list_has_item(MetaParser.EXCETIONLIST_FOR_DRIVER_TYPE, tmp_ipdriver_name) == 0:
                    driver_dir_list2.append(tmp_ipdriver_name.lower())


        # Adds "clock"
        driver_dir_list2.append("clock")
        driver_dir_list2.sort()

        # Compare the two driver list
        for each_item_in_driver_dir_list2 in driver_dir_list2:
            if self.list_has_item(driver_dir_list1, each_item_in_driver_dir_list2) == 1:
                self.ipdriver_dic[each_item_in_driver_dir_list2] = "certain "
            else:
                self.ipdriver_dic[each_item_in_driver_dir_list2] = "uncertain "

            driver_dir_list.append(each_item_in_driver_dir_list2)

        for each_item_in_driver_dir_list1 in driver_dir_list1:
            if self.list_has_item(driver_dir_list2, each_item_in_driver_dir_list1) == 0:
                self.ipdriver_dic[each_item_in_driver_dir_list1] = "uncertain "
                driver_dir_list.append(each_item_in_driver_dir_list1)


        # Parse all the drivers' meta file under the platform/driver
        for ipdriver_name in driver_dir_list:
            driver_dir_path = MetaParser.PLATFORM_DIRVERS_DIR + '/' + ipdriver_name
            if os.path.exists(driver_dir_path):
                for parent,dirnames,filenames in os.walk(driver_dir_path):
                    for filename in filenames:
                        filename_path = os.path.join(parent,filename)
                        if re.search(r'.meta', filename_path):
                            driver_meta_dom = xml.dom.minidom.parse(filename_path)
                            root = driver_meta_dom.documentElement
                            tag_component = root.getElementsByTagName('components')[0].getElementsByTagName('component')

                            # Fill in the 'name' group with differnet 'requires'
                            for component in tag_component:
                                if component.hasAttribute('description'):
                                    # The following 3 drivers are needed in all devices
                                    if component.getAttribute('description') == 'Clock Driver' or \
                                        component.getAttribute('description') == 'Flash Driver' or \
                                        component.getAttribute('description') == 'PORT Driver':

                                        ipdriver_dic[ipdriver_name] = 'None'
                                        component_name[component.getAttribute('name')] = []

                                    # The 'common' is not needed
                                    if component.getAttribute('description') == 'COMMON Driver':
                                        break
                                else:
                                    # smartcard is special
                                    if re.search('smartcard', component.getAttribute('name')):

                                        ip_version = str(component.getAttribute('requires').split('.')[-1])
                                        if self.list_has_item(device_meta_ip_list, ip_version) == 1:
                                            if component.getAttribute('name') == 'platform.drivers.smartcard_phy_emvsim.support':
                                                ipdriver_dic['smartcard'] = ip_version
                                                find_emvsim = 1
                                            component_name[('.').join(component.getAttribute('name').split('.')[0:-1])] = []

                                    elif component.getAttribute('name').split('.')[2].find(ipdriver_name) != -1:
                                        # Ignores the "platform.drivers.xxxxx.platform.support"
                                        if component.getAttribute('name').split('.')[3] == "platform":
                                            pass
                                        else:
                                            ip_version = str(component.getAttribute('requires').split('.')[-1])
                                            if self.list_has_item(device_meta_ip_list, ip_version) == 1:
                                                if ((ipdriver_name=="edma") and (ip_version.find("D_IP_DMA_CH_MUX")!=-1)):
                                                    pass
                                                else:
                                                    ipdriver_dic[ipdriver_name] = ip_version
                                                component_name[('.').join(component.getAttribute('name').split('.')[0:-1])] = []
            else:
                ipdriver_dic[ipdriver_name] = 'unsupport'

        if find_emvsim == 0:
            ipdriver_dic['smartcard'] = "no_emvsim"

        # Add mmcau support
        mmcau_meta_path = MetaParser.MMCAU_DIR + '/fsl_mmcau.meta'
        if os.path.exists(mmcau_meta_path):
            driver_meta_dom = xml.dom.minidom.parse(mmcau_meta_path)
            root = driver_meta_dom.documentElement
            tag_component = root.getElementsByTagName('components')[0].getElementsByTagName('component')[0]
            mmcau_ipversion = tag_component.getAttribute('requires').split('.')[-1]
            if self.list_has_item(device_meta_ip_list, mmcau_ipversion):
                ipdriver_dic['mmcau'] = mmcau_ipversion
        else:
            pass

        for each_key in self.ipdriver_dic.keys():
            if ipdriver_dic.has_key(each_key):
                self.ipdriver_dic[each_key] += ipdriver_dic[each_key]
            else:
                self.ipdriver_dic[each_key] += "unsupport"

        # for k,v in self.ipdriver_dic.items():
        #     print k, v

        # Parse the ip drivers' meta file under the platform/driver
        # This time is for get all the drivers.
        for key in ipdriver_dic.keys():
            meta_path = MetaParser.PLATFORM_DIRVERS_DIR + '/%s' % (key)
            if os.path.exists(meta_path):
                for parent,dirnames,filenames in os.walk(meta_path):
                    for filename in filenames:
                        filename_path = os.path.join(parent,filename)
                        if re.search(r'\.meta', filename_path):
                            # print filename_path
                            driver_meta_dom = xml.dom.minidom.parse(filename_path)
                            root = driver_meta_dom.documentElement
                            tag_component = root.getElementsByTagName('components')[0].getElementsByTagName('component')
                            for component in tag_component:
                                if component.hasAttribute('description'):
                                    driver_version = component.getAttribute('version')
                                    tag_files = component.getElementsByTagName('source')[0].getElementsByTagName('files')
                                    for files in tag_files:
                                        if re.search(r'\.h',files.getAttribute('mask')) :
                                            if files.hasAttribute('requires'):
                                                if component_name.has_key(files.getAttribute('requires')):
                                                    alldriver_dic[(('_').join((files.getAttribute('mask').split('.')[0].split('_')[1:])))] = driver_version
                                                elif self.list_has_item(device_meta_ip_list, files.getAttribute('requires').split('.')[-1]):
                                                    alldriver_dic[(('_').join((files.getAttribute('mask').split('.')[0].split('_')[1:])))] = driver_version
                                                elif re.search(r'middleware\.',files.getAttribute('requires')) :
                                                    alldriver_dic[(('_').join((files.getAttribute('mask').split('.')[0].split('_')[1:])))] = driver_version
                                            else:
                                                alldriver_dic[(('_').join((files.getAttribute('mask').split('.')[0].split('_')[1:])))] = driver_version
        self.alldriver_dic = alldriver_dic.copy()

    def get_platform_drivertype_list(self):
        '''
            This function is used to get the driver type list under platform/drivers/fsl_xxx.meta.
            The list is stored in self.platform_drivertype_list.
            The list is like:

        '''
        for parent,dirnames,filenames in os.walk(MetaParser.PLATFORM_DIRVERS_DIR):
            for filename in filenames:
                filename_path = os.path.join(parent,filename)
                if re.search(r'\.meta', filename_path):
                    driver_meta_dom = xml.dom.minidom.parse(filename_path)
                    root = driver_meta_dom.documentElement
                    tag_component = root.getElementsByTagName('components')[0].getElementsByTagName('component')
                    for component in tag_component:
                        if component.hasAttribute('requires'):
                            if component.getAttribute('requires').find("DriverType_") != -1:
                                if self.list_has_item(self.platform_drivertype_list,component.getAttribute('requires').split(' ')[0].split('.')[-1])==0:
                                    self.platform_drivertype_list.append(component.getAttribute('requires').split(' ')[0].split('.')[-1])
                                break
        # for mem in self.platform_drivertype_list:
        #     print mem

    def get_exception_driver_type_list(self):
        ''''
        Find drivers which are in self.platform_drivers_list but not in the
        version tags.
        In device meta, there would be the driver name list naming
        as DriverType_(DRIVER_NAME) in 'version' tag, such as DriverType_GPIO. We
        use the lower case of DRIVER_NAME as the drivers supported by this device.
        This method returns the drivers in the 'version' tag but not in
        self.platform_drivers_list.

        '''
        self.get_platform_drivertype_list()
        for parent,dirnames,filenames in os.walk(MetaParser.DEVICE_DIR):
            for filename in filenames:
                filename_path = os.path.join(parent,filename)
                if re.search(r'_device.meta',filename_path):
                    if os.path.exists(filename_path):
                        device_meta_dom = xml.dom.minidom.parse(filename_path)
                        dom_root = device_meta_dom.documentElement
                        tag_devices = dom_root.getElementsByTagName('devices')[0]
                        tag_device = dom_root.getElementsByTagName('device')
                        for each_device in tag_device:
                            tag_ip_block = each_device.getElementsByTagName('modules')[0].getElementsByTagName('ip_block')
                            for each_ip_block in tag_ip_block:
                                version_string = each_ip_block.getAttribute('version')
                                if re.search(r"DriverType_",version_string):
                                    if self.list_has_item(self.platform_drivertype_list, version_string) == 0:
                                        if self.list_has_item(self.exception_driver_type_list, version_string) == 0:
                                            self.exception_driver_type_list.append(version_string)
                        
                    else:
                        print filename_path + " not found\n"

        self.exception_driver_type_list.sort()
        for each_item in self.exception_driver_type_list:
            print each_item

    def list_has_item(self, list, item):
        '''This function is used to check whether the item is in the list

        If in, return 1, else return 0'''
        for mem in list:
            if mem == item:
                return 1
        return 0



if __name__ == '__main__':
    metaObject =  MetaParser()
    # metaObject.meta_compare_to_get_drivers_dic('MK64F12', 'MK64FN1M0VLL12')
    # metaObject.meta_get_device_part_num('MK64F12')
    # print '*'*78
    # metaObject1 =  MetaParser()
    # metaObject1.meta_get_device_part_num('MK11D5')
    # metaObject.get_exception_driver_type_list()
    # metaObject.meta_compare_to_get_drivers_dic('MKS22F12', 'MKS22FN128VLL12')
    # metaObject.meta_compare_to_get_drivers_dic('MKL28Z7', 'MKL28Z512VDC7')
    # metaObject.get_platform_drivertype_list()
    metaObject.get_platform_drivertype_list()
    # metaObject.meta_compare_to_get_drivers_dic('MK80F25615', 'MK80FN256VDC15')
    # metaObject.meta_compare_to_get_drivers_dic('MK80F25615', 'MK80FN256VDC15')
    # metaObject.meta_compare_to_get_drivers_dic('MKV58F22', 'MKV58F1M0VLQ22')
    # metaObject.meta_compare_to_get_drivers_dic('MKL27Z4', 'MKL27Z128VMP4')
    # metaObject.meta_get_device_part_num('MKW01Z4')
    # metaObject.meta_compare_to_get_drivers_dic('MKW01Z4','MKW01Z128CHN4')
