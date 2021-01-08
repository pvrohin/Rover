#!/bin/bash

model_file=${1:-robot.urdf} # set default file to open if one is not specified on command line

roslaunch urdf_tutorial display.launch  model:=$model_file gui:=True
