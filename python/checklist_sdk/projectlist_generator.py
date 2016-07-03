#!/usr/bin/python
#Filename : projectlist_generator.py
#command line example:
#   python projectlist_generator.py -d MK64F12 -c MK64FN1M0VDC12 -e all
#   python projectlist_generator.py -d MKS22F12 -e all
#   python projectlist_generator.py -d MK80F25615 -e all
#   python projectlist_generator.py -d MK50D10 -c MK50DN512CLL10 -e all
#   python projectlist_generator.py -d MK50D10 -c MK50DX256CLK10 -e all
#   python projectlist_generator.py -d MKE16F16 -e all
#   python projectlist_generator.py -d MKM34Z7 -e all

import os, sys, re, argparse, yaml

def __read_options():
    # Build arg parser.
    parser = argparse.ArgumentParser(
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description='Build projects')

    # Options
    parser.add_argument('-d', '--device', help='The device name, such as MK64F12')
    parser.add_argument('-c', '--chipmodule', default=None, help='The chipmodule, such as MK64FN1M0VDC12')
    parser.add_argument('-e', '--exampletype', help='This argument represents exmaple type, available options: all, demo_apps, driver_examples, rtos_examples, usb_examples', default='all')

    return parser.parse_args()

soc_feature_dic = {}
driver_dic = {}

if __name__ == '__main__':
    # Clean variables
    start_parse_soc = 0
    start_parse_sim = 0
    start_parse_wdog = 0
    start_parse_rtc = 0
    start_parse_tsi = 0
    start_parse_uart_smartcard = 0

    with_chipmodule = 0
    parse_under_chipmodule = 0

    has_driver = 0
    # Gets the arg
    the_args = __read_options()
    
    # Gets the fear
    projectlist_generator_path = os.getcwd().replace('\\', '/')
    feature_file_path  = '/'.join(projectlist_generator_path.split('/')[0:-3]) + '/devices/' + the_args.device + '/' + the_args.device + '_%s'%'features.h'
    
    f_feature = open(feature_file_path, 'r')

    if the_args.chipmodule != None:
        find_chipmodule = 0
        for line in f_feature.readlines():
            if start_parse_soc == 0:
                if re.search(the_args.chipmodule, line) != None:
                    start_parse_soc = 1
                    find_chipmodule = 1
            else:
                if re.search(r'#elif',line)!=None or re.search(r'#endif',line)!=None :
                    start_parse_soc = 0
                if re.search(r'(#define)\s*(FSL_FEATURE_SOC_.*)\s*(\(\d\))',line) != None:
                    searchobj = re.search(r'(#define)\s*(FSL_FEATURE_SOC_.*)\s*(\(\d\))',line)
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
                    with_chipmodule = 1
                if with_chipmodule == 1:
                    if re.search(the_args.chipmodule, line) != None:
                        parse_under_chipmodule = 1
                    if parse_under_chipmodule == 1:                       
                        if (re.search(r'#elif',line)!=None or re.search(r'#endif',line)!= None) and re.search(the_args.chipmodule, line)==None :
                            parse_under_chipmodule = 0 
                            with_chipmodule = 0
                            start_parse_sim = 0
                        if re.search(r'(#define)\s*(FSL_FEATURE_SIM_HAS_COP_WATCHDOG)\s*(\(\d\))',line) != None:
                            searchobj = re.search(r'(#define)\s*(FSL_FEATURE_SIM_HAS_COP_WATCHDOG)\s*(\(\d\))',line)
                            if searchobj.group(3) == '(0)':
                                pass
                            else:
                                soc_feature_dic[searchobj.group(2)] = 'true' 
                else:
                    if re.search(r'(#define)\s*(FSL_FEATURE_SIM_HAS_COP_WATCHDOG)\s*(\(\d\))',line) != None:
                        searchobj = re.search(r'(#define)\s*(FSL_FEATURE_SIM_HAS_COP_WATCHDOG)\s*(\(\d\))',line)
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
                    with_chipmodule = 1
                if with_chipmodule == 1:
                    if re.search(the_args.chipmodule, line) != None:
                        parse_under_chipmodule = 1
                    if parse_under_chipmodule == 1:                       
                        if (re.search(r'#elif',line)!=None or re.search(r'#endif',line)!= None) and re.search(the_args.chipmodule, line)==None :
                            parse_under_chipmodule = 0 
                            with_chipmodule = 0
                            start_parse_wdog = 0
                        if re.search(r'(#define)\s*(FSL_FEATURE_WDOG_HAS_32BIT_ACCESS)\s*(\(\d\))',line) != None:
                            searchobj = re.search(r'(#define)\s*(FSL_FEATURE_WDOG_HAS_32BIT_ACCESS)\s*(\(\d\))',line)
                            if searchobj.group(3) == '(0)':
                                soc_feature_dic[searchobj.group(2)] = 'false'
                            else:
                                soc_feature_dic[searchobj.group(2)] = 'true' 
                else:
                    if re.search(r'(#define)\s*(FSL_FEATURE_WDOG_HAS_32BIT_ACCESS)\s*(\(\d\))',line) != None:
                        searchobj = re.search(r'(#define)\s*(FSL_FEATURE_WDOG_HAS_32BIT_ACCESS)\s*(\(\d\))',line)
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
                    with_chipmodule = 1
                if with_chipmodule == 1:
                    if re.search(the_args.chipmodule, line) != None:
                        parse_under_chipmodule = 1
                    if parse_under_chipmodule == 1:                       
                        if (re.search(r'#elif',line)!=None or re.search(r'#endif',line)!= None) and re.search(the_args.chipmodule, line)==None :
                            parse_under_chipmodule = 0 
                            with_chipmodule = 0
                            start_parse_rtc = 0
                        if re.search(r'(#define)\s*(FSL_FEATURE_RTC_IS_IRTC)\s*(\(\d\))',line) != None:
                            searchobj = re.search(r'(#define)\s*(FSL_FEATURE_RTC_IS_IRTC)\s*(\(\d\))',line)
                            if searchobj.group(3) == '(0)':
                                pass
                            else:
                                soc_feature_dic[searchobj.group(2)] = 'true' 
                else:
                    if re.search(r'(#define)\s*(FSL_FEATURE_RTC_IS_IRTC)\s*(\(\d\))',line) != None:
                        searchobj = re.search(r'(#define)\s*(FSL_FEATURE_RTC_IS_IRTC)\s*(\(\d\))',line)
                        if searchobj.group(3) == '(0)':
                            pass
                        else:
                            soc_feature_dic[searchobj.group(2)] = 'true'  
            
            # Parse the tsi module features to find the FSL_FEATURE_TSI_VERSION
            if start_parse_tsi == 0:
                if re.search(r'TSI module features', line) != None:
                    start_parse_tsi = 1
            else:
                if re.search(r'module features',line)!=None:
                    start_parse_tsi = 0
                if re.search(r'#if', line) != None:
                    with_chipmodule = 1
                if with_chipmodule == 1:
                    if re.search(the_args.chipmodule, line) != None:
                        parse_under_chipmodule = 1
                    if parse_under_chipmodule == 1:                       
                        if (re.search(r'#elif',line)!=None or re.search(r'#endif',line)!= None) and re.search(the_args.chipmodule, line)==None :
                            parse_under_chipmodule = 0 
                            with_chipmodule = 0
                            start_parse_tsi = 0
                        if re.search(r'(#define)\s*(FSL_FEATURE_TSI_VERSION)\s*(\(\d\))',line) != None:
                            searchobj = re.search(r'(#define)\s*(FSL_FEATURE_TSI_VERSION)\s*(\(\d\))',line)
                            soc_feature_dic[searchobj.group(2)] = searchobj.group(3).split('(')[1].split(')')[0]
                else:
                    if re.search(r'(#define)\s*(FSL_FEATURE_TSI_VERSION)\s*(\(\d\))',line) != None:
                        searchobj = re.search(r'(#define)\s*(FSL_FEATURE_TSI_VERSION)\s*(\(\d\))',line)
                        soc_feature_dic[searchobj.group(2)] = searchobj.group(3).split('(')[1].split(')')[0]                                                      
            
            # Parse the uart_smartcard module features to find the FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT
            if start_parse_uart_smartcard == 0:
                if re.search(r'UART module features', line) != None:
                    start_parse_uart_smartcard = 1
            else:
                if re.search(r'module features',line)!=None:
                    start_parse_uart_smartcard = 0
                if re.search(r'#if', line) != None:
                    with_chipmodule = 1
                if with_chipmodule == 1:
                    if re.search(the_args.chipmodule, line) != None:
                        parse_under_chipmodule = 1
                    if parse_under_chipmodule == 1:                       
                        if (re.search(r'#elif',line)!=None or re.search(r'#endif',line)!= None) and re.search(the_args.chipmodule, line)==None :
                            parse_under_chipmodule = 0 
                            with_chipmodule = 0
                            start_parse_uart_smartcard = 0
                        if re.search(r'(#define)\s*(FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT)\s*(\(\d\))',line) != None:
                            searchobj = re.search(r'(#define)\s*(FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT)\s*(\(\d\))',line)
                            if searchobj.group(3) == '(0)':
                                pass
                            else:
                                soc_feature_dic[searchobj.group(2)] = 'true' 
                else:
                    if re.search(r'(#define)\s*(FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT)\s*(\(\d\))',line) != None:
                        searchobj = re.search(r'(#define)\s*(FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT)\s*(\(\d\))',line)
                        if searchobj.group(3) == '(0)':
                            pass
                        else:
                            soc_feature_dic[searchobj.group(2)] = 'true'            
        if find_chipmodule == 0:
            print 'Cannot find chipmodule : %s' % the_args.chipmodule + ', please check the spell or the soc feature files\n'
            sys.exit()
    else:
        for line in f_feature.readlines():
            # Parse the soc module features
            if start_parse_soc == 0:
                if re.search(r'SOC module features', line) != None:
                    start_parse_soc = 1
            else:
                if re.search(r'module features',line)!=None:
                    start_parse_soc = 0
                if re.search(r'(#define)\s*(FSL_FEATURE_SOC_.*)\s*(\(\d\))',line) != None:
                    searchobj = re.search(r'(#define)\s*(FSL_FEATURE_SOC_.*)\s*(\(\d\))',line)
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
                if re.search(r'(#define)\s*(FSL_FEATURE_SIM_HAS_COP_WATCHDOG)\s*(\(\d\))',line) != None:
                    searchobj = re.search(r'(#define)\s*(FSL_FEATURE_SIM_HAS_COP_WATCHDOG)\s*(\(\d\))',line)
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
                if re.search(r'(#define)\s*(FSL_FEATURE_WDOG_HAS_32BIT_ACCESS)\s*(\(\d\))',line) != None:
                    searchobj = re.search(r'(#define)\s*(FSL_FEATURE_WDOG_HAS_32BIT_ACCESS)\s*(\(\d\))',line)
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
                if re.search(r'(#define)\s*(FSL_FEATURE_RTC_IS_IRTC)\s*(\(\d\))',line) != None:
                    searchobj = re.search(r'(#define)\s*(FSL_FEATURE_RTC_IS_IRTC)\s*(\(\d\))',line)
                    if searchobj.group(3) == '(0)':
                        pass
                    else:
                        soc_feature_dic[searchobj.group(2)] = 'true'
            
            # Parse the tsi module features to find the FSL_FEATURE_TSI_VERSION
            if start_parse_tsi == 0:
                if re.search(r'TSI module features', line) != None:
                    start_parse_tsi = 1
            else:
                if re.search(r'module features',line)!=None:
                    start_parse_tsi = 0
                if re.search(r'(#define)\s*(FSL_FEATURE_TSI_VERSION)\s*(\(\d\))',line) != None:
                    searchobj = re.search(r'(#define)\s*(FSL_FEATURE_TSI_VERSION)\s*(\(\d\))',line)
                    soc_feature_dic[searchobj.group(2)] = searchobj.group(3).split('(')[1].split(')')[0]
           
            # Parse the uart_smartcard module features to find the FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT
            if start_parse_uart_smartcard == 0:
                if re.search(r'UART module features', line) != None:
                    start_parse_uart_smartcard = 1
            else:
                if re.search(r'module features',line)!=None:
                    start_parse_uart_smartcard = 0
                if re.search(r'(#define)\s*(FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT)\s*(\(\d\))',line) != None:
                    searchobj = re.search(r'(#define)\s*(FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT)\s*(\(\d\))',line)
                    if searchobj.group(3) == '(0)':
                        pass
                    else:
                        soc_feature_dic[searchobj.group(2)] = 'true'    
    f_feature.close()
    
    for mem in soc_feature_dic.items():
        print mem

    f = file('./maps/map_feature2driver.yml')
    yf = yaml.load(f)
    f.close()

    for item in yf.items():
        if item[0] == 'flash':
            pass
        else:
            key = item[1].keys()[0]
            if key == 'and':
                has_driver = 1
                for keymem in item[1].values()[0].keys():
                    print keymem
                    if soc_feature_dic.has_key(keymem) == False:
                        has_driver = 0
                        break
                if has_driver == 1:
                    print '%%%%%%%%%%%%%%%%%%%%'
                    driver_dic[item[0]] = True
                    # if item[1].values()[0][keymem] != True:
                    #     print keymem
                    #     print item[1].values()[0][keymem]    

    print driver_dic


