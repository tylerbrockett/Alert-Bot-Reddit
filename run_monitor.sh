#!/bin/bash

project_root=`dirname $0`
monitor=${project_root%%/}/bot/monitor.py

gnome-terminal --command "python $monitor"

# XTERM is for other systems
#xterm -hold -title "Bot Monitor" -e python $bot_monitor

