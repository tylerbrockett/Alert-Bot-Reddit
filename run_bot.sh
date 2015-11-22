#!/bin/bash

project_root=`dirname $0`

bot=${project_root%%/}/bot/bot.py
gnome-terminal --command "python $bot"

# XTERM is for other systems
#xterm -hold -title "/r/buildapcsales bot" -e python $bot

