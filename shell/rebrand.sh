#!/bin/sh
#
# File:  rebrand.sh
# =================
# Copyright (c) 2016 Freescale Semiconductor
# 
# Author : Holt Sun 
# 

# cd /e/git_sdk_2.0_rel/mcu-sdk-2.0/platform/drivers/lpc_adc

echo "Start rebrand work."
echo "      "
# Change the name from "fsl_*" to "mcux_*"
echo "Change the files'names from "fsl_*" to "mcux_*""
for fname in $(find . -name "fsl_*")
do
    echo $fname "==>" ${fname/fsl/mcux}
    mv $fname ${fname/fsl/mcux}
done

# Update include file from fsl_xxxxx.h to mcux_xxxx.h
echo
echo "Change include files from fsl_xxxxx.h to mcux_xxxx.h"
for fname in $(find . -type f | xargs grep -rl "fsl_")
do
    echo "Update" $fname
    sed -i 's/fsl_/mcux_/g' $fname
done

# Update the FSL to MCUX
# 1. __FSL_XXX_H__ to __MCUX_XXX_H__
# 2. feature : FSL_FEATURE_SOC_ADC12_COUNT to MCUX_FEATURE_SOC_ADC12_COUNT
echo
echo "Change macro FSL to MCUX"
for fname in $(find . -type f | xargs grep -rl "FSL_")
do
    echo "Update" $fname
    sed -i 's/FSL_/MCUX_/g' $fname
done

# Update the Freescale/freescale to NXP
echo
echo "Change "Freescale/freescale" to "NXP""
for fname in $(find . -type f | xargs grep -rl "[F|f]reescale")
do
    echo "Update" $fname
    sed -i 's/[F|f]reescale/NXP/g' $fname
done

echo
echo "Rebrand job is finished"
