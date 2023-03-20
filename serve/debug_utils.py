from simple_chalk import (greenBright, redBright, blueBright, yellowBright, white, whiteBright, cyan)

'''
Simple Chalk Docs
-----------------

The following colors are exported

black
red
green
yellow
blue
magenta
cyan
white
blackBright (also 'gray' and 'grey')
redBright
greenBright
yellowBright
blueBright
magentaBright
cyanBright
whiteBright
Each color also has a camel-cased bg equivalent. e.g. bgBlack and bgYellowBright

Finally the following miscellaneous styles are exported

bold
dim
underline
hidden
------------------*END DOCS*--------------------------------
'''


def debug(message : str, type: str = 'INFO'):
    '''params:
    type - takes the degree of importance of message
    It can take the following degrees:
    
    1) 'INFO' - 'i'
    2) 'SUCCESS' - 's'
    3) 'DEBUG' - 'd'
    4) 'WARNING' - 'w'
    5) 'ERROR' - 'e' [HIGHEST PRIORITY - URGENT]
    '''
    if type == 'ERROR' or type == 'e':
        print(redBright(f"[ERROR] {message}"))
    elif type == 'WARNING' or type == 'w':
        print(yellowBright(f"[WARNING] {message}"))
    elif type == 'DEBUG' or type == 'd':
        print(blueBright(f"[DEBUG] {message}"))
    elif type == 'SUCCESS' or type == 's':
        print(greenBright(f"[SUCCESS] {message}"))
    elif type == 'INFO' or type == 'i':
        print(cyan(f"[INFO] {message}"))
    else:
        print(f"{message}")
    