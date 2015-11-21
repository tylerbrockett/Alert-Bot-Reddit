#!/bin/bash

project_root=`dirname $0`

bot_monitor=${project_root%%/}/bot/monitor.py

gnome-terminal --command "python $bot_monitor"

# XTERM is for other systems
#xterm -hold -title "Bot Monitor" -e python $bot_monitor

