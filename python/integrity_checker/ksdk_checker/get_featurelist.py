#!/usr/bin/python
#Filename : get_featurelist.py

import os, sys, re, argparse, yaml


def __get_featurelist(feature_file_path, the_args):

    soc_feature_dic = {}
    
    # Clean variables
    start_parse_soc = 0
    start_parse_sim = 0
    start_parse_wdog = 0
    start_parse_rtc = 0
    start_parse_tsi = 0
    start_parse_uart_smartcard = 0

    with_chipmodule = 0
    parse_under_chipmodule = 0

    # Chipmodule check
    find_chipmodule = 0
    f_feature = open(feature_file_path, 'r')

    if the_args.chipmodule != None:
        for line in f_feature.readlines():
            if re.search(the_args.chipmodule, line) != None:
                find_chipmodule = 1
                break

        if find_chipmodule == 0:
            print 'Cannot find chipmodule : %s' % the_args.chipmodule + ', please check the spell or the soc feature files\n'
            sys.exit()

    else:
        for line in f_feature.readlines():
            if re.search(r'#if defined', line) != None:
                find_chipmodule = 1
                break        
        if find_chipmodule == 1:
            print 'Not find the chipmodule in your command, please check'
            sys.exit()
    
    f_feature.close()


    # Parse the feature file
    f_feature = open(feature_file_path, 'r')

    if the_args.chipmodule != None:
        for line in f_feature.readlines():
            if start_parse_soc == 0:
                if re.search(r'SOC module features', line) != None:
                    start_parse_soc = 1
            else:
                if re.search(r'module features',line)!=None:
                    start_parse_soc = 0
                if re.search(r'#if', line) != None:
                    with_chipmodule = 1
                if with_chipmodule == 1:
                    if re.search(the_args.chipmodule, line) != None:
                        parse_under_chipmodule = 1
                    if parse_under_chipmodule == 1:                       
                        if (re.search(r'#elif',line)!=None or re.search(r'#endif',line)!= None) and re.search(the_args.chipmodule, line)==None :
                            parse_under_chipmodule = 0 
                            with_chipmodule = 0
                            start_parse_soc = 0
                        if re.search(r'(#define)\s*(FSL_FEATURE_SOC_\w*)\s*(\(\d\))',line) != None:
                            searchobj = re.search(r'(#define)\s*(FSL_FEATURE_SOC_\w*)\s*(\(\d\))',line)
                            if searchobj.group(3) == '(0)':
                                pass
                            else:
                                soc_feature_dic[searchobj.group(2)] = 'true'  
                else:
                    if re.search(r'(#define)\s*(FSL_FEATURE_SOC_\w*)\s*(\(\d\))',line) != None:
                        searchobj = re.search(r'(#define)\s*(FSL_FEATURE_SOC_\w*)\s*(\(\d\))',line)
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
    else:
        for line in f_feature.readlines():
            # Parse the soc module features
            if start_parse_soc == 0:
                if re.search(r'SOC module features', line) != None:
                    start_parse_soc = 1
            else:
                if re.search(r'module features',line)!=None:
                    start_parse_soc = 0
                if re.search(r'(#define)\s*(FSL_FEATURE_SOC_\w*)\s*(\(\d\))',line) != None:
                    searchobj = re.search(r'(#define)\s*(FSL_FEATURE_SOC_\w*)\s*(\(\d\))',line)
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
    
    return soc_feature_dic
    