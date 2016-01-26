@echo off

set BUILD_NAME_THIS_TIME=build2
set BUILD_MODE=release
 
if "%1"=="keil" goto keil
if "%1"=="kds" goto kds
if "%1"=="atl" goto atl

start "" %0 keil
python autobuild_iar_release_package.py -n %BUILD_NAME_THIS_TIME% -m %BUILD_MODE%
pause>nul
exit

:keil
start "" %0 kds
python autobuild_keil_%BUILD_MODE%_package.py -n %BUILD_NAME_THIS_TIME% -m %BUILD_MODE%
pause>nul
exit

:kds
python autobuild_kds_%BUILD_MODE%_package.py -n %BUILD_NAME_THIS_TIME% -m %BUILD_MODE%
pause>nul
exit

:atl
python autobuild_atl_%BUILD_MODE%_package.py -n %BUILD_NAME_THIS_TIME% -m %BUILD_MODE%
pause>nul
exit