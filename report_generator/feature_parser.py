#!/usr/bin/python
#Filename : feature_parser.py

import os, sys, re, argparse, yaml

class FeatureParser:
    """docstring for FeatureParser"""

    DEVICE_DIR = './../../../devices'
    MAP_YML_FILE_PATH = './map_features2drivers.yml'

    def __init__(self):
        self.feature_dic = {}
        self.driver_dir_list = []

    def get_featurelist(self, device, part_num=None):
        soc_feature_dic = {}
        
        # Clean variables
        start_parse_soc = 0
        start_parse_sim = 0
        start_parse_wdog = 0
        start_parse_rtc = 0
        start_parse_uart_smartcard = 0

        with_part_num = 0
        parse_under_part_num = 0

        # device check
        find_part_num = 0
        # All device has part num, but not all feature file has part num
        featurefile_has_part_num = 0

        feature_file_path = FeatureParser.DEVICE_DIR + '/%s/%s_features.h' % (device, device)

        with open(feature_file_path, 'r') as f_feature:
            if part_num != None:
                for line in f_feature.readlines():
                    if re.search(r'#if defined', line) != None:
                        featurefile_has_part_num = 1;

                    if re.search(part_num, line) != None:
                        featurefile_has_part_num = 1;
                        find_part_num = 1
                        break

                if find_part_num==0 and featurefile_has_part_num==1:
                    print 'Cannot find part_num : %s' % part_num + ', please check the spell or the soc feature files\n'
                    sys.exit()
            else:
                for line in f_feature.readlines():
                    if re.search(r'#if defined', line) != None:
                        featurefile_has_part_num = 1
                        break        
                if featurefile_has_part_num == 1:
                    print 'Not find the part_num in your command, please check'
                    sys.exit()
            
        # Parse the feature file
        f_feature = open(feature_file_path, 'r')

        if featurefile_has_part_num == 1:
            for line in f_feature.readlines():
                if start_parse_soc == 0:
                    if re.search(r'SOC module features', line) != None:
                        start_parse_soc = 1
                else:
                    if re.search(r'module features',line)!=None:
                        start_parse_soc = 0
                    if re.search(r'#if', line) != None:
                        with_part_num = 1
                    if with_part_num == 1:
                        if re.search(part_num, line) != None:
                            parse_under_part_num = 1
                        if parse_under_part_num == 1:                       
                            if (re.search(r'#elif',line)!=None or re.search(r'#endif',line)!= None) and re.search(part_num, line)==None :
                                parse_under_part_num = 0 
                                with_part_num = 0
                                start_parse_soc = 0
                            if re.search(r'(#define)\s*(FSL_FEATURE_SOC_\w*)\s*(\(\d*\))',line) != None:
                                searchobj = re.search(r'(#define)\s*(FSL_FEATURE_SOC_\w*)\s*(\(\d*\))',line)
                                if searchobj.group(3) == '(0)':
                                    pass
                                else:
                                    soc_feature_dic[searchobj.group(2)] = 'true'  
                    else:
                        if re.search(r'(#define)\s*(FSL_FEATURE_SOC_\w*)\s*(\(\d*\))',line) != None:
                            searchobj = re.search(r'(#define)\s*(FSL_FEATURE_SOC_\w*)\s*(\(\d*\))',line)
                            if searchobj.group(3) == '(0)':
                                pass
                            else:
                                soc_feature_dic[searchobj.group(2)] = 'true'
                # Parse the sim module features to find the FSL_FEATURE_SIM_HAS_COP_WATCHDOG
                if start_parse_sim == 0:
                    if re.search(r'SIM module features', line) != None:
                        start_parse_sim = 1
                else:
                    if re.search(r'module features',line)!=None:
                        start_parse_sim = 0
                    if re.search(r'#if', line) != None:
                        with_part_num = 1
                    if with_part_num == 1:
                        if re.search(part_num, line) != None:
                            parse_under_part_num = 1
                        if parse_under_part_num == 1:                       
                            if (re.search(r'#elif',line)!=None or re.search(r'#endif',line)!= None) and re.search(part_num, line)==None :
                                parse_under_part_num = 0 
                                with_part_num = 0
                                start_parse_sim = 0
                            if re.search(r'(#define)\s*(FSL_FEATURE_SIM_HAS_COP_WATCHDOG)\s*(\(\d*\))',line) != None:
                                searchobj = re.search(r'(#define)\s*(FSL_FEATURE_SIM_HAS_COP_WATCHDOG)\s*(\(\d*\))',line)
                                if searchobj.group(3) == '(0)':
                                    pass
                                else:
                                    soc_feature_dic[searchobj.group(2)] = 'true' 
                    else:
                        if re.search(r'(#define)\s*(FSL_FEATURE_SIM_HAS_COP_WATCHDOG)\s*(\(\d*\))',line) != None:
                            searchobj = re.search(r'(#define)\s*(FSL_FEATURE_SIM_HAS_COP_WATCHDOG)\s*(\(\d*\))',line)
                            if searchobj.group(3) == '(0)':
                                pass
                            else:
                                soc_feature_dic[searchobj.group(2)] = 'true'
                
                # Parse the wdog module features to find the FSL_FEATURE_WDOG_HAS_32BIT_ACCESS
                if start_parse_wdog == 0:
                    if re.search(r'WDOG module features', line) != None:
                        start_parse_wdog = 1
                else:
                    if re.search(r'module features',line)!=None:
                        start_parse_wdog = 0
                    if re.search(r'#if', line) != None:
                        with_part_num = 1
                    if with_part_num == 1:
                        if re.search(part_num, line) != None:
                            parse_under_part_num = 1
                        if parse_under_part_num == 1:                       
                            if (re.search(r'#elif',line)!=None or re.search(r'#endif',line)!= None) and re.search(part_num, line)==None :
                                parse_under_part_num = 0 
                                with_part_num = 0
                                start_parse_wdog = 0
                            if re.search(r'(#define)\s*(FSL_FEATURE_WDOG_HAS_32BIT_ACCESS)\s*(\(\d*\))',line) != None:
                                searchobj = re.search(r'(#define)\s*(FSL_FEATURE_WDOG_HAS_32BIT_ACCESS)\s*(\(\d*\))',line)
                                if searchobj.group(3) == '(0)':
                                    soc_feature_dic[searchobj.group(2)] = 'false'
                                else:
                                    soc_feature_dic[searchobj.group(2)] = 'true' 
                    else:
                        if re.search(r'(#define)\s*(FSL_FEATURE_WDOG_HAS_32BIT_ACCESS)\s*(\(\d*\))',line) != None:
                            searchobj = re.search(r'(#define)\s*(FSL_FEATURE_WDOG_HAS_32BIT_ACCESS)\s*(\(\d*\))',line)
                            if searchobj.group(3) == '(0)':
                                soc_feature_dic[searchobj.group(2)] = 'false'
                            else:
                                soc_feature_dic[searchobj.group(2)] = 'true'
                
                # Parse the rtc module features to find the FSL_FEATURE_RTC_IS_IRTC
                if start_parse_rtc == 0:
                    if re.search(r'RTC module features', line) != None:
                        start_parse_rtc = 1
                else:
                    if re.search(r'module features',line)!=None:
                        start_parse_rtc = 0
                    if re.search(r'#if', line) != None:
                        with_part_num = 1
                    if with_part_num == 1:
                        if re.search(part_num, line) != None:
                            parse_under_part_num = 1
                        if parse_under_part_num == 1:                       
                            if (re.search(r'#elif',line)!=None or re.search(r'#endif',line)!= None) and re.search(part_num, line)==None :
                                parse_under_part_num = 0 
                                with_part_num = 0
                                start_parse_rtc = 0
                            if re.search(r'(#define)\s*(FSL_FEATURE_RTC_IS_IRTC)\s*(\(\d*\))',line) != None:
                                searchobj = re.search(r'(#define)\s*(FSL_FEATURE_RTC_IS_IRTC)\s*(\(\d*\))',line)
                                if searchobj.group(3) == '(0)':
                                    pass
                                else:
                                    soc_feature_dic[searchobj.group(2)] = 'true' 
                    else:
                        if re.search(r'(#define)\s*(FSL_FEATURE_RTC_IS_IRTC)\s*(\(\d*\))',line) != None:
                            searchobj = re.search(r'(#define)\s*(FSL_FEATURE_RTC_IS_IRTC)\s*(\(\d*\))',line)
                            if searchobj.group(3) == '(0)':
                                pass
                            else:
                                soc_feature_dic[searchobj.group(2)] = 'true'  
                
                # Parse the uart_smartcard module features to find the FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT
                if start_parse_uart_smartcard == 0:
                    if re.search(r'UART module features', line) != None:
                        start_parse_uart_smartcard = 1
                else:
                    if re.search(r'module features',line)!=None:
                        start_parse_uart_smartcard = 0
                    if re.search(r'#if', line) != None:
                        with_part_num = 1
                    if with_part_num == 1:
                        if re.search(part_num, line) != None:
                            parse_under_part_num = 1
                        if parse_under_part_num == 1:                       
                            if (re.search(r'#elif',line)!=None or re.search(r'#endif',line)!= None) and re.search(part_num, line)==None :
                                parse_under_part_num = 0 
                                with_part_num = 0
                                start_parse_uart_smartcard = 0
                            if re.search(r'(#define)\s*(FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT)\s*(\(\d*\))',line) != None:
                                searchobj = re.search(r'(#define)\s*(FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT)\s*(\(\d*\))',line)
                                if searchobj.group(3) == '(0)':
                                    pass
                                else:
                                    soc_feature_dic[searchobj.group(2)] = 'true' 
                    else:
                        if re.search(r'(#define)\s*(FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT)\s*(\(\d*\))',line) != None:
                            searchobj = re.search(r'(#define)\s*(FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT)\s*(\(\d*\))',line)
                            if searchobj.group(3) == '(0)':
                                pass
                            else:
                                soc_feature_dic[searchobj.group(2)] = 'true'            
        else:
            for line in f_feature.readlines():
                # Parse the soc module features
                if start_parse_soc == 0:
                    if re.search(r'SOC module features', line) != None:
                        start_parse_soc = 1
                else:
                    if re.search(r'module features',line)!=None:
                        start_parse_soc = 0
                    if re.search(r'(#define)\s*(FSL_FEATURE_SOC_\w*)\s*(\(\d*\))',line) != None:
                        searchobj = re.search(r'(#define)\s*(FSL_FEATURE_SOC_\w*)\s*(\(\d*\))',line)
                        if searchobj.group(3) == '(0)':
                            pass
                        else:
                            soc_feature_dic[searchobj.group(2)] = 'true'        

                # Parse the sim module features to find the FSL_FEATURE_SIM_HAS_COP_WATCHDOG
                if start_parse_sim == 0:
                    if re.search(r'SIM module features', line) != None:
                        start_parse_sim = 1
                else:
                    if re.search(r'module features',line)!=None:
                        start_parse_sim = 0
                    if re.search(r'(#define)\s*(FSL_FEATURE_SIM_HAS_COP_WATCHDOG)\s*(\(\d*\))',line) != None:
                        searchobj = re.search(r'(#define)\s*(FSL_FEATURE_SIM_HAS_COP_WATCHDOG)\s*(\(\d*\))',line)
                        if searchobj.group(3) == '(0)':
                            pass
                        else:
                            soc_feature_dic[searchobj.group(2)] = 'true'

                # Parse the wdog module features to find the FSL_FEATURE_WDOG_HAS_32BIT_ACCESS
                if start_parse_wdog == 0:
                    if re.search(r'WDOG module features', line) != None:
                        start_parse_wdog = 1
                else:
                    if re.search(r'module features',line)!=None:
                        start_parse_wdog = 0
                    if re.search(r'(#define)\s*(FSL_FEATURE_WDOG_HAS_32BIT_ACCESS)\s*(\(\d*\))',line) != None:
                        searchobj = re.search(r'(#define)\s*(FSL_FEATURE_WDOG_HAS_32BIT_ACCESS)\s*(\(\d*\))',line)
                        if searchobj.group(3) == '(0)':
                            soc_feature_dic[searchobj.group(2)] = 'false'
                        else:
                            soc_feature_dic[searchobj.group(2)] = 'true'                        

                # Parse the rtc module features to find the FSL_FEATURE_RTC_IS_IRTC
                if start_parse_rtc == 0:
                    if re.search(r'RTC module features', line) != None:
                        start_parse_rtc = 1
                else:
                    if re.search(r'module features',line)!=None:
                        start_parse_rtc = 0
                    if re.search(r'(#define)\s*(FSL_FEATURE_RTC_IS_IRTC)\s*(\(\d*\))',line) != None:
                        searchobj = re.search(r'(#define)\s*(FSL_FEATURE_RTC_IS_IRTC)\s*(\(\d*\))',line)
                        if searchobj.group(3) == '(0)':
                            pass
                        else:
                            soc_feature_dic[searchobj.group(2)] = 'true'
                               
                # Parse the uart_smartcard module features to find the FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT
                if start_parse_uart_smartcard == 0:
                    if re.search(r'UART module features', line) != None:
                        start_parse_uart_smartcard = 1
                else:
                    if re.search(r'module features',line)!=None:
                        start_parse_uart_smartcard = 0
                    if re.search(r'(#define)\s*(FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT)\s*(\(\d*\))',line) != None:
                        searchobj = re.search(r'(#define)\s*(FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT)\s*(\(\d*\))',line)
                        if searchobj.group(3) == '(0)':
                            pass
                        else:
                            soc_feature_dic[searchobj.group(2)] = 'true'    
        f_feature.close()

        self.feature_dic = soc_feature_dic.copy()
 

    def transfer_features2drivers(self):
        
        driver_list = []
        
        # Loads the map_feature2driver.yml for getting the driver list
        f = file(FeatureParser.MAP_YML_FILE_PATH)
        yf = yaml.load(f)
        f.close()

        for item in yf.items():
            if item[0] == 'flash':
                driver_list.append('flash')
            elif item[0] == 'wdog':
                if self.feature_dic.has_key('FSL_FEATURE_SOC_WDOG_COUNT'):
                    if self.feature_dic.has_key('FSL_FEATURE_WDOG_HAS_32BIT_ACCESS'):
                        if self.feature_dic['FSL_FEATURE_WDOG_HAS_32BIT_ACCESS'] == 'true':
                            driver_list.append('wdog32')
                    else:
                        driver_list.append('wdog')
                else:
                    pass
            elif item[0] == 'wdog32':
                pass
            elif item[0] == 'rtc':
                if self.feature_dic.has_key('FSL_FEATURE_SOC_RTC_COUNT'):
                    if self.feature_dic.has_key('FSL_FEATURE_RTC_IS_IRTC'):
                        if self.feature_dic['FSL_FEATURE_RTC_IS_IRTC'] == 'true':
                            driver_list.append('irtc')
                    else:
                        driver_list.append('rtc')
                else:
                    pass
            elif item[0] == 'irtc':
                pass    
            else:
                key = item[1].keys()[0]
                if key == 'and':
                    has_driver = 1
                    for keymem in item[1].values()[0].keys():
                        if self.feature_dic.has_key(keymem) == False:
                            has_driver = 0
                            break
                    if has_driver == 1:
                        driver_list.append(item[0])
                elif key == 'or':
                    has_driver = 0
                    for keymem in item[1].values()[0].keys():
                        if self.feature_dic.has_key(keymem) == True:
                            has_driver = 1
                            break
                    if has_driver == 1:
                        driver_list.append(item[0])

        self.driver_list = driver_list[:] 
        self.driver_list.sort()

        # for mem in self.driver_list:
        #     print mem     
        return self.driver_list

if __name__ == '__main__':
    featureParser =  FeatureParser()
    featureParser.get_featurelist('MK64F12', 'MK64FN1M0VLL12')
    # featureParser.get_featurelist('MKS22F12', 'MKS22FN128VLL12') 
    # featureParser.get_featurelist('MKS22F12') 
    # featureParser.get_featurelist('PKE18F15') 
    # featureParser.get_featurelist('MKM34Z7', 'MKM34Z256VLQ7') 
    # featureParser.get_featurelist('MK80F25615', 'MK80FN256VDC15')
    # featureParser.get_featurelist('MK52D10', 'MK52DN512CLQ10')
    featureParser.transfer_features2drivers()        