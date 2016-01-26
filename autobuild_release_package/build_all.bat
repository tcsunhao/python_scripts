@echo off

set BUILD_NAME_THIS_TIME=build_1
set BUILD_MODE=release
set BUILD_PATH="E:\tmp\SDK_2.0_FRDM-K82F_all_nda_3f09dc9\boards\frdmk82f"
 
if "%1"=="keil" goto keil
if "%1"=="kds" goto kds
if "%1"=="atl" goto atl
if "%1"=="armgcc" goto armgcc

start "" %0 keil
python autobuild_iar_release_package.py -n %BUILD_NAME_THIS_TIME% -m %BUILD_MODE% -r %BUILD_PATH%
pause>nul
exit

:keil
start "" %0 kds
python autobuild_keil_release_package.py -n %BUILD_NAME_THIS_TIME% -m %BUILD_MODE% -r %BUILD_PATH%
pause>nul
exit

:kds
start "" %0 atl
python autobuild_kds_release_package.py -n %BUILD_NAME_THIS_TIME% -m %BUILD_MODE% -r %BUILD_PATH%
pause>nul
exit

:atl
start "" %0 armgcc
python autobuild_atl_release_package.py -n %BUILD_NAME_THIS_TIME% -m %BUILD_MODE% -r %BUILD_PATH%
pause>nul
exit

:armgcc
python autobuild_armgcc_release_package.py -n %BUILD_NAME_THIS_TIME% -m %BUILD_MODE% -r %BUILD_PATH%
pause>nul