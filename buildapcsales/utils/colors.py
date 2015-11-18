

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

''' Example Print Statement
print bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC
'''


RESET_ALL_COLORS_AND_BRIGHTNESSES = '\033[0m'
BRIGHT = '\033[1m'
DIM = '\033[2m'      # dim (looks same as normal brightness)
NORMAL_BRIGHTNESS = '\033[22m'

# FOREGROUND:
FORE_BLACK = '\033[30m'
FORE_RED = '\033[31m'
FORE_GREEN = '\033[32m'
FORE_YELLOW = '\033[33m'
FORE_BLUE = '\033[34m'
FORE_MAGENTA = '\033[35m'
FORE_CYAN = '\033[36m'
FORE_WHITE = '\033[37m'
FORE_RESET = '\033[39m'

# BACKGROUND
BACK_BLACK = '\033[40m'
BACK_RED = '\033[41m'
BACK_GREEN = '\033[42m'
BACK_YELLOW = '\033[43m'
BACK_BLUE = '\033[44m'
BACK_MAGENTA = '\033[45m'
BACK_CYAN = '\033[46m'
BACK_WHITE = '\033[47m'
BACK_RESET = '\033[49m'

''' cursor positioning
ESC [ y;x H     # position cursor at x across, y down
ESC [ y;x f     # position cursor at x across, y down
ESC [ n A       # move cursor n lines up
ESC [ n B       # move cursor n lines down
ESC [ n C       # move cursor n characters forward
ESC [ n D       # move cursor n characters backward

# clear the screen
ESC [ mode J    # clear the screen

# clear the line
ESC [ mode K    # clear the line
'''